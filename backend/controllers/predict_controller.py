import os
import uuid
import logging
from io import BytesIO
from datetime import datetime, timezone
from pathlib import Path

from fastapi import UploadFile, HTTPException
from PIL import Image, UnidentifiedImageError

from config.database import db
from services.prediction_service import predict_image

logger = logging.getLogger(__name__)

# Dynamic cross-platform uploads path
BACKEND_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BACKEND_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


async def predict_controller(
    file: UploadFile,
    current_user: dict,
):
    image_path = None

    try:
        if not file or not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No image uploaded.",
            )

        extension = os.path.splitext(file.filename)[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Only JPG, JPEG, PNG, and WEBP images are allowed.",
            )

        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty.",
            )

        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="Image size must not exceed 10 MB.",
            )

        try:
            with Image.open(BytesIO(contents)) as image:
                if image.format not in {"JPEG", "PNG", "WEBP"}:
                    raise HTTPException(
                        status_code=400,
                        detail="Unsupported image format. Please upload JPG, PNG, or WEBP.",
                    )
                image.verify()
        except (UnidentifiedImageError, OSError, ValueError):
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is not a valid image.",
            )

        unique_filename = f"{uuid.uuid4()}{extension}"
        image_path = UPLOAD_DIR / unique_filename

        with open(image_path, "wb") as image_file:
            image_file.write(contents)

        # Run AI prediction service
        result = predict_image(str(image_path))

        response = {
            "success": True,
            "filename": file.filename,
            "is_leaf": result.get("is_leaf", False),
            "leaf_confidence": result.get("leaf_confidence"),
            "disease": result.get("disease"),
            "formatted_disease": result.get("formatted_disease"),
            "plant_name": result.get("plant_name"),
            "confidence": result.get("confidence"),
            "severity": result.get("severity"),
            "status": result.get("status"),
            "models_agree": result.get("models_agree", False),
            "species_agree": result.get("species_agree", False),
            "message": result.get("message"),
            "top_predictions": result.get("top_predictions", []),
            "details": result.get("details"),
            "dataset_evidence": result.get("dataset_evidence"),
            "comparison": result.get("comparison"),
            "candidates_comparison": result.get("candidates_comparison", []),
            "comparison_graph_base64": result.get("comparison_graph_base64"),
            "photography_tips": result.get("photography_tips"),
            "supported_crops": result.get("supported_crops", []),
            "herb_guide": result.get("herb_guide"),
            "unsupported_species_note": result.get("unsupported_species_note"),
            "record_id": None,
            "history_saved": False,
        }

        # Attempt to save to prediction history without failing the request if DB is offline
        record = {
            "user_email": current_user.get("email", "anonymous@deepleaf.ai"),
            "filename": file.filename,
            "is_leaf": response["is_leaf"],
            "leaf_confidence": response["leaf_confidence"],
            "disease": response["disease"],
            "formatted_disease": response["formatted_disease"],
            "plant_name": response["plant_name"],
            "confidence": response["confidence"],
            "severity": response["severity"],
            "status": response.get("status"),
            "message": response["message"],
            "details": response.get("details"),
            "comparison": response["comparison"],
            "candidates_comparison": response["candidates_comparison"],
            "dataset_evidence": response["dataset_evidence"],
            "top_predictions": response["top_predictions"],
            "photography_tips": response.get("photography_tips"),
            "comparison_graph_base64": response.get("comparison_graph_base64"),
            "models_agree": response.get("models_agree", False),
            "species_agree": response.get("species_agree", False),
            "created_at": datetime.now(timezone.utc),
        }

        try:
            if db is not None:
                saved = db["predictions"].insert_one(record)
                record_id = str(saved.inserted_id)
                response["record_id"] = record_id
                response["history_saved"] = True
                response["comparison_graph_url"] = f"/predict/{record_id}/comparison-graph.png"
        except Exception as db_err:
            logger.warning("Could not persist prediction to database: %s", db_err)

        return response

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Plant disease prediction failed: %s", exc)
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(exc)}",
        )
    finally:
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
            except OSError:
                logger.warning("Could not remove temporary image: %s", image_path)
        await file.close()
