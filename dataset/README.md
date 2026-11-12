# DeepLeaf Training Datasets Guide

This directory holds the raw image datasets utilized for training, fine-tuning, and evaluating the DeepLeaf convolutional neural networks and VGG-19 transfer learning models.

---

## 📊 Dataset Inventory & Size Breakdown

Across all training benchmarks, the dataset comprises **467,948 labeled images** spanning **31.76 GB**:

| Dataset Directory | Categories / Purpose | Image Count | Size | Public Source |
| :--- | :--- | :--- | :--- | :--- |
| **`PlantVillage/`** | 38 Classes (14 Crop Species: Apple, Tomato, Potato, Grape, Corn, etc.) | 54,305 files | 811 MB | [Kaggle: PlantVillage](https://www.kaggle.com/datasets/emmarex/plantdisease) |
| **`LeavesBank/`** | Extended agricultural foliage & disease categories | 120,077 files | 11.55 GB | Academic foliage repository |
| **`LeavesBank_Training/`** | Balanced training slice for high-accuracy VGG-19 fine-tuning | 60,028 files | 6.27 GB | Derived subset |
| **`Combined_Training/`** | Unified multi-source augmented training set | 112,493 files | 6.89 GB | Generated via `prepare_combined_dataset.py` |
| **`LeafCheck/`** | Non-leaf vs. leaf discrimination (negative controls) | 8,000 files | 544 MB | Generated via `prepare_leafcheck.py` |
| **`Caltech256/`** | General non-botanical negative classes | 61,214 files | 2.21 GB | [Caltech-256 Dataset](https://authors.library.caltech.edu/records/w76pk-sft80) |
| **`17C67DHC/`** | Multi-crop secondary field dataset | 51,831 files | 4.22 GB | Field research repository |

---

## ⚠️ Why Raw Images Are Not Committed to Git

GitHub imposes strict repository storage policies:
1. **Repository Limit**: GitHub recommends repositories stay under 1–5 GB and hard-blocks git pushes that exceed 5–10 GB. Pushing 31.76 GB (467,948 files) exceeds GitHub's limits and would cause permanent push rejection.
2. **Standard Machine Learning Practice**: In production AI and data science repositories, model training scripts (`ml/scripts/`) and model weights (`ml/models/` via Git LFS) are tracked in the repository, while multi-gigabyte raw image archives are hosted on dedicated data registries (such as Kaggle, Hugging Face Datasets, or Cloud Storage buckets).

---

## 🚀 How to Download & Set Up the Datasets

### 1. PlantVillage (Primary Dataset)
Using the Kaggle CLI:
```bash
kaggle datasets download -d emmarex/plantdisease -p dataset/PlantVillage --unzip
```

### 2. Run Dataset Preparation & Verification Scripts
The repository includes automated preparation scripts in `ml/scripts/`:
```bash
# Verify dataset structure and integrity
python ml/scripts/check_dataset.py

# Build the complete inventory index
python ml/data/build_dataset_inventory.py

# Prepare balanced combined datasets
python ml/scripts/prepare_combined_dataset.py
```
