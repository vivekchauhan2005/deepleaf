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

# LeavesBank -> PlantVillage label mapping
CLASS_MAPPING = {
    "scab": "Apple___Apple_scab",
    "cider_apple_rust": "Apple___Cedar_apple_rust",
    "healthy": "Apple___healthy",
}

IMAGE_SIZE = (224, 224)

with open(LABELS_PATH, "r") as f:
    labels = json.load(f)

label_to_index = {label: i for i, label in enumerate(labels)}

print("Loading CNN...")
cnn = load_model(CNN_PATH, compile=False)

print("Loading VGG19...")
vgg19 = load_model(VGG19_PATH, compile=False)

results = {
    "CNN": {"correct": 0, "total": 0},
    "VGG19": {"correct": 0, "total": 0},
}

class_results = {
    "CNN": {},
    "VGG19": {},
}


def load_image(path):
    img = image.load_img(path, target_size=IMAGE_SIZE)
    arr = image.img_to_array(img)
    return np.expand_dims(arr, axis=0)


def evaluate_model(model, model_name):

    print(f"\n========== {model_name} ==========")

    total = 0
    correct = 0

    for folder_name, expected_label in CLASS_MAPPING.items():

        folder = os.path.join(LEAVESBANK_DIR, folder_name, "images")

        files = [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

        class_total = len(files)
        class_correct = 0

        print(f"\n{folder_name}: {class_total} images")

        expected_index = label_to_index[expected_label]

        for i, path in enumerate(files):

            try:
                img = load_image(path)

                # IMPORTANT:
                # Both current models perform their own preprocessing internally.
                prediction = model.predict(img, verbose=0)

                predicted_index = int(np.argmax(prediction[0]))

                if predicted_index == expected_index:
                    correct += 1
                    class_correct += 1

                total += 1

            except Exception as e:
                print(f"Error: {path}")
                print(e)

            if (i + 1) % 500 == 0:
                print(f"Processed: {i + 1}/{class_total}")

        accuracy = (class_correct / class_total) * 100

        class_results[model_name][folder_name] = {
            "correct": class_correct,
            "total": class_total,
            "accuracy": accuracy,
        }

        print(
            f"{folder_name} accuracy: "
            f"{class_correct}/{class_total} = {accuracy:.2f}%"
        )

    overall_accuracy = (correct / total) * 100

    results[model_name]["correct"] = correct
    results[model_name]["total"] = total
    results[model_name]["accuracy"] = overall_accuracy

    print(f"\n{model_name} overall:")
    print(f"Correct: {correct}/{total}")
    print(f"Accuracy: {overall_accuracy:.2f}%")

    return model


# Evaluate CNN first
evaluate_model(cnn, "CNN")

# Free CNN memory before VGG19 evaluation
del cnn
tf.keras.backend.clear_session()

# Evaluate VGG19
evaluate_model(vgg19, "VGG19")

del vgg19
tf.keras.backend.clear_session()


print("\n\n========================================")
print("       LEAVESBANK EXTERNAL TEST")
print("========================================")

for model_name in ["CNN", "VGG19"]:
    print(f"\n{model_name}")
    print(
        f"Accuracy: "
        f"{results[model_name]['correct']}/"
        f"{results[model_name]['total']} "
        f"= {results[model_name]['accuracy']:.2f}%"
    )

    for cls, data in class_results[model_name].items():
        print(
            f"  {cls}: "
            f"{data['correct']}/{data['total']} "
            f"= {data['accuracy']:.2f}%"
        )

cnn_acc = results["CNN"]["accuracy"]
vgg_acc = results["VGG19"]["accuracy"]

print("\n========================================")

if cnn_acc > vgg_acc:
    print("BETTER MODEL: CNN")
elif vgg_acc > cnn_acc:
    print("BETTER MODEL: VGG19")
else:
    print("RESULT: BOTH MODELS HAVE SAME ACCURACY")

print("========================================")