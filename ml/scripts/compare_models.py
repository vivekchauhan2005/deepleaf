import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.vgg19 import preprocess_input

BASE_DIR = r"C:\project\deepleaf"

PLANTVILLAGE_MODEL = os.path.join(BASE_DIR, "ml", "models", "vgg19_final.keras")
PLANTVILLAGE_VAL = os.path.join(BASE_DIR, "dataset", "PlantVillage", "val")

LEAVESBANK_MODEL = os.path.join(BASE_DIR, "ml", "models", "leavesbank_vgg19.keras")
LEAVESBANK_VAL = os.path.join(BASE_DIR, "dataset", "LeavesBank_Training", "val")

PLANTVILLAGE_LABELS = os.path.join(BASE_DIR, "ml", "models", "class_labels.json")
LEAVESBANK_LABELS = os.path.join(BASE_DIR, "ml", "models", "leavesbank_class_labels.json")

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

def load_labels(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def evaluate_model(model_path, val_path, labels_path, name):
    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    labels = load_labels(labels_path)

    generator = ImageDataGenerator(
        preprocessing_function=preprocess_input
    ).flow_from_directory(
        val_path,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="sparse",
        shuffle=False
    )

    model = tf.keras.models.load_model(
        model_path,
        compile=False
    )

    predictions = model.predict(
        generator,
        verbose=1
    )

    predicted_indices = np.argmax(predictions, axis=1)
    actual_indices = generator.classes

    correct = predicted_indices == actual_indices
    accuracy = np.mean(correct) * 100

    print("\n" + "-" * 70)
    print(f"{name} OVERALL ACCURACY: {accuracy:.2f}%")
    print("-" * 70)

    print("\nPER-IMAGE RESULTS")

    filenames = generator.filenames

    for i in range(len(filenames)):
        predicted_index = predicted_indices[i]
        actual_index = actual_indices[i]

        predicted_name = labels[predicted_index]
        actual_name = labels[actual_index]
        confidence = predictions[i][predicted_index] * 100

        status = "CORRECT" if predicted_index == actual_index else "WRONG"

        print(
            f"{i + 1}. {os.path.basename(filenames[i])} | "
            f"Actual: {actual_name} | "
            f"Predicted: {predicted_name} | "
            f"Confidence: {confidence:.2f}% | "
            f"{status}"
        )

    return accuracy

print("=" * 70)
print("DEEPLEAF MODEL ACCURACY COMPARISON")
print("=" * 70)

plantvillage_accuracy = evaluate_model(
    PLANTVILLAGE_MODEL,
    PLANTVILLAGE_VAL,
    PLANTVILLAGE_LABELS,
    "PLANTVILLAGE VGG19"
)

leavesbank_accuracy = evaluate_model(
    LEAVESBANK_MODEL,
    LEAVESBANK_VAL,
    LEAVESBANK_LABELS,
    "LEAVESBANK VGG19"
)

print("\n" + "=" * 70)
print("FINAL COMPARISON")
print("=" * 70)

print(
    f"PlantVillage VGG19 : "
    f"{plantvillage_accuracy:.2f}%"
)

print(
    f"LeavesBank VGG19   : "
    f"{leavesbank_accuracy:.2f}%"
)

if plantvillage_accuracy > leavesbank_accuracy:
    print("\nHIGHER ACCURACY: PlantVillage VGG19")
elif leavesbank_accuracy > plantvillage_accuracy:
    print("\nHIGHER ACCURACY: LeavesBank VGG19")
else:
    print("\nBOTH MODELS HAVE THE SAME ACCURACY")

print("=" * 70)