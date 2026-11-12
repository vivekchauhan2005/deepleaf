import os
import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from tensorflow.keras.applications.vgg19 import preprocess_input

BASE_DIR = r"C:\project\deepleaf"
TEST_DIR = os.path.join(BASE_DIR, "dataset", "LeafCheck", "test")
MODEL_PATH = os.path.join(BASE_DIR, "ml", "models", "leaf_checker.keras")

IMG_SIZE = (224, 224)

model = tf.keras.models.load_model(
    MODEL_PATH,
    custom_objects={"preprocess_input": preprocess_input},
    compile=False,
    safe_mode=False
)

y_true = []
y_pred = []

for label_name, label in [("leaf", 0), ("non_leaf", 1)]:
    folder = os.path.join(TEST_DIR, label_name)

    for filename in os.listdir(folder):
        image_path = os.path.join(folder, filename)

        try:
            image = tf.keras.utils.load_img(
                image_path,
                target_size=IMG_SIZE
            )

            image_array = tf.keras.utils.img_to_array(image)
            image_array = np.expand_dims(image_array, axis=0)
            image_array = preprocess_input(image_array)

            prediction = float(
                model.predict(image_array, verbose=0)[0][0]
            )

            predicted_label = 1 if prediction >= 0.5 else 0

            y_true.append(label)
            y_pred.append(predicted_label)

        except Exception as error:
            print(f"Skipped: {image_path}")
            print(error)

accuracy = accuracy_score(y_true, y_pred)
matrix = confusion_matrix(y_true, y_pred)

print("=" * 70)
print("DEEPLEAF LEAF CHECKER TEST")
print("=" * 70)
print(f"Total test images : {len(y_true)}")
print(f"Correct           : {sum(a == b for a, b in zip(y_true, y_pred))}")
print(f"Incorrect         : {sum(a != b for a, b in zip(y_true, y_pred))}")
print(f"Accuracy          : {accuracy * 100:.2f}%")
print("=" * 70)
print("CONFUSION MATRIX")
print("=" * 70)
print(matrix)
print("=" * 70)
print("CLASSIFICATION REPORT")
print("=" * 70)
print(
    classification_report(
        y_true,
        y_pred,
        target_names=["leaf", "non_leaf"],
        digits=4
    )
)