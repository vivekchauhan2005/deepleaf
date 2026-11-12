import csv
import json
from pathlib import Path

BASE = Path(r"C:\project\deepleaf")
MAPPING = BASE / "ml" / "models" / "leavesbank_mapping.csv"
LABELS = BASE / "ml" / "models" / "class_labels.json"

with open(MAPPING, "r", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

with open(LABELS, "r", encoding="utf-8") as f:
    labels = json.load(f)

def normalize(text):
    text = text.lower()
    text = text.replace("___", " ")
    text = text.replace("_", " ")
    text = text.replace("(", " ")
    text = text.replace(")", " ")
    text = text.replace(",", " ")
    text = " ".join(text.split())
    return text

plants = sorted(set(row["plant"] for row in rows if row["plant"]))
diseases = sorted(set(row["disease"] for row in rows if row["disease"]))

print("=" * 65)
print("DEEPLEAF EXACT MODEL ↔ LEAVESBANK MATCH")
print("=" * 65)
print()
print(f"MODEL CLASSES: {len(labels)}")
print()

for index, label in enumerate(labels, 1):

    parts = label.split("___")

    if len(parts) != 2:
        print(f"{index:02}. {label}")
        print("    INVALID MODEL LABEL")
        continue

    model_plant = normalize(parts[0])
    model_disease = normalize(parts[1])

    plant_matches = [
        plant for plant in plants
        if model_plant in normalize(plant)
        or normalize(plant) in model_plant
    ]

    exact_matches = []

    for row in rows:
        dataset_plant = normalize(row["plant"])
        dataset_disease = normalize(row["disease"])

        if not (
            model_plant in dataset_plant
            or dataset_plant in model_plant
        ):
            continue

        if (
            model_disease in dataset_disease
            or dataset_disease in model_disease
        ):
            exact_matches.append(row)

    print(f"{index:02}. {label}")

    if plant_matches:
        print("    PLANT:")
        for plant in plant_matches[:5]:
            print(f"    -> {plant}")
    else:
        print("    PLANT: NO MATCH")

    if exact_matches:
        unique = {}

        for row in exact_matches:
            key = (row["plant"], row["disease"])
            unique[key] = unique.get(key, 0) + 1

        print("    DATASET MATCH:")
        for (plant, disease), count in sorted(unique.items()):
            print(f"    -> {plant} | {disease} | {count} images")
    else:
        print("    DATASET MATCH: NO EXACT MATCH")

    print()

print("=" * 65)
print("EXACT MATCH CHECK COMPLETE")
print("=" * 65)