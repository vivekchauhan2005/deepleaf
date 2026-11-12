import os
import tensorflow as tf
from tensorflow.keras.applications.vgg19 import VGG19, preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import json
import pandas as pd
 
BASE_DIR = r"C:\project\deepleaf"
TRAIN_DIR = '/mnt/c/project/deepleaf/dataset/PlantVillage/train'
VAL_DIR = '/mnt/c/project/deepleaf/dataset/PlantVillage/val'

MODEL_SAVE_PATH = os.path.join(BASE_DIR, "ml", "models", "vgg19_final.keras")
LABELS_PATH = '/mnt/c/project/deepleaf/ml/models/class_labels.json'

IMG_SIZE = (224, 224)
BATCH_SIZE = 4  
EPOCHS = 10
NUM_CLASSES = 38

print("🚀 Starting DeepLeaf VGG19 Full Training...")

 
class_names = sorted(os.listdir(TRAIN_DIR))
print(f"✅ Found {len(class_names)} classes")

with open(LABELS_PATH, "w") as f:
    json.dump(class_names, f)
print(f"✅ Class labels saved")
 
train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2,
    shear_range=0.2
)

val_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="sparse",
    shuffle=True
)

val_generator = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="sparse",
    shuffle=False
)

print(f"✅ Train samples: {train_generator.samples}")
print(f"✅ Val samples: {val_generator.samples}")

 
class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(train_generator.classes),
    y=train_generator.classes
)
class_weight_dict = {i: weight for i, weight in enumerate(class_weights)}

print("✅ Class weights applied for imbalance handling")
 
base_model = VGG19(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False  # Freeze base

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(256, activation="relu")(x)
x = Dropout(0.5)(x)
x = Dense(NUM_CLASSES, activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=x)

model.compile(
    optimizer=Adam(learning_rate=0.0001),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

print("✅ VGG19 model built and compiled!")
 
checkpoint = ModelCheckpoint(
    MODEL_SAVE_PATH,
    monitor="val_accuracy",
    save_best_only=True,
    mode="max",
    verbose=1
)

early_stop = EarlyStopping(
    monitor="val_loss", 
    patience=3, 
    restore_best_weights=True
)

reduce_lr = ReduceLROnPlateau(
    monitor="val_loss", 
    factor=0.5, 
    patience=2, 
    min_lr=1e-6,
    verbose=1
)

print("🚀 Training started (full dataset, 10 epochs).... This will take time on CPU. Please be patient.")

history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=val_generator,
    class_weight=class_weight_dict,
    callbacks=[checkpoint, early_stop, reduce_lr],
    verbose=1
)

print("✅ Training completed successfully!")
 
model.save(os.path.join(BASE_DIR, "ml", "models", "vgg19_last.keras"))
print(f"✅ Final model saved at {MODEL_SAVE_PATH}")
 
import pickle
with open(os.path.join(BASE_DIR, "ml", "models", "training_history.pkl"), "wb") as f:
    pickle.dump(history.history, f)
print("✅ Training history saved!")
