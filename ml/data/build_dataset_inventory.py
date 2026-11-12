from pathlib import Path
import csv
from collections import Counter

root = Path("dataset")
out = Path("ml/data/all_datasets_inventory.csv")
ext = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

counts = Counter()
total = 0

out.parent.mkdir(parents=True, exist_ok=True)

with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["image_path", "source", "source_label"])

    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in ext:
            continue

        if p.is_relative_to(root / "17C67DHC" / "plant data"):
            relative = p.relative_to(root / "17C67DHC" / "plant data")
            source = "17C67DHC"
            label = relative.parts[0] if len(relative.parts) > 1 else ""
        else:
            source = "existing"
            label = p.parent.name

        writer.writerow([str(p.resolve()), source, label])
        counts[source] += 1
        total += 1

        if total % 5000 == 0:
            print(f"Indexed {total:,} images...", flush=True)

print("\nInventory complete.")
print(f"Total: {total:,}")
print(f"New dataset: {counts['17C67DHC']:,}")
print(f"Existing datasets: {counts['existing']:,}")
print(f"Saved to: {out.resolve()}")
