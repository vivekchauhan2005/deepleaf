import json
from pathlib import Path
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.vgg19 import preprocess_input

ROOT = Path(__file__).resolve().parents[2]
VAL_DIR = ROOT / "dataset" / "PlantVillage" / "val"
MODEL_DIR = ROOT / "ml" / "models"
SAMPLES_PER_CLASS = 10
BATCH_SIZE = 8

with open(MODEL_DIR / "class_labels.json", encoding="utf-8") as f:
    labels = json.load(f)

print("Classes in labels:", len(labels))
print("Validation folder:", VAL_DIR)

if not VAL_DIR.exists():
    raise FileNotFoundError(f"Validation folder missing: {VAL_DIR}")

folder_classes = sorted(p.name for p in VAL_DIR.iterdir() if p.is_dir())
if folder_classes != labels:
    print("WARNING: Validation folder order/names do not exactly match class_labels.json")
    print("First mismatches may indicate a label mapping issue.")

samples = []
for class_index, class_name in enumerate(labels):
    class_dir = VAL_DIR / class_name
    if not class_dir.is_dir():
        print("Missing class folder:", class_name)
        continue

    files = sorted(
        p for p in class_dir.iterdir()
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
    )
    for path in files[:SAMPLES_PER_CLASS]:
        samples.append((path, class_index))

if not samples:
    raise RuntimeError("No validation images found.")

print("Images selected:", len(samples))
print("Loading models...")

models = {
    "CNN": (
        tf.keras.models.load_model(MODEL_DIR / "cnn_disease.keras", compile=False),
        "raw"
    ),
    "VGG19_95plus": (
        tf.keras.models.load_model(MODEL_DIR / "vgg19_95plus.keras", compile=False),
        "raw"
    ),
    "VGG19_final": (
        tf.keras.models.load_model(MODEL_DIR / "vgg19_final.keras", compile=False),
        "vgg"
    ),
}

for name, (model, _) in models.items():
    print(f"{name}: output={model.output_shape}")
    if model.output_shape[-1] != len(labels):
        raise ValueError(
            f"{name} outputs {model.output_shape[-1]} classes, "
            f"but labels contain {len(labels)}"
        )

actual = np.array([label for _, label in samples])
all_predictions = {}

for name, (model, mode) in models.items():
    print(f"\nTesting {name}...")
    predictions = []

    for start in range(0, len(samples), BATCH_SIZE):
        batch_paths = samples[start:start + BATCH_SIZE]
        images = []

        for path, _ in batch_paths:
            img = tf.keras.utils.load_img(
                path, target_size=(224, 224), color_mode="rgb"
            )
            images.append(tf.keras.utils.img_to_array(img))

        x = np.asarray(images, dtype=np.float32)

        # CNN has internal Rescaling(1/255).
        # VGG19_95plus has VGG preprocessing inside its model.
        # VGG19_final was trained with external preprocess_input.
        if mode == "vgg":
            x = preprocess_input(x)

        scores = model.predict(x, verbose=0)
        predictions.extend(np.argmax(scores, axis=1))

        if start == 0 or start + BATCH_SIZE >= len(samples):
            print(f"  Processed {min(start + BATCH_SIZE, len(samples))}/{len(samples)}")

    predictions = np.asarray(predictions)
    all_predictions[name] = predictions
    accuracy = np.mean(predictions == actual) * 100
    print(f"{name} accuracy on this subset: {accuracy:.2f}%")

print("\n========== COMPARISON ==========")
for name, pred in all_predictions.items():
    print(f"{name}: {(pred == actual).mean() * 100:.2f}%")

if "CNN" in all_predictions and "VGG19_95plus" in all_predictions:
    same = np.mean(all_predictions["CNN"] == all_predictions["VGG19_95plus"]) * 100
    print(f"CNN vs VGG19_95plus agreement: {same:.2f}%")

if "VGG19_final" in all_predictions and "VGG19_95plus" in all_predictions:
    same = np.mean(all_predictions["VGG19_final"] == all_predictions["VGG19_95plus"]) * 100
    print(f"VGG19_final vs VGG19_95plus agreement: {same:.2f}%")

print("\nPreliminary test complete. This is a 10-images-per-class subset, not final accuracy.")
