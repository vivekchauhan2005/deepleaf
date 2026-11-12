import os
import sys
import json
import numpy as np
import tensorflow as tf

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg19 import preprocess_input

BASE_DIR = r"C:\project\deepleaf"

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "models",
    "vgg19_final.keras"
)

LABELS_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "models",
    "class_labels.json"
)

IMG_SIZE = (224, 224)

if not os.path.exists(LABELS_PATH):
    print("ERROR: class_labels.json not found!")
    print(LABELS_PATH)
    sys.exit(1)

with open(LABELS_PATH, "r") as f:
    class_names = json.load(f)

print(f"Loaded {len(class_names)} classes")

if not os.path.exists(MODEL_PATH):
    print("ERROR: Model not found!")
    print(MODEL_PATH)
    sys.exit(1)

print("Loading VGG19 model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully!")


def predict_disease(image_path):

    if not os.path.exists(image_path):
        print("ERROR: Image not found!")
        print(image_path)
        return

    img = image.load_img(
        image_path,
        target_size=IMG_SIZE
    )

    img_array = image.img_to_array(img)

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    img_array = preprocess_input(
        img_array
    )

    predictions = model.predict(
        img_array,
        verbose=0
    )

    predicted_index = np.argmax(
        predictions[0]
    )

    confidence = (
        float(predictions[0][predicted_index]) * 100
    )

    predicted_class = class_names[
        predicted_index
    ]

    print("\n" + "=" * 55)
    print("             DEEPLEAF RESULT")
    print("=" * 55)
    print(
        f"Image      : {os.path.basename(image_path)}"
    )
    print(
        f"Disease    : {predicted_class}"
    )
    print(
        f"Confidence : {confidence:.2f}%"
    )
    print("=" * 55)

    return predicted_class, confidence


if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("\nUsage:")
        print(
            'python predict.py "path_to_image"'
        )

        print("\nExample:")
        print(
            'python predict.py "C:\\project\\deepleaf\\test.jpg"'
        )

        sys.exit(1)

    image_path = sys.argv[1]

    predict_disease(image_path)