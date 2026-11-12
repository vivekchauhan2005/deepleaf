import os
import json
import pickle
import numpy as np
import tensorflow as tf

from tensorflow.keras.applications import VGG19
from tensorflow.keras.applications.vgg19 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from sklearn.utils.class_weight import compute_class_weight

BASE_DIR = r"C:\project\deepleaf"

TRAIN_DIR = os.path.join(
    BASE_DIR,
    "dataset",
    "Combined_Training",
    "train"
)

VAL_DIR = os.path.join(
    BASE_DIR,
    "dataset",
    "Combined_Training",
    "val"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "ml",
    "models"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "combined_vgg19.keras"
)

LABELS_PATH = os.path.join(
    MODEL_DIR,
    "combined_class_labels.json"
)

HISTORY_PATH = os.path.join(
    MODEL_DIR,
    "combined_training_history.pkl"
)

IMG_SIZE = (224, 224)
BATCH_SIZE = 16

STAGE1_EPOCHS = 15
STAGE2_EPOCHS = 15

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

if not os.path.exists(TRAIN_DIR):
    raise FileNotFoundError(TRAIN_DIR)

if not os.path.exists(VAL_DIR):
    raise FileNotFoundError(VAL_DIR)

print("=" * 70)
print("DEEPLEAF COMBINED PLANTVILLAGE + LEAVESBANK VGG19 TRAINING")
print("=" * 70)

train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=20,
    width_shift_range=0.15,
    height_shift_range=0.15,
    zoom_range=0.15,
    shear_range=0.15,
    horizontal_flip=True,
    vertical_flip=True
)

val_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input
)

train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="sparse",
    shuffle=True,
    seed=42
)

val_generator = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="sparse",
    shuffle=False
)

class_names = list(
    train_generator.class_indices.keys()
)

num_classes = len(class_names)

print(f"Classes: {num_classes}")
print(f"Training images: {train_generator.samples}")
print(f"Validation images: {val_generator.samples}")

with open(
    LABELS_PATH,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        class_names,
        file,
        ensure_ascii=False,
        indent=2
    )

classes = np.unique(
    train_generator.classes
)

weights = compute_class_weight(
    class_weight="balanced",
    classes=classes,
    y=train_generator.classes
)

class_weight = {
    int(class_id): float(weight)
    for class_id, weight in zip(
        classes,
        weights
    )
}

base_model = VGG19(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

base_model.trainable = False

x = base_model.output

x = GlobalAveragePooling2D()(x)

x = Dense(
    512,
    activation="relu"
)(x)

x = Dropout(
    0.5
)(x)

x = Dense(
    256,
    activation="relu"
)(x)

x = Dropout(
    0.3
)(x)

output = Dense(
    num_classes,
    activation="softmax"
)(x)

model = Model(
    inputs=base_model.input,
    outputs=output
)

model.compile(
    optimizer=Adam(
        learning_rate=0.0001
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

checkpoint = ModelCheckpoint(
    MODEL_PATH,
    monitor="val_accuracy",
    save_best_only=True,
    mode="max",
    verbose=1
)

early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True,
    verbose=1
)

reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,
    patience=2,
    min_lr=1e-7,
    verbose=1
)

print()
print("=" * 70)
print("STAGE 1: FROZEN VGG19")
print("=" * 70)

history_stage1 = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=STAGE1_EPOCHS,
    class_weight=class_weight,
    callbacks=[
        checkpoint,
        early_stopping,
        reduce_lr
    ],
    verbose=1
)

print()
print("=" * 70)
print("STAGE 2: VGG19 FINE-TUNING")
print("=" * 70)

base_model.trainable = True

for layer in base_model.layers:
    layer.trainable = False

for layer in base_model.layers[-8:]:
    layer.trainable = True

model.compile(
    optimizer=Adam(
        learning_rate=0.00001
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

history_stage2 = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=STAGE2_EPOCHS,
    class_weight=class_weight,
    callbacks=[
        checkpoint,
        early_stopping,
        reduce_lr
    ],
    verbose=1
)

model.save(
    MODEL_PATH
)

combined_history = {}

for key in history_stage1.history:
    combined_history[key] = (
        history_stage1.history[key]
        + history_stage2.history[key]
    )

with open(
    HISTORY_PATH,
    "wb"
) as file:
    pickle.dump(
        combined_history,
        file
    )

best_val_accuracy = max(
    combined_history["val_accuracy"]
)

best_epoch = (
    combined_history["val_accuracy"].index(
        best_val_accuracy
    ) + 1
)

print()
print("=" * 70)
print("TRAINING COMPLETE")
print("=" * 70)
print(f"Classes: {num_classes}")
print(f"Training images: {train_generator.samples}")
print(f"Validation images: {val_generator.samples}")
print(f"Best validation accuracy: {best_val_accuracy * 100:.2f}%")
print(f"Best epoch: {best_epoch}")
print(f"Model: {MODEL_PATH}")
print(f"Labels: {LABELS_PATH}")
print(f"History: {HISTORY_PATH}")
print("=" * 70)