import csv
import json
from pathlib import Path

mapping_path = Path(r"C:\project\deepleaf\ml\models\leavesbank_mapping.csv")
labels_path = Path(r"C:\project\deepleaf\ml\models\class_labels.json")

with open(mapping_path, "r", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

with open(labels_path, "r", encoding="utf-8") as f:
    labels = json.load(f)

diseases = sorted(
    set(
        row["disease"].strip().lower()
        for row in rows
        if row["disease"].strip()
    )
)

print("=" * 65)
print("DEEPLEAF MODEL ↔ LEAVESBANK MATCH CHECK")
print("=" * 65)
print()
print(f"MODEL CLASSES: {len(labels)}")
print(f"DATASET DISEASE FOLDERS: {len(diseases)}")
print()

for index, label in enumerate(labels, 1):
    model_name = label.lower()
    model_name = model_name.replace("___", " ")
    model_name = model_name.replace("_", " ")
    model_name = model_name.replace("(", " ")
    model_name = model_name.replace(")", " ")
    model_name = " ".join(model_name.split())

    matches = []

    for disease in diseases:
        dataset_name = disease
        dataset_name = dataset_name.replace("_", " ")
        dataset_name = dataset_name.replace("(", " ")
        dataset_name = dataset_name.replace(")", " ")
        dataset_name = " ".join(dataset_name.split())

        if (
            model_name in dataset_name
            or dataset_name in model_name
        ):
            matches.append(disease)

    if matches:
        print(f"{index:02}. {label}")
        print("    MATCH:")
        for match in matches:
            print(f"    -> {match}")
    else:
        print(f"{index:02}. {label}")
        print("    NO MATCH")

print()
print("=" * 65)
print("MATCH CHECK COMPLETE")
print("=" * 65)