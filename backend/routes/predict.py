
from datetime import datetime
from io import BytesIO

from bson import ObjectId
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
    Query,
)
from fastapi.responses import StreamingResponse, HTMLResponse
from pymongo.errors import PyMongoError

from controllers.predict_controller import predict_controller
from config.database import db
from utils.auth import get_current_user
from utils.model_comparison import (
    generate_model_comparison_line_graph,
    generate_prediction_line_graph,
    get_latest_prediction_graph,
    get_model_comparison_metrics,
    generate_comparison_html,
)


router = APIRouter(
    prefix="/predict",
    tags=["Prediction"],
)


def serialize_prediction(record):
    """Convert a MongoDB prediction document into JSON-safe data."""
    created_at = record.get("created_at")

    return {
        "id": str(record["_id"]),
        "filename": record.get("filename", "Unknown image"),
        "is_leaf": record.get("is_leaf"),
        "disease": record.get("disease"),
        "formatted_disease": record.get("formatted_disease"),
        "plant_name": record.get("plant_name"),
        "confidence": record.get("confidence"),
        "severity": record.get("severity"),
        "message": record.get("message"),
        "created_at": (
            created_at.isoformat()
            if isinstance(created_at, datetime)
            else str(created_at) if created_at is not None else None
        ),
    }


@router.post("/")
async def predict(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """Predict plant disease for an authenticated user."""
    return await predict_controller(
        file=file,
        current_user=current_user,
    )


@router.get("/dashboard")
async def get_dashboard(
    current_user: dict = Depends(get_current_user),
):
    """Return prediction statistics and the latest five records."""
    try:
        user_email = current_user["email"]
        collection = db["predictions"]
        user_filter = {"user_email": user_email}

        total_predictions = collection.count_documents(user_filter)

        healthy_filter = {
            **user_filter,
            "is_leaf": True,
            "disease": {
                "$regex": r"(^|___)healthy$",
                "$options": "i",
            },
        }

        healthy_count = collection.count_documents(healthy_filter)

        diseased_filter = {
            **user_filter,
            "is_leaf": True,
            "disease": {
                "$exists": True,
                "$nin": [None, ""],
                "$not": {
                    "$regex": r"(^|___)healthy$",
                    "$options": "i",
                },
            },
        }

        diseased_count = collection.count_documents(diseased_filter)

        recent_records = (
            collection.find(user_filter)
            .sort("created_at", -1)
            .limit(5)
        )

        recent_predictions = [
            serialize_prediction(record)
            for record in recent_records
        ]

        return {
            "success": True,
            "total_predictions": total_predictions,
            "healthy_count": healthy_count,
            "diseased_count": diseased_count,
            "recent_predictions": recent_predictions,
        }

    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail=(
                "Unable to load dashboard data. "
                "Check the database connection."
            ),
        )


@router.get("/history")
async def get_prediction_history(
    current_user: dict = Depends(get_current_user),
):
    """Return up to 100 saved predictions for the logged-in user."""
    try:
        user_email = current_user["email"]

        records = (
            db["predictions"]
            .find({"user_email": user_email})
            .sort("created_at", -1)
            .limit(100)
        )

        predictions = [
            serialize_prediction(record)
            for record in records
        ]

        return {
            "success": True,
            "predictions": predictions,
            "total": len(predictions),
        }

    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail=(
                "Unable to load prediction history. "
                "Check the database connection."
            ),
        )


@router.get(
    "/comparison/line-graph",
    summary="CNN vs VGG-19 Accuracy & Confidence Line Graph",
    description="Generates and renders a high-resolution line graph comparing CNN and VGG-19 models using accuracy and confidence scores across the 14 supported agricultural crops and training convergence checkpoints. Viewable directly inside Swagger UI.",
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Rendered PNG comparison line graph of CNN vs VGG-19.",
        }
    },
    tags=["Model Analytics & Comparison", "Prediction"],
)
async def get_comparison_line_graph(
    mode: str = Query(
        "combined",
        description="Line graph mode: 'combined' (both crops & training convergence), 'crops' (14 crop categories only), or 'epochs' (10-epoch training trajectory only)",
    ),
):
    """Return a publication-grade line graph comparing CNN and VGG-19 accuracy and confidence scores."""
    image_buffer = generate_model_comparison_line_graph(mode=mode)
    return StreamingResponse(
        image_buffer,
        media_type="image/png",
        headers={
            "Content-Disposition": f'inline; filename="cnn_vs_vgg19_{mode}_line_graph.png"',
            "Cache-Control": "public, max-age=3600",
        },
    )


@router.get(
    "/comparison/line-graph.png",
    summary="Direct Image URL for CNN vs VGG-19 Line Graph",
    description="Direct PNG image endpoint for embedding in Markdown, HTML, external web apps, or report downloads.",
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Rendered PNG comparison line graph.",
        }
    },
    tags=["Model Analytics & Comparison"],
)
async def get_comparison_line_graph_direct(
    mode: str = Query("combined", description="Line graph mode: 'combined', 'crops', or 'epochs'"),
):
    """Direct PNG image URL for embedding."""
    image_buffer = generate_model_comparison_line_graph(mode=mode)
    return StreamingResponse(
        image_buffer,
        media_type="image/png",
        headers={
            "Content-Disposition": 'inline; filename="cnn_vs_vgg19_comparison.png"',
            "Cache-Control": "public, max-age=3600",
        },
    )


@router.get(
    "/comparison/metrics",
    summary="CNN vs VGG-19 Performance & Accuracy Confidence Scores (JSON)",
    description="Returns raw structured JSON metrics comparing CNN and VGG-19 overall accuracy (97.32% vs 85.29%), mean confidence (94.11% vs 87.85%), and crop-by-crop validation results.",
    tags=["Model Analytics & Comparison", "Prediction"],
)
async def get_comparison_metrics_json():
    """Return structured JSON metrics comparing CNN vs VGG-19."""
    return get_model_comparison_metrics()


@router.get(
    "/comparison/interactive-view",
    response_class=HTMLResponse,
    summary="Interactive Model Performance Dashboard (HTML)",
    description="Renders a standalone interactive HTML dashboard featuring the line graph, summary KPI cards, and the 14-crop accuracy breakdown table.",
    tags=["Model Analytics & Comparison"],
)
async def get_comparison_interactive_dashboard():
    """Return an interactive HTML dashboard comparing CNN vs VGG-19."""
    html_content = generate_comparison_html()
    return HTMLResponse(content=html_content)


@router.get(
    "/comparison/latest-line-graph.png",
    summary="Latest Prediction CNN vs VGG-19 Line Graph",
    description="Direct image URL streaming the line graph comparing CNN and VGG-19 confidence scores for the most recently diagnosed leaf image. Dynamically reflects each uploaded photo.",
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Rendered PNG line graph for the most recent prediction.",
        }
    },
    tags=["Model Analytics & Comparison", "Prediction"],
)
async def get_latest_prediction_line_graph():
    """Return the CNN vs VGG-19 confidence line graph for the most recently analyzed leaf image."""
    buffer = get_latest_prediction_graph()
    return StreamingResponse(
        buffer,
        media_type="image/png",
        headers={
            "Content-Disposition": 'inline; filename="latest_prediction_line_graph.png"',
            "Cache-Control": "no-store",
        },
    )


@router.get(
    "/{record_id}/comparison-graph.png",
    summary="Prediction Specific Confidence Line Graph",
    description="Return a line graph comparing CNN versus VGG-19 confidence scores for a specific saved prediction record.",
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Rendered PNG line graph for the specific prediction.",
        }
    },
    tags=["Prediction"],
)
async def get_comparison_graph(
    record_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Return a CNN versus VGG-19 line graph for a saved prediction record."""
    if not ObjectId.is_valid(record_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid prediction record ID.",
        )

    try:
        record = db["predictions"].find_one({
            "_id": ObjectId(record_id),
            "user_email": current_user["email"],
        })
    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve prediction data.",
        )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Prediction record not found.",
        )

    if not record.get("is_leaf", False):
        raise HTTPException(
            status_code=422,
            detail="A comparison graph is only available for leaf images.",
        )

    candidates = record.get("candidates_comparison")
    if candidates and isinstance(candidates, list) and len(candidates) > 0:
        image_buffer = generate_prediction_line_graph(candidates_or_cnn=candidates)
    else:
        comparison = record.get("comparison") or {}
        cnn = comparison.get("cnn") or {}
        vgg19 = comparison.get("vgg19") or {}
        image_buffer = generate_prediction_line_graph(candidates_or_cnn=cnn, vgg_data=vgg19)

    return StreamingResponse(
        image_buffer,
        media_type="image/png",
        headers={
            "Content-Disposition": 'inline; filename="prediction-comparison-line-graph.png"',
            "Cache-Control": "no-store",
        },
    )
