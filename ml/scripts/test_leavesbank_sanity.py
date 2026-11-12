import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

BASE_DIR = "/mnt/c/project/deepleaf"

LEAVESBANK_DIR = os.path.join(
    BASE_DIR,
    "dataset",
    "LeavesBank",
    "Apple Leaf",
    "Apple Leaf Seperated"
)

CNN_PATH = os.path.join(BASE_DIR, "ml", "models", "cnn_disease.keras")
VGG19_PATH = os.path.join(BASE_DIR, "ml", "models", "vgg19_95plus.keras")
LABELS_PATH = os.path.join(BASE_DIR, "ml", "models", "class_labels.json")

with open(LABELS_PATH) as f:
    labels = json.load(f)

IMAGE_SIZE = (224, 224)

def load_image(path):
    img = image.load_img(path, target_size=IMAGE_SIZE)
    arr = image.img_to_array(img)
    return np.expand_dims(arr, axis=0)

def test_model(model_path, model_name):

    print("\n" + "=" * 50)
    print(model_name)
    print("=" * 50)

    print("Loading model...")
    model = load_model(model_path, compile=False)

    for folder_name in ["scab", "cider_apple_rust", "healthy"]:

        folder = os.path.join(
            LEAVESBANK_DIR,
            folder_name,
            "images"
        )

        files = [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        print(f"\n{folder_name}: testing 10 images")

        for path in files[:10]:

            img = load_image(path)

            prediction = model.predict(img, verbose=0)[0]

            top_indices = np.argsort(prediction)[-5:][::-1]

            print("\nFile:", os.path.basename(path))

            for idx in top_indices:
                print(
                    f"  {labels[idx]}: "
                    f"{prediction[idx] * 100:.2f}%"
                )

    del model
    tf.keras.backend.clear_session()


print("GPU:", tf.config.list_physical_devices("GPU"))

test_model(CNN_PATH, "CUSTOM CNN")

test_model(VGG19_PATH, "VGG19")