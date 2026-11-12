import os
import csv
import random
import shutil
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(r"C:\project\deepleaf")
SOURCE_DIR = BASE_DIR / "dataset" / "LeavesBank"
OUTPUT_DIR = BASE_DIR / "dataset" / "LeavesBank_Training"

TRAIN_DIR = OUTPUT_DIR / "train"
VAL_DIR = OUTPUT_DIR / "val"
TEST_DIR = OUTPUT_DIR / "test"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}

TRAIN_RATIO = 0.70
VAL_RATIO = 0.15
TEST_RATIO = 0.15

SEED = 42

random.seed(SEED)

if not SOURCE_DIR.exists():
    raise FileNotFoundError(
        f"LeavesBank dataset not found: {SOURCE_DIR}"
    )

classes = defaultdict(list)

for root, dirs, files in os.walk(SOURCE_DIR):

    root_path = Path(root)

    if root_path.name.lower() != "images":
        continue

    relative_parts = root_path.relative_to(SOURCE_DIR).parts

    if len(relative_parts) < 2:
        continue

    plant = relative_parts[0]
    disease = relative_parts[-2]

    if not plant or not disease:
        continue

    class_name = f"{plant} - {disease}"

    for file in files:

        file_path = root_path / file

        if file_path.suffix.lower() not in {
            ".jpg",
            ".jpeg",
            ".png"
        }:
            continue

        classes[class_name].append(
            str(file_path)
        )

print("=" * 65)
print("DEEPLEAF LEAVESBANK DATASET PREPARATION")
print("=" * 65)

print(f"Total classes found: {len(classes)}")

total_images = sum(
    len(images)
    for images in classes.values()
)

print(f"Total images found: {total_images}")
print()

if total_images == 0:
    raise RuntimeError(
        "No images found in LeavesBank dataset."
    )

if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)

TRAIN_DIR.mkdir(
    parents=True,
    exist_ok=True
)

VAL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

TEST_DIR.mkdir(
    parents=True,
    exist_ok=True
)

mapping_file = OUTPUT_DIR / "dataset_mapping.csv"

mapping_rows = []

for class_name in sorted(classes.keys()):

    images = classes[class_name]

    random.shuffle(images)

    total = len(images)

    if total == 1:
        train_images = images
        val_images = []
        test_images = []

    elif total == 2:
        train_images = images[:1]
        val_images = []
        test_images = images[1:]

    else:

        train_count = max(
            1,
            int(total * TRAIN_RATIO)
        )

        val_count = max(
            1,
            int(total * VAL_RATIO)
        )

        if train_count + val_count >= total:
            val_count = 1
            train_count = total - 2

        test_count = total - train_count - val_count

        if test_count < 1:
            test_count = 1
            train_count -= 1

        train_images = images[
            :train_count
        ]

        val_images = images[
            train_count:
            train_count + val_count
        ]

        test_images = images[
            train_count + val_count:
        ]

    safe_class_name = (
        class_name
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
        .replace("*", "_")
        .replace("?", "_")
        .replace('"', "_")
        .replace("<", "_")
        .replace(">", "_")
        .replace("|", "_")
    )

    train_class_dir = (
        TRAIN_DIR / safe_class_name
    )

    val_class_dir = (
        VAL_DIR / safe_class_name
    )

    test_class_dir = (
        TEST_DIR / safe_class_name
    )

    train_class_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    val_class_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    test_class_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    for index, source in enumerate(train_images):

        source_path = Path(source)

        destination = (
            train_class_dir /
            f"{index:06d}_{source_path.name}"
        )

        shutil.copy2(
            source_path,
            destination
        )

        mapping_rows.append({
            "split": "train",
            "class": class_name,
            "source": str(source_path),
            "destination": str(destination)
        })

    for index, source in enumerate(val_images):

        source_path = Path(source)

        destination = (
            val_class_dir /
            f"{index:06d}_{source_path.name}"
        )

        shutil.copy2(
            source_path,
            destination
        )

        mapping_rows.append({
            "split": "val",
            "class": class_name,
            "source": str(source_path),
            "destination": str(destination)
        })

    for index, source in enumerate(test_images):

        source_path = Path(source)

        destination = (
            test_class_dir /
            f"{index:06d}_{source_path.name}"
        )

        shutil.copy2(
            source_path,
            destination
        )

        mapping_rows.append({
            "split": "test",
            "class": class_name,
            "source": str(source_path),
            "destination": str(destination)
        })

    print(
        f"{class_name:<55}"
        f"{total:>7} images"
        f"  train={len(train_images):>5}"
        f"  val={len(val_images):>5}"
        f"  test={len(test_images):>5}"
    )

with open(
    mapping_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "split",
            "class",
            "source",
            "destination"
        ]
    )

    writer.writeheader()
    writer.writerows(mapping_rows)

print()
print("=" * 65)
print("DATASET PREPARATION COMPLETE")
print("=" * 65)
print(f"Classes: {len(classes)}")
print(f"Images: {total_images}")
print(f"Output: {OUTPUT_DIR}")
print(f"Mapping: {mapping_file}")
print("=" * 65)