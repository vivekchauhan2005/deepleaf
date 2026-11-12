import os
import kagglehub
 
base_path = kagglehub.dataset_download(
    "mohitsingh1804/plantvillage"
)

dataset_path = os.path.join(base_path, "PlantVillage")

train_path = os.path.join(dataset_path, "train")
val_path = os.path.join(dataset_path, "val")


def count_images(folder_path):
    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

    total = 0
    class_counts = {}

    for class_name in sorted(os.listdir(folder_path)):
        class_path = os.path.join(folder_path, class_name)

        if not os.path.isdir(class_path):
            continue

        count = 0

        for file_name in os.listdir(class_path):
            if file_name.lower().endswith(image_extensions):
                count += 1

        class_counts[class_name] = count
        total += count

    return class_counts, total
 
train_counts, train_total = count_images(train_path)
 
val_counts, val_total = count_images(val_path)


print("\n==============================")
print("DEEPLEAF DATASET INFORMATION")
print("==============================")

print("\nTRAIN DATA")
print("------------------------------")

for class_name, count in train_counts.items():
    print(f"{class_name}: {count}")

print("\nTotal training images:", train_total)
print("Total training classes:", len(train_counts))


print("\nVAL DATA")
print("------------------------------")

for class_name, count in val_counts.items():
    print(f"{class_name}: {count}")

print("\nTotal validation images:", val_total)
print("Total validation classes:", len(val_counts))


print("\n==============================")
print("TOTAL DATASET")
print("==============================")

print("Total images:", train_total + val_total)