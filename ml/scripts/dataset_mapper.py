from pathlib import Path
import csv

BASE = Path(r"C:\project\deepleaf")
DATASET = BASE / "dataset" / "LeavesBank"
OUTPUT = BASE / "ml" / "models" / "leavesbank_mapping.csv"

EXTENSIONS = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}

def find_images():
    return [
        p for p in DATASET.rglob("*")
        if p.is_file() and p.suffix in EXTENSIONS
    ]

def get_info(path):
    parts = path.relative_to(DATASET).parts

    if "images" in parts:
        image_index = parts.index("images")

        plant = parts[0] if len(parts) > 0 else ""
        disease = parts[image_index - 1] if image_index > 0 else ""

        return plant, disease

    return "", ""

def main():
    images = find_images()

    print("=" * 65)
    print("DEEPLEAF LEAVESBANK DATASET MAPPER")
    print("=" * 65)
    print(f"Total images found: {len(images):,}")

    rows = []

    for image in images:
        plant, disease = get_info(image)

        rows.append({
            "image": image.name,
            "path": str(image),
            "plant": plant,
            "disease": disease
        })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(
        OUTPUT,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "image",
                "path",
                "plant",
                "disease"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)

    valid = sum(
        1 for row in rows
        if row["plant"] and row["disease"]
    )

    print(f"Mapped images: {valid:,}")
    print(f"Unmapped images: {len(rows) - valid:,}")
    print()
    print("Mapping saved:")
    print(OUTPUT)
    print()
    print("=" * 65)
    print("MAPPING COMPLETE")
    print("=" * 65)

if __name__ == "__main__":
    main()