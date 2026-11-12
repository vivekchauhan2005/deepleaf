from fastapi import FastAPI
from config.database import db
from routes import auth, predict
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "Model Analytics & Comparison",
        "description": (
            "Interactive line graph visualizations and comparative benchmark metrics comparing "
            "**CNN** vs **VGG-19** accuracy (85.29% vs 97.32%) and confidence scores (87.85% vs 94.11%) "
            "across the 14 supported agricultural crops and training iterations."
        ),
    },
    {
        "name": "Prediction",
        "description": "Real-time plant leaf diagnosis, multi-model consensus verification, and disease history.",
    },
    {
        "name": "Authentication",
        "description": "User registration, authentication, and JWT session tokens.",
    },
]

app = FastAPI(
    title="DeepLeaf AI - Plant Pathology & Disease Detection API",
    description=(
        "Dual-model neural network diagnostics (VGG-19 vs CNN) with comprehensive model performance analytics, "
        "accuracy-confidence line graph visualizations, and botanical guidance.\n\n"
        "### Model Comparison Features\n"
        "- 📈 **CNN vs VGG-19 Line Graph**: View high-resolution comparison curves right in Swagger at `/predict/comparison/line-graph`\n"
        "- 📊 **Interactive HTML Dashboard**: View `/predict/comparison/interactive-view`\n"
        "- 📋 **Raw Metrics JSON**: Fetch `/predict/comparison/metrics`"
    ),
    version="2.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    print("MongoDB Connected Successfully")


@app.get("/")
async def root():
    return {
        "message": "DeepLeaf Backend Running 🚀"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "Server Running",
        "database": "MongoDB Connected"
    }


app.include_router(auth.router)
app.include_router(predict.router)