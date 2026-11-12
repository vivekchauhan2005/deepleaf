import os
import sys
import json
import numpy as np
import tensorflow as tf

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

IMAGE_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "PlantVillage",
    "val",
    "Apple___Apple_scab",
    "00075aa8-d81a-4184-8541-b692b78d398a___FREC_Scab 3335.JPG"
)

sys.path.insert(
    0,
    os.path.join(
        BASE_DIR,
        "backend"
    )
)

from utils.preprocess import preprocess_image

from tensorflow.keras.applications.vgg19 import preprocess_input


with open(
    LABELS_PATH,
    "r",
    encoding="utf-8"
) as file:
    class_names = json.load(file)


model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)


image = tf.keras.utils.load_img(
    IMAGE_PATH,
    target_size=(224, 224)
)

image_array = tf.keras.utils.img_to_array(
    image
)

image_array = np.expand_dims(
    image_array,
    axis=0
)

standalone_data = preprocess_input(
    image_array.copy()
)

backend_data = preprocess_image(
    IMAGE_PATH
)

print("=" * 70)
print("PREPROCESSING COMPARISON")
print("=" * 70)

print(
    "Arrays equal:",
    np.array_equal(
        standalone_data,
        backend_data
    )
)

print(
    "Maximum difference:",
    np.max(
        np.abs(
            standalone_data - backend_data
        )
    )
)

print(
    "Standalone shape:",
    standalone_data.shape
)

print(
    "Backend shape:",
    backend_data.shape
)

standalone_prediction = model.predict(
    standalone_data,
    verbose=0
)[0]

backend_prediction = model.predict(
    backend_data,
    verbose=0
)[0]

standalone_index = int(
    np.argmax(
        standalone_prediction
    )
)

backend_index = int(
    np.argmax(
        backend_prediction
    )
)

print("\n" + "=" * 70)
print("STANDALONE PREDICTION")
print("=" * 70)

print(
    class_names[standalone_index],
    f"{standalone_prediction[standalone_index] * 100:.2f}%"
)

print("\n" + "=" * 70)
print("BACKEND PREPROCESSING PREDICTION")
print("=" * 70)

print(
    class_names[backend_index],
    f"{backend_prediction[backend_index] * 100:.2f}%"
)

print("\n" + "=" * 70)
print("TOP 5 STANDALONE")
print("=" * 70)

for index in np.argsort(
    standalone_prediction
)[::-1][:5]:

    print(
        f"{class_names[index]} : "
        f"{standalone_prediction[index] * 100:.2f}%"
    )

print("\n" + "=" * 70)
print("TOP 5 BACKEND")
print("=" * 70)

for index in np.argsort(
    backend_prediction
)[::-1][:5]:

    print(
        f"{class_names[index]} : "
        f"{backend_prediction[index] * 100:.2f}%"
    )

print("=" * 70)