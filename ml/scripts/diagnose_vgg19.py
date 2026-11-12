"""
DeepLeaf model diagnostic.
Run from WSL:
  cd /mnt/c/project/deepleaf
  source ml/.venv/bin/activate
  python ml/scripts/diagnose_vgg19.py "/path/to/your/leaf-image.jpg"

This does NOT change or overwrite any model. It compares raw and VGG19-preprocessed
inference so we can detect a likely preprocessing mismatch.
"""
import json
import sys
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.vgg19 import preprocess_input

BASE_DIR = Path("/mnt/c/project/deepleaf")
MODEL_CANDIDATES = [
    BASE_DIR / "ml/models/vgg19_final.keras",
    BASE_DIR / "ml/models/vgg19_95plus.keras",
    BASE_DIR / "ml/models/leavesbank_vgg19.keras",
]
LABEL_CANDIDATES = [
    BASE_DIR / "ml/models/class_labels.json",
    BASE_DIR / "ml/models/leavesbank_class_labels.json",
]

def choose_existing(paths, description):
    for path in paths:
        if path.is_file():
            print(f"{description}: {path}")
            return path
    raise FileNotFoundError(
        f"No {description.lower()} found. Checked:\n" +
        "\n".join(str(p) for p in paths)
    )

def main():
    if len(sys.argv) < 2:
        print('Usage: python ml/scripts/diagnose_vgg19.py "/path/to/leaf.jpg"')
        raise SystemExit(2)

    image_path = Path(sys.argv[1].strip('"'))
    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    model_path = choose_existing(MODEL_CANDIDATES, "Model")
    labels_path = choose_existing(LABEL_CANDIDATES, "Labels")

    with labels_path.open(encoding="utf-8") as f:
        labels = json.load(f)

    print("Loading model...")
    model = tf.keras.models.load_model(model_path, compile=False)
    output_count = int(model.output_shape[-1])
    print(f"Model output classes: {output_count}")
    print(f"Label count: {len(labels)}")

    if output_count != len(labels):
        raise ValueError(
            "STOP: model output count and label count do not match. "
            "Do not trust predictions until the matching label file is found."
        )

    image = tf.keras.utils.load_img(image_path, target_size=(224, 224), color_mode="rgb")
    array = tf.keras.utils.img_to_array(image).astype("float32")
    batch_raw = np.expand_dims(array, axis=0)
    batch_preprocessed = preprocess_input(batch_raw.copy())

    def show_top(label, batch):
        values = np.asarray(model.predict(batch, verbose=0)[0], dtype=np.float64)
        if not np.all(np.isfinite(values)):
            print(f"\n{label}: ERROR - non-finite model outputs")
            return
        # Softmax models return probabilities. If output looks like logits,
        # print raw scores and do not call them confidence percentages.
        looks_like_probabilities = (
            np.all(values >= 0) and np.all(values <= 1.0001)
            and abs(float(values.sum()) - 1.0) < 0.05
        )
        indices = np.argsort(values)[::-1][:5]
        print(f"\n--- {label} ---")
        print("Output interpreted as probabilities:", looks_like_probabilities)
        for rank, idx in enumerate(indices, 1):
            suffix = f"{values[idx] * 100:.2f}%" if looks_like_probabilities else f"score={values[idx]:.5f}"
            print(f"{rank}. {labels[int(idx)]} | {suffix}")

    print(f"\nImage: {image_path}")
    show_top("RAW RGB input (0..255)", batch_raw)
    show_top("VGG19 preprocess_input applied", batch_preprocessed)
    print("\nCompare these results. If the two lists differ drastically, inference preprocessing may not match training.")
    print("This script cannot establish real-world accuracy by itself; test with labelled images not used for training.")

if __name__ == "__main__":
    main()
