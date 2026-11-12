import os
import random
import shutil
from pathlib import Path

 

BASE = Path(r"C:\project\deepleaf")
LEAF_SOURCE = BASE / "dataset" / "LeavesBank"
NON_LEAF_SOURCE = BASE / "dataset" / "Caltech256"
OUTPUT = BASE / "dataset" / "LeafCheck"

SEED = 42
TOTAL_LEAF = 4000
TOTAL_NON_LEAF = 4000

TRAIN_RATIO = 0.80
VAL_RATIO = 0.10
TEST_RATIO = 0.10

random.seed(SEED)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}

 

NON_LEAF_CLASSES = [
    "003.backpack",
    "004.baseball-bat",
    "005.baseball-glove",
    "008.bathtub",
    "016.boom-box",
    "020.brain-101",
    "023.bulldozer",
    "026.cake",
    "027.calculator",
    "031.car-tire",
    "033.cd",
    "035.cereal-box",
    "045.computer-keyboard",
    "046.computer-monitor",
    "047.computer-mouse",
    "056.dog",
    "063.electric-guitar-101",
    "070.fire-extinguisher",
    "071.fire-hydrant",
    "072.fire-truck",
    "074.flashlight",
    "075.floppy-disk",
    "083.gas-pump",
    "101.head-phones",
    "117.ipod",
    "127.laptop-101",
    "130.license-plate",
    "139.megaphone",
    "142.microwave",
    "146.mountain-bike",
    "155.paperclip",
    "159.people",
    "162.picnic-table",
    "171.refrigerator",
    "174.rotary-phone",
    "180.screwdriver",
    "187.skyscraper",
    "193.soccer-ball",
    "195.soda-can",
    "202.steering-wheel",
    "220.toaster",
    "226.traffic-light",
    "227.treadmill",
    "232.t-shirt",
    "235.umbrella-101",
    "238.video-projector",
    "239.washing-machine",
    "240.watch-101",
    "244.wheelbarrow",
    "252.car-side-101",
    "253.faces-easy-101",
]

 

def find_images(folder):
    images = []

    for path in folder.rglob("*"):
        if path.is_file() and path.suffix in IMAGE_EXTENSIONS:
            images.append(path)

    return images


 

def clean_output():

    for split in ["train", "val", "test"]:
        for label in ["leaf", "non_leaf"]:

            folder = OUTPUT / split / label
            folder.mkdir(parents=True, exist_ok=True)

            for file in folder.iterdir():
                if file.is_file():
                    file.unlink()

 

def split_images(images):

    random.shuffle(images)

    train_end = int(len(images) * TRAIN_RATIO)
    val_end = train_end + int(len(images) * VAL_RATIO)

    return (
        images[:train_end],
        images[train_end:val_end],
        images[val_end:]
    )

 

def copy_images(images, label):

    train_images, val_images, test_images = split_images(images)

    splits = {
        "train": train_images,
        "val": val_images,
        "test": test_images,
    }

    copied = 0

    for split, split_images_list in splits.items():

        destination = OUTPUT / split / label
        destination.mkdir(parents=True, exist_ok=True)

        for index, source in enumerate(split_images_list):

            # Unique filename prevents collisions
            new_name = f"{label}_{index:05d}_{source.name}"

            destination_file = destination / new_name

            shutil.copy2(source, destination_file)

            copied += 1

    return {
        "train": len(train_images),
        "val": len(val_images),
        "test": len(test_images),
        "total": copied,
    }

 

print("=" * 65)
print("        DEEPLEAF LEAF CHECK DATASET PREPARATION")
print("=" * 65)

print("\nCleaning generated LeafCheck folders...")
clean_output()

 

print("\nSearching real leaf images in LeavesBank...")

all_leaf_images = find_images(LEAF_SOURCE)

print(f"Found leaf images: {len(all_leaf_images):,}")

if len(all_leaf_images) < TOTAL_LEAF:
    raise RuntimeError(
        f"Not enough leaf images. Required {TOTAL_LEAF}, "
        f"found {len(all_leaf_images)}."
    )

random.shuffle(all_leaf_images)

leaf_images = all_leaf_images[:TOTAL_LEAF]

print(f"Selected leaf images: {len(leaf_images):,}")

 

print("\nSearching selected real non-leaf classes...")

all_non_leaf_images = []

for class_name in NON_LEAF_CLASSES:

    class_folder = NON_LEAF_SOURCE / class_name

    if not class_folder.exists():
        print(f"WARNING: Missing class: {class_name}")
        continue

    class_images = find_images(class_folder)

    print(f"{class_name:<30} {len(class_images):>4}")

    all_non_leaf_images.extend(class_images)

print(f"\nTotal candidate non-leaf images: {len(all_non_leaf_images):,}")

if len(all_non_leaf_images) < TOTAL_NON_LEAF:
    raise RuntimeError(
        f"Not enough non-leaf images. Required {TOTAL_NON_LEAF}, "
        f"found {len(all_non_leaf_images)}."
    )

random.shuffle(all_non_leaf_images)

non_leaf_images = all_non_leaf_images[:TOTAL_NON_LEAF]

print(f"Selected non-leaf images: {len(non_leaf_images):,}")

 

print("\nCopying leaf images...")

leaf_result = copy_images(
    leaf_images,
    "leaf"
)

print("\nCopying non-leaf images...")

non_leaf_result = copy_images(
    non_leaf_images,
    "non_leaf"
)
 

print("\n" + "=" * 65)
print("              DATASET CREATED SUCCESSFULLY")
print("=" * 65)

print("\nLEAF")
print(f"Train : {leaf_result['train']}")
print(f"Val   : {leaf_result['val']}")
print(f"Test  : {leaf_result['test']}")
print(f"Total : {leaf_result['total']}")

print("\nNON-LEAF")
print(f"Train : {non_leaf_result['train']}")
print(f"Val   : {non_leaf_result['val']}")
print(f"Test  : {non_leaf_result['test']}")
print(f"Total : {non_leaf_result['total']}")

print("\nDataset location:")
print(OUTPUT)

print("\nFinal structure:")
print(r"LeafCheck")
print(r"├── train")
print(r"│   ├── leaf")
print(r"│   └── non_leaf")
print(r"├── val")
print(r"│   ├── leaf")
print(r"│   └── non_leaf")
print(r"└── test")
print(r"    ├── leaf")
print(r"    └── non_leaf")

print("\nDone!")