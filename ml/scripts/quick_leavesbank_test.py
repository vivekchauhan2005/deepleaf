import json
import sys
from pathlib import Path
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.vgg19 import preprocess_input

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "ml/models/leavesbank_vgg19.keras"
LABELS_PATH = ROOT / "ml/models/leavesbank_class_labels.json"

if len(sys.argv) < 2:
    print('Usage: python ml/scripts/quick_leavesbank_test.py "/path/to/leaf.jpg"')
    raise SystemExit(1)

model = tf.keras.models.load_model(MODEL_PATH, compile=False)
labels = json.loads(LABELS_PATH.read_text(encoding="utf-8"))

if model.output_shape[-1] != len(labels):
    raise ValueError("Model output and label count mismatch")

img = tf.keras.utils.load_img(sys.argv[1], target_size=(224, 224))
x = tf.keras.utils.img_to_array(img)
x = preprocess_input(np.expand_dims(x, axis=0))

pred = model.predict(x, verbose=0)[0]
for i in np.argsort(pred)[-5:][::-1]:
    print(f"{labels[int(i)]}: {pred[i] * 100:.2f}%")
