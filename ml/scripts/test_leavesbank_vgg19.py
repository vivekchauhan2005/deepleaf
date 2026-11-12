import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.vgg19 import preprocess_input

BASE_DIR = r"C:\project\deepleaf"

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "models",
    "leavesbank_vgg19.keras"
)

LABELS_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "models",
    "leavesbank_class_labels.json"
)

print("=" * 65)
print("DEEPLEAF LEAVESBANK VGG19 REAL IMAGE TEST")
print("=" * 65)

model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

with open(
    LABELS_PATH,
    "r",
    encoding="utf-8"
) as file:
    class_names = json.load(file)

print(f"Classes loaded: {len(class_names)}")
print("Model loaded successfully!")

image_path = input(
    "\nEnter REAL IMAGE PATH: "
).strip().strip('"')

if not os.path.isfile(image_path):
    raise FileNotFoundError(
        f"Image not found: {image_path}"
    )

image = tf.keras.utils.load_img(
    image_path,
    target_size=(224, 224)
)

image_array = tf.keras.utils.img_to_array(
    image
)

image_array = np.expand_dims(
    image_array,
    axis=0
)

image_array = preprocess_input(
    image_array
)

predictions = model.predict(
    image_array,
    verbose=0
)[0]

top_indices = np.argsort(
    predictions
)[::-1][:5]

print("\n" + "=" * 65)
print("TOP 5 PREDICTIONS")
print("=" * 65)

for rank, index in enumerate(top_indices, start=1):
    print(
        f"{rank}. {class_names[index]} : "
        f"{predictions[index] * 100:.2f}%"
    )

print("=" * 65)