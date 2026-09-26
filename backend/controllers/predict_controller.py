import os
import uuid

from fastapi import UploadFile, HTTPException

from services.prediction_service import predict_image

 
UPLOAD_DIR = "/mnt/c/project/deepleaf/backend/uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


async def predict_controller(file: UploadFile):

    if not file:
        raise HTTPException(
            status_code=400,
            detail="No image uploaded"
        )


    filename = file.filename or ""


    extension = os.path.splitext(
        filename
    )[1].lower()


    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG, PNG and WEBP images are allowed"
        )


    unique_filename = f"{uuid.uuid4()}{extension}"


    image_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )


    try:

        contents = await file.read()


        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty"
            )


        with open(
            image_path,
            "wb"
        ) as image_file:

            image_file.write(contents)
 
        result = predict_image(
            image_path
        )
 

        if not result["is_leaf"]:

            return {
                "success": True,
                "is_leaf": False,
                "leaf_confidence": result["leaf_confidence"],
                "filename": filename,
                "message": "Please enter a plant leaf image.",
                "disease": None,
                "confidence": None,

                "dataset_evidence": {
                    "available": False,
                    "plant": None,
                    "disease": None,
                    "images": []
                },

                "comparison": {
                    "cnn": {
                        "disease": None,
                        "confidence": None
                    },
                    "vgg19": {
                        "disease": None,
                        "confidence": None
                    }
                }
            }


        # --------------------------------
        # LEAF / DISEASE RESULT
        # --------------------------------

        return {
            "success": True,
            "is_leaf": True,
            "leaf_confidence": result["leaf_confidence"],
            "filename": filename,

            "disease": result["disease"],
            "confidence": result["confidence"],

            "dataset_evidence": result.get(
                "dataset_evidence",
                {
                    "available": False,
                    "plant": None,
                    "disease": None,
                    "images": []
                }
            ),

            "comparison": result.get(
                "comparison",
                {
                    "cnn": {
                        "disease": None,
                        "confidence": None
                    },
                    "vgg19": {
                        "disease": None,
                        "confidence": None
                    }
                }
            )
        }


    except HTTPException:

        raise


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )

 
    finally:
 
        pass