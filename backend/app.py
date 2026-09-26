from fastapi import FastAPI
from config.database import db
from routes import auth, predict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="DeepLeaf AI",
    description="AI Plant Disease Detection"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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