# ml/scripts/test_setup.py

print("🚀 DeepLeaf Setup Test Started...")

import os
import sys
import tensorflow as tf

print(f"✅ Python Version: {sys.version}")
print(f"✅ TensorFlow Version: {tf.__version__}")
 
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"✅ GPU Detected: {gpus}")
else:
    print("⚠️ No GPU detected. Running on CPU (expected on Windows).")

# Check paths
BASE_DIR = r"C:\Users\vkcha\OneDrive\Desktop\project\deepleaf"
TRAIN_DIR = os.path.join(BASE_DIR, "dataset", "PlantVillage", "train")

if os.path.exists(TRAIN_DIR):
    classes = os.listdir(TRAIN_DIR)
    print(f"✅ Dataset found at: {TRAIN_DIR}")
    print(f"✅ Total classes: {len(classes)}")
    print(f"✅ Classes: {classes[:5]}... (showing first 5)")
else:
    print(f"❌ Dataset NOT found at: {TRAIN_DIR}")

print("✅ Setup test complete!")