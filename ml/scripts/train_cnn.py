import os
import json
import tensorflow as tf
from tensorflow.keras import layers, models

BASE_DIR = r"C:\project\deepleaf"

TRAIN_DIR = os.path.join(
    BASE_DIR,
    "dataset",
    "PlantVillage",
    "train"
)

VAL_DIR = os.path.join(
    BASE_DIR,
    "dataset",
    "PlantVillage",
    "val"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "ml",
    "models"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "cnn_disease.keras"
)

LABELS_PATH = os.path.join(
    MODEL_DIR,
    "cnn_class_labels.json"
)

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5

os.makedirs(MODEL_DIR, exist_ok=True)

print("=" * 70)
print("DeepLeaf Custom CNN Disease Training")
print("=" * 70)

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

print(f"Classes: {num_classes}")
 
normalization = layers.Rescaling(1.0 / 255)

model = models.Sequential([
    layers.Input(shape=(224, 224, 3)),
    normalization,

    layers.Conv2D(32, (3, 3), activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(128, (3, 3), activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(256, (3, 3), activation="relu"),
    layers.MaxPooling2D(),

    layers.Flatten(),

    layers.Dense(512, activation="relu"),
    layers.Dropout(0.5),

    layers.Dense(num_classes, activation="softmax")
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.0001
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

callbacks = [
    tf.keras.callbacks.ModelCheckpoint(
        MODEL_PATH,
        monitor="val_accuracy",
        save_best_only=True,
        mode="max"
    ),
    tf.keras.callbacks.EarlyStopping(
        monitor="val_accuracy",
        patience=4,
        mode="max",
        restore_best_weights=True
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=2,
        min_lr=0.000001
    )
]

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS,
    callbacks=callbacks
)

model.save(MODEL_PATH)

with open(
    LABELS_PATH,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        class_names,
        file,
        indent=2
    )

best_accuracy = max(
    history.history["val_accuracy"]
)

final_accuracy = history.history["val_accuracy"][-1]

print("=" * 70)
print("CNN TRAINING COMPLETE")
print("=" * 70)
print(f"Best validation accuracy : {best_accuracy * 100:.2f}%")
print(f"Final validation accuracy: {final_accuracy * 100:.2f}%")
print(f"Model saved              : {MODEL_PATH}")
print(f"Labels saved             : {LABELS_PATH}")
print("=" * 70)