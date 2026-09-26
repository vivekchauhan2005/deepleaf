import os
import csv
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.vgg19 import preprocess_input

BASE_DIR = r"/mnt/c/project/deepleaf"

DISEASE_MODEL_PATH = os.path.join(BASE_DIR, "ml", "models", "vgg19_95plus.keras")
CNN_MODEL_PATH = os.path.join(BASE_DIR, "ml", "models", "cnn_disease.keras")
LABELS_PATH = os.path.join(BASE_DIR, "ml", "models", "class_labels.json")
CNN_LABELS_PATH = os.path.join(BASE_DIR, "ml", "models", "cnn_class_labels.json")
LEAF_CHECKER_PATH = os.path.join(BASE_DIR, "ml", "models", "leaf_checker.keras")
MAPPING_PATH = os.path.join(BASE_DIR, "ml", "models", "leavesbank_mapping.csv")

gpus = tf.config.list_physical_devices("GPU")

if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print("GPU memory growth enabled")
    except RuntimeError as e:
        print("GPU memory configuration warning:", e)
else:
    print("No GPU detected. Using CPU.")

print("Loading DeepLeaf models...")

for path in [
    DISEASE_MODEL_PATH,
    CNN_MODEL_PATH,
    LABELS_PATH,
    CNN_LABELS_PATH,
    LEAF_CHECKER_PATH,
    MAPPING_PATH
]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required file not found: {path}")

vgg19_model = tf.keras.models.load_model(
    DISEASE_MODEL_PATH,
    compile=False
)

cnn_model = tf.keras.models.load_model(
    CNN_MODEL_PATH,
    compile=False
)

leaf_checker = tf.keras.models.load_model(
    LEAF_CHECKER_PATH,
    custom_objects={
        "preprocess_input": preprocess_input
    },
    compile=False,
    safe_mode=False
)

with open(
    LABELS_PATH,
    "r",
    encoding="utf-8"
) as file:
    class_names = json.load(file)

with open(
    CNN_LABELS_PATH,
    "r",
    encoding="utf-8"
) as file:
    cnn_class_names = json.load(file)

with open(
    MAPPING_PATH,
    "r",
    encoding="utf-8-sig"
) as file:
    leavesbank_rows = list(csv.DictReader(file))

print(f"Loaded {len(class_names)} VGG19 disease classes")
print(f"Loaded {len(cnn_class_names)} CNN disease classes")
print(f"Loaded {len(leavesbank_rows)} LeavesBank mappings")
print("Leaf checker loaded successfully!")
print("VGG19 model loaded successfully!")
print("CNN model loaded successfully!")


def normalize(text):
    text = str(text).lower()
    text = text.replace("___", " ")
    text = text.replace("_", " ")
    text = text.replace("(", " ")
    text = text.replace(")", " ")
    text = text.replace(",", " ")
    return " ".join(text.split())


def plant_matches(model_plant, dataset_plant):

    a = normalize(model_plant)
    b = normalize(dataset_plant)

    aliases = {
        "apple": ["apple leaf"],
        "peach": ["peach leaf"],
        "pepper bell": [
            "pepper leaf",
            "bell pepper leaf",
            "pepper bell leaf"
        ],
        "tomato": ["tomato leaf"],
        "potato": ["potato leaf"],
        "grape": ["grape leaf"],
        "corn maize": [
            "corn leaf",
            "maize leaf"
        ],
        "soybean": ["soybean leaf"],
        "strawberry": ["strawberry leaf"],
        "raspberry": ["raspberry leaf"],
        "blueberry": ["blueberry leaf"],
        "squash": ["squash leaf"]
    }

    if a == b:
        return True

    if a in b:
        return True

    if b in a:
        return True

    for alias in aliases.get(a, []):
        if normalize(alias) == b:
            return True

        if normalize(alias) in b:
            return True

    return False


def disease_matches(model_disease, dataset_disease):

    a = normalize(model_disease)
    b = normalize(dataset_disease)

    replacements = {
        "apple scab": ["scab"],
        "black rot": ["black rot"],
        "cedar apple rust": [
            "rust",
            "cider apple rust"
        ],
        "healthy": [
            "healthy",
            "healthy leaf"
        ],
        "powdery mildew": [
            "powdery mildew",
            "powdery_mildew"
        ],
        "bacterial spot": ["bacterial spot"],
        "leaf mold": ["leaf mold"],
        "septoria leaf spot": ["septoria leaf spot"],
        "target spot": ["target spot"],
        "yellow leaf curl virus": ["leaf curly virus"],
        "tomato mosaic virus": ["mosaic disease"],
        "leaf scorch": ["leaf scorch"],
        "common rust": ["rust"],
        "cercospora leaf spot gray leaf spot": [
            "cercospora leaf spot",
            "leaf spot"
        ]
    }

    if a == b:
        return True

    for alias in replacements.get(a, []):
        if normalize(alias) == b:
            return True

    return False


leavesbank_index = {}

for row in leavesbank_rows:

    plant = normalize(row.get("plant", ""))
    disease = normalize(row.get("disease", ""))
    path = row.get("path", "")

    if not plant or not disease or not path:
        continue

    if path.startswith("C:\\project\\deepleaf"):
        path = path.replace(
            "C:\\project\\deepleaf",
            "/mnt/c/project/deepleaf"
        ).replace("\\", "/")

    key = (plant, disease)

    if key not in leavesbank_index:
        leavesbank_index[key] = []

    if os.path.exists(path):
        leavesbank_index[key].append(path)

print(
    f"Fast LeavesBank index created: "
    f"{len(leavesbank_index)} classes"
)


def load_raw_image(image_path):

    image = tf.keras.utils.load_img(
        image_path,
        target_size=(224, 224)
    )

    image_array = tf.keras.utils.img_to_array(image)

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    return image_array.astype(np.float32)


def check_leaf(image_array):

    prediction = float(
        leaf_checker(
            image_array,
            training=False
        )[0][0]
    )

    if prediction >= 0.5:
        return {
            "is_leaf": False,
            "confidence": round(
                prediction * 100,
                2
            )
        }

    return {
        "is_leaf": True,
        "confidence": round(
            (1 - prediction) * 100,
            2
        )
    }


def find_dataset_evidence(predicted_class):

    parts = predicted_class.split("___")

    if len(parts) != 2:
        return {
            "available": False,
            "plant": None,
            "disease": None,
            "images": []
        }

    model_plant = parts[0]
    model_disease = parts[1]

    for (
        dataset_plant,
        dataset_disease
    ), paths in leavesbank_index.items():

        if not plant_matches(
            model_plant,
            dataset_plant
        ):
            continue

        if not disease_matches(
            model_disease,
            dataset_disease
        ):
            continue

        valid_images = paths[:5]

        if valid_images:
            return {
                "available": True,
                "plant": dataset_plant,
                "disease": dataset_disease,
                "images": valid_images
            }

    return {
        "available": False,
        "plant": None,
        "disease": None,
        "images": []
    }


def predict_image(image_path):

    image_data = load_raw_image(
        image_path
    )

    leaf_result = check_leaf(
        image_data
    )

    if not leaf_result["is_leaf"]:

        return {
            "is_leaf": False,
            "leaf_confidence": leaf_result["confidence"],
            "disease": None,
            "confidence": None,
            "class_index": None,
            "message": "Please enter a plant leaf image.",
            "dataset_evidence": {
                "available": False,
                "plant": None,
                "disease": None,
                "images": []
            },
            "comparison": {
                "cnn": {
                    "disease": None,
                    "confidence": None
                },
                "vgg19": {
                    "disease": None,
                    "confidence": None
                }
            }
        }

    cnn_predictions = cnn_model(
        image_data,
        training=False
    ).numpy()[0]

    vgg_predictions = vgg19_model(
        image_data,
        training=False
    ).numpy()[0]

    cnn_index = int(
        np.argmax(cnn_predictions)
    )

    vgg_index = int(
        np.argmax(vgg_predictions)
    )

    cnn_confidence = float(
        cnn_predictions[cnn_index] * 100
    )

    vgg_confidence = float(
        vgg_predictions[vgg_index] * 100
    )

    cnn_class = cnn_class_names[
        cnn_index
    ]

    vgg_class = class_names[
        vgg_index
    ]

    minimum_confidence = 70.0

    cnn_reliable = (
        cnn_confidence >= minimum_confidence
    )

    vgg_reliable = (
        vgg_confidence >= minimum_confidence
    )

    comparison = {
        "cnn": {
            "disease": cnn_class,
            "confidence": round(
                cnn_confidence,
                2
            )
        },
        "vgg19": {
            "disease": vgg_class,
            "confidence": round(
                vgg_confidence,
                2
            )
        }
    }

    if (
        cnn_reliable
        and
        vgg_reliable
        and
        cnn_class == vgg_class
    ):

        evidence = find_dataset_evidence(
            vgg_class
        )

        return {
            "is_leaf": True,
            "leaf_confidence": leaf_result["confidence"],
            "disease": vgg_class,
            "confidence": round(
                vgg_confidence,
                2
            ),
            "class_index": vgg_index,
            "message": "Both CNN and VGG19 identified the same disease.",
            "dataset_evidence": evidence,
            "comparison": comparison
        }

    elif vgg_reliable:

        evidence = find_dataset_evidence(
            vgg_class
        )

        return {
            "is_leaf": True,
            "leaf_confidence": leaf_result["confidence"],
            "disease": vgg_class,
            "confidence": round(
                vgg_confidence,
                2
            ),
            "class_index": vgg_index,
            "message": "Disease identified using VGG19.",
            "dataset_evidence": evidence,
            "comparison": comparison
        }

    elif cnn_reliable:

        evidence = find_dataset_evidence(
            cnn_class
        )

        return {
            "is_leaf": True,
            "leaf_confidence": leaf_result["confidence"],
            "disease": cnn_class,
            "confidence": round(
                cnn_confidence,
                2
            ),
            "class_index": cnn_index,
            "message": "Disease identified using CNN.",
            "dataset_evidence": evidence,
            "comparison": comparison
        }

    return {
        "is_leaf": True,
        "leaf_confidence": leaf_result["confidence"],
        "disease": None,
        "confidence": None,
        "class_index": None,
        "message": "Unable to identify the disease confidently. Please upload a clearer leaf image.",
        "dataset_evidence": {
            "available": False,
            "plant": None,
            "disease": None,
            "images": []
        },
        "comparison": comparison
    }