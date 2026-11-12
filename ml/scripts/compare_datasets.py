import os
import csv

BASE_DIR = r"C:\project\deepleaf"

PLANTVILLAGE_TRAIN = os.path.join(
    BASE_DIR,
    "dataset",
    "PlantVillage",
    "train"
)

LEAVESBANK_TRAINING = os.path.join(
    BASE_DIR,
    "dataset",
    "LeavesBank_Training",
    "train"
)

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "models",
    "dataset_class_comparison.csv"
)

plantvillage_classes = sorted(
    [
        d
        for d in os.listdir(PLANTVILLAGE_TRAIN)
        if os.path.isdir(
            os.path.join(PLANTVILLAGE_TRAIN, d)
        )
    ]
)

leavesbank_classes = sorted(
    [
        d
        for d in os.listdir(LEAVESBANK_TRAINING)
        if os.path.isdir(
            os.path.join(LEAVESBANK_TRAINING, d)
        )
    ]
)

def normalize(text):
    text = str(text).lower()
    text = text.replace("___", " ")
    text = text.replace("_", " ")
    text = text.replace(",", " ")
    text = text.replace("(", " ")
    text = text.replace(")", " ")
    text = text.replace("-", " ")
    return " ".join(text.split())

rows = []

for pv in plantvillage_classes:

    pv_normalized = normalize(pv)

    matches = []

    for lb in leavesbank_classes:

        lb_normalized = normalize(lb)

        if (
            pv_normalized in lb_normalized
            or lb_normalized in pv_normalized
        ):
            matches.append(lb)

    rows.append(
        {
            "plantvillage_class": pv,
            "possible_leavesbank_matches": " | ".join(matches)
        }
    )

with open(
    OUTPUT_PATH,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "plantvillage_class",
            "possible_leavesbank_matches"
        ]
    )

    writer.writeheader()
    writer.writerows(rows)

print("=" * 70)
print("DATASET CLASS COMPARISON")
print("=" * 70)

print(
    f"PlantVillage classes found: "
    f"{len(plantvillage_classes)}"
)

print(
    f"LeavesBank training classes found: "
    f"{len(leavesbank_classes)}"
)

print()

for row in rows:

    print(
        f"PlantVillage: "
        f"{row['plantvillage_class']}"
    )

    if row["possible_leavesbank_matches"]:

        print(
            f"  Possible match: "
            f"{row['possible_leavesbank_matches']}"
        )

    else:

        print(
            "  Possible match: NONE"
        )

print()

print(
    f"Comparison saved to: {OUTPUT_PATH}"
)

print("=" * 70)