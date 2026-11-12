#!/usr/bin/env python3
"""
DeepLeaf VGG19 retraining for a 4 GB GPU (for example, RTX 3050).

Expected layout:
  dataset/PlantVillage/train/<class>/*
  dataset/PlantVillage/val/<class>/*

Run from project root:
  source ml/.venv/bin/activate
  python ml/scripts/retrain_vgg19_gpu.py

This writes to new filenames and does not overwrite vgg19_final.keras.
VGG19 preprocessing is applied to both training and validation batches.
Mixed precision is enabled only when TensorFlow detects a GPU.
"""
import json
import os
import random
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.applications import VGG19
from tensorflow.keras.applications.vgg19 import preprocess_input
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau,
    CSVLogger,
)
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.utils.class_weight import compute_class_weight

SEED = 42
IMG_SIZE = (224, 224)
BATCH_SIZE = 4
HEAD_EPOCHS = 8
FINETUNE_EPOCHS = 12
FINE_TUNE_LAST_LAYERS = 4

ROOT = Path(__file__).resolve().parents[2]
TRAIN_DIR = ROOT / "dataset" / "PlantVillage" / "train"
VAL_DIR = ROOT / "dataset" / "PlantVillage" / "val"
MODEL_DIR = ROOT / "ml" / "models"
MODEL_PATH = MODEL_DIR / "vgg19_retrained_gpu_best.keras"
LABELS_PATH = MODEL_DIR / "vgg19_retrained_gpu_class_labels.json"
HISTORY_PATH = MODEL_DIR / "vgg19_retrained_gpu_history.csv"

os.environ.setdefault("TF_DETERMINISTIC_OPS", "1")
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

def main():
    if not TRAIN_DIR.is_dir() or not VAL_DIR.is_dir():
        raise FileNotFoundError(
            f"Dataset folders not found.\nExpected:\n  {TRAIN_DIR}\n  {VAL_DIR}"
        )
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    gpus = tf.config.list_physical_devices("GPU")
    print("TensorFlow:", tf.__version__, flush=True)
    print("Detected GPUs:", gpus if gpus else "NONE (CPU training)", flush=True)
    for gpu in gpus:
        try:
            tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as exc:
            print("Memory growth setting:", exc, flush=True)

    # Mixed precision is supported on RTX 3050. Keep the final output layer
    # in float32 for numerically stable softmax/loss calculations.
    if gpus:
        tf.keras.mixed_precision.set_global_policy("mixed_float16")
        print("Mixed precision policy: mixed_float16", flush=True)
    else:
        tf.keras.mixed_precision.set_global_policy("float32")
        print("Mixed precision policy: float32", flush=True)

    print("Training directory:", TRAIN_DIR, flush=True)
    print("Validation directory:", VAL_DIR, flush=True)
    print("Batch size:", BATCH_SIZE, flush=True)
    print("New output model:", MODEL_PATH, flush=True)

    train_aug = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        rotation_range=12,
        width_shift_range=0.08,
        height_shift_range=0.08,
        zoom_range=0.12,
        horizontal_flip=True,
        fill_mode="nearest",
    )
    val_aug = ImageDataGenerator(preprocessing_function=preprocess_input)

    train_gen = train_aug.flow_from_directory(
        str(TRAIN_DIR),
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="sparse",
        shuffle=True,
        seed=SEED,
    )
    val_gen = val_aug.flow_from_directory(
        str(VAL_DIR),
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="sparse",
        shuffle=False,
    )

    if train_gen.class_indices != val_gen.class_indices:
        raise ValueError("Train and validation class mappings do not match.")

    class_count = len(train_gen.class_indices)
    if class_count < 2:
        raise ValueError(f"Only {class_count} class(es) found; check dataset folders.")

    index_to_class = {idx: name for name, idx in train_gen.class_indices.items()}
    class_names = [index_to_class[i] for i in range(class_count)]
    with open(LABELS_PATH, "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=2, ensure_ascii=False)

    classes = np.unique(train_gen.classes)
    weights = compute_class_weight(
        class_weight="balanced",
        classes=classes,
        y=train_gen.classes,
    )
    class_weight = {int(c): float(w) for c, w in zip(classes, weights)}

    print(f"Classes: {class_count}", flush=True)
    print(f"Training images: {train_gen.samples}", flush=True)
    print(f"Validation images: {val_gen.samples}", flush=True)
    print("Label file:", LABELS_PATH, flush=True)

    backbone = VGG19(
        include_top=False,
        weights="imagenet",
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
    )
    backbone.trainable = False

    x = GlobalAveragePooling2D(name="global_average_pooling")(backbone.output)
    x = Dense(256, activation="relu", name="classifier_dense")(x)
    x = Dropout(0.4, name="classifier_dropout")(x)
    outputs = Dense(
        class_count, activation="softmax", dtype="float32", name="predictions"
    )(x)
    model = Model(backbone.input, outputs, name="DeepLeaf_VGG19_GPU_Retrain")

    model.compile(
        optimizer=Adam(learning_rate=1e-4),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    callbacks = [
        ModelCheckpoint(
            str(MODEL_PATH), monitor="val_accuracy", mode="max",
            save_best_only=True, verbose=1,
        ),
        EarlyStopping(
            monitor="val_loss", patience=3,
            restore_best_weights=True, verbose=1,
        ),
        ReduceLROnPlateau(
            monitor="val_loss", factor=0.3, patience=2,
            min_lr=1e-7, verbose=1,
        ),
        CSVLogger(str(HISTORY_PATH), append=False),
    ]

    print("\nPHASE 1: training classifier head", flush=True)
    model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=HEAD_EPOCHS,
        class_weight=class_weight,
        callbacks=callbacks,
        verbose=1,
    )

    print("\nPHASE 2: fine-tuning final VGG19 layers", flush=True)
    backbone.trainable = True
    for layer in backbone.layers[:-FINE_TUNE_LAST_LAYERS]:
        layer.trainable = False
    model.compile(
        optimizer=Adam(learning_rate=1e-5),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=FINETUNE_EPOCHS,
        class_weight=class_weight,
        callbacks=callbacks,
        verbose=1,
    )

    best_model = tf.keras.models.load_model(MODEL_PATH)
    val_gen.reset()
    loss, accuracy = best_model.evaluate(val_gen, verbose=1)
    print("\nTRAINING FINISHED", flush=True)
    print("Best checkpoint:", MODEL_PATH, flush=True)
    print("Labels:", LABELS_PATH, flush=True)
    print("History:", HISTORY_PATH, flush=True)
    print(f"Validation loss: {loss:.4f}", flush=True)
    print(f"Validation accuracy: {accuracy * 100:.2f}%", flush=True)
    print("Existing vgg19_final.keras was not overwritten.", flush=True)
    print("Prediction service must use this matching labels file and VGG19 preprocessing.", flush=True)

if __name__ == "__main__":
    main()
