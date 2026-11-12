import os
import shutil

BASE_DIR = r"C:\project\deepleaf"

PLANTVILLAGE_DIR = os.path.join(
    BASE_DIR,
    "dataset",
    "PlantVillage"
)

LEAVESBANK_DIR = os.path.join(
    BASE_DIR,
    "dataset",
    "LeavesBank_Training"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "dataset",
    "Combined_Training"
)

CLASS_MERGES = {
    "Apple___Apple_scab": [
        ("plantvillage", "Apple___Apple_scab"),
        ("leavesbank", "Apple Leaf - scab")
    ],
    "Apple___Cedar_apple_rust": [
        ("plantvillage", "Apple___Cedar_apple_rust"),
        ("leavesbank", "Apple Leaf - cider_apple_rust")
    ],
    "Apple___healthy": [
        ("plantvillage", "Apple___healthy"),
        ("leavesbank", "Apple Leaf - healthy")
    ],
    "Peach___healthy": [
        ("plantvillage", "Peach___healthy"),
        ("leavesbank", "Peach Leaf - Healthy")
    ]
}

PLANTVILLAGE_MERGED = {
    item[1]
    for sources in CLASS_MERGES.values()
    for item in sources
    if item[0] == "plantvillage"
}

LEAVESBANK_MERGED = {
    item[1]
    for sources in CLASS_MERGES.values()
    for item in sources
    if item[0] == "leavesbank"
}

for split in ["train", "val", "test"]:
    os.makedirs(
        os.path.join(OUTPUT_DIR, split),
        exist_ok=True
    )

def copy_images(source_dir, destination_dir, prefix):
    if not os.path.exists(source_dir):
        return 0

    os.makedirs(
        destination_dir,
        exist_ok=True
    )

    count = 0

    for filename in os.listdir(source_dir):
        source_path = os.path.join(
            source_dir,
            filename
        )

        if not os.path.isfile(source_path):
            continue

        extension = os.path.splitext(
            filename
        )[1].lower()

        if extension not in [
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        ]:
            continue

        destination_filename = (
            f"{prefix}_{count:06d}{extension}"
        )

        destination_path = os.path.join(
            destination_dir,
            destination_filename
        )

        shutil.copy2(
            source_path,
            destination_path
        )

        count += 1

    return count

print("=" * 70)
print("DEEPLEAF COMBINED DATASET CREATION")
print("=" * 70)

total_images = 0

for split in ["train", "val", "test"]:

    print()
    print(f"Processing {split}...")

    pv_split = os.path.join(
        PLANTVILLAGE_DIR,
        split
    )

    lb_split = os.path.join(
        LEAVESBANK_DIR,
        split
    )

    if os.path.exists(pv_split):

        for class_name in sorted(
            os.listdir(pv_split)
        ):

            source = os.path.join(
                pv_split,
                class_name
            )

            if not os.path.isdir(source):
                continue

            if class_name in PLANTVILLAGE_MERGED:
                continue

            destination = os.path.join(
                OUTPUT_DIR,
                split,
                class_name
            )

            copied = copy_images(
                source,
                destination,
                "pv"
            )

            print(
                f"PlantVillage | {class_name}: {copied}"
            )

            total_images += copied

    if os.path.exists(lb_split):

        for class_name in sorted(
            os.listdir(lb_split)
        ):

            source = os.path.join(
                lb_split,
                class_name
            )

            if not os.path.isdir(source):
                continue

            if class_name in LEAVESBANK_MERGED:
                continue

            destination = os.path.join(
                OUTPUT_DIR,
                split,
                class_name
            )

            copied = copy_images(
                source,
                destination,
                "lb"
            )

            print(
                f"LeavesBank | {class_name}: {copied}"
            )

            total_images += copied

    if split in ["train", "val"]:

        for class_name, sources in CLASS_MERGES.items():

            destination = os.path.join(
                OUTPUT_DIR,
                split,
                class_name
            )

            class_total = 0

            for source_type, source_class in sources:

                if source_type == "plantvillage":

                    source_root = os.path.join(
                        PLANTVILLAGE_DIR,
                        split,
                        source_class
                    )

                    prefix = "pv"

                else:

                    source_root = os.path.join(
                        LEAVESBANK_DIR,
                        split,
                        source_class
                    )

                    prefix = "lb"

                copied = copy_images(
                    source_root,
                    destination,
                    prefix
                )

                class_total += copied

            print(
                f"Merged | {class_name}: {class_total}"
            )

            total_images += class_total

print()
print("=" * 70)
print("COMBINED DATASET COMPLETE")
print("=" * 70)
print(f"Output: {OUTPUT_DIR}")
print(f"Total images copied: {total_images}")
print("=" * 70)