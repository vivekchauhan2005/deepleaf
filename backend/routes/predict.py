from fastapi import APIRouter, UploadFile, File

from controllers.predict_controller import predict_controller


router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


@router.post("/")
async def predict(
    file: UploadFile = File(...)
):

    return await predict_controller(file)