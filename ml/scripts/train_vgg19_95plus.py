import os
import json
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import VGG19
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

BASE_DIR = r"/mnt/c/project/deepleaf"

TRAIN_DIR = os.path.join(BASE_DIR, "dataset", "PlantVillage", "train")
VAL_DIR = os.path.join(BASE_DIR, "dataset", "PlantVillage", "val")
MODEL_DIR = os.path.join(BASE_DIR, "ml", "models")

MODEL_PATH = os.path.join(MODEL_DIR, "vgg19_95plus.keras")
LABELS_PATH = os.path.join(MODEL_DIR, "vgg19_95plus_labels.json")

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
INITIAL_EPOCHS = 7
FINE_TUNE_EPOCHS = 3

if not os.path.exists(TRAIN_DIR):
    raise FileNotFoundError(TRAIN_DIR)

if not os.path.exists(VAL_DIR):
    raise FileNotFoundError(VAL_DIR)

os.makedirs(MODEL_DIR, exist_ok=True)

train_data = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=True,
    seed=42
)

val_data = tf.keras.utils.image_dataset_from_directory(
    VAL_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int",
    shuffle=False
)

class_names = train_data.class_names
num_classes = len(class_names)

if num_classes != 38:
    raise ValueError(f"Expected 38 classes, but found {num_classes}")

AUTOTUNE = tf.data.AUTOTUNE

train_data = train_data.prefetch(AUTOTUNE)
val_data = val_data.prefetch(AUTOTUNE)

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.10),
    layers.RandomZoom(0.10),
    layers.RandomContrast(0.10)
])

base_model = VGG19(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

base_model.trainable = False

inputs = layers.Input(shape=(224, 224, 3))

x = data_augmentation(inputs)
x = tf.keras.applications.vgg19.preprocess_input(x)
x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.BatchNormalization()(x)
x = layers.Dense(512, activation="relu")(x)
x = layers.Dropout(0.5)(x)
outputs = layers.Dense(num_classes, activation="softmax")(x)

model = models.Model(
    inputs,
    outputs,
    name="DeepLeaf_VGG19"
)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

checkpoint = ModelCheckpoint(
    MODEL_PATH,
    monitor="val_accuracy",
    mode="max",
    save_best_only=True,
    verbose=1
)

early_stopping = EarlyStopping(
    monitor="val_accuracy",
    mode="max",
    patience=4,
    restore_best_weights=True,
    verbose=1
)

reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.3,
    patience=2,
    min_lr=1e-7,
    verbose=1
)

model.fit(
    train_data,
    validation_data=val_data,
    epochs=INITIAL_EPOCHS,
    callbacks=[checkpoint, early_stopping, reduce_lr]
)

base_model.trainable = True

for layer in base_model.layers:
    layer.trainable = False

for layer in base_model.layers:
    if layer.name.startswith("block5"):
        layer.trainable = True

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(
    train_data,
    validation_data=val_data,
    epochs=FINE_TUNE_EPOCHS,
    callbacks=[checkpoint, early_stopping, reduce_lr]
)

best_model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

best_model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

results = best_model.evaluate(
    val_data,
    verbose=1
)

loss = results[0]
accuracy = results[1]

with open(LABELS_PATH, "w", encoding="utf-8") as f:
    json.dump(class_names, f, indent=2)

print(f"VGG19 validation loss: {loss:.4f}")
print(f"VGG19 validation accuracy: {accuracy * 100:.2f}%")
print(f"Model saved: {MODEL_PATH}")
print(f"Labels saved: {LABELS_PATH}")
