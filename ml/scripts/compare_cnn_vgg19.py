import os
import json
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# Works from the project root in Ubuntu/WSL or Windows.
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VAL_DIR = os.path.join(BASE_DIR, "dataset", "PlantVillage", "val")
CNN_PATH = os.path.join(BASE_DIR, "ml", "models", "cnn_disease.keras")
CNN_LABELS_PATH = os.path.join(BASE_DIR, "ml", "models", "cnn_class_labels.json")
VGG_PATH = os.path.join(BASE_DIR, "ml", "models", "vgg19_final.keras")
VGG_LABELS_PATH = os.path.join(BASE_DIR, "ml", "models", "class_labels.json")
RESULTS_DIR = os.path.join(BASE_DIR, "ml", "results")
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".bmp")

os.makedirs(RESULTS_DIR, exist_ok=True)

def load_labels(path):
    with open(path, "r", encoding="utf-8") as f:
        labels = json.load(f)
    if not isinstance(labels, list):
        raise ValueError(f"Expected a JSON list of class labels in {path}")
    return labels

def collect_validation_images():
    if not os.path.isdir(VAL_DIR):
        raise FileNotFoundError(f"Validation folder not found: {VAL_DIR}")
    paths, actual = [], []
    folder_classes = sorted(
        name for name in os.listdir(VAL_DIR)
        if os.path.isdir(os.path.join(VAL_DIR, name))
    )
    if not folder_classes:
        raise ValueError(f"No class folders found in {VAL_DIR}")
    for class_name in folder_classes:
        class_dir = os.path.join(VAL_DIR, class_name)
        for filename in sorted(os.listdir(class_dir)):
            if filename.lower().endswith(EXTENSIONS):
                paths.append(os.path.join(class_dir, filename))
                actual.append(class_name)
    if not paths:
        raise ValueError(f"No supported images found under {VAL_DIR}")
    return paths, actual, folder_classes

def preprocess_batch(paths):
    raw_images = []
    for path in paths:
        img = tf.keras.utils.load_img(path, target_size=IMAGE_SIZE, color_mode="rgb")
        raw_images.append(tf.keras.utils.img_to_array(img))
    # CNN has an internal Rescaling(1/255) layer, so give it raw 0..255 pixels.
    cnn_batch = np.asarray(raw_images, dtype=np.float32)
    # train_vgg19_final.py uses ImageDataGenerator(preprocessing_function=preprocess_input),
    # so apply the same VGG19 preprocessing externally here.
    vgg_batch = tf.keras.applications.vgg19.preprocess_input(
        np.asarray(raw_images, dtype=np.float32).copy()
    )
    return cnn_batch, vgg_batch

def confusion_matrix_numpy(y_true, y_pred, labels):
    index = {name: i for i, name in enumerate(labels)}
    cm = np.zeros((len(labels), len(labels)), dtype=np.int64)
    for actual, predicted in zip(y_true, y_pred):
        if actual in index and predicted in index:
            cm[index[actual], index[predicted]] += 1
    return cm

def metrics_numpy(y_true, y_pred, labels):
    cm = confusion_matrix_numpy(y_true, y_pred, labels)
    accuracy = sum(a == p for a, p in zip(y_true, y_pred)) / max(1, len(y_true))
    per_class = []
    for i in range(len(labels)):
        tp = cm[i, i]
        fp = cm[:, i].sum() - tp
        fn = cm[i, :].sum() - tp
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        per_class.append((precision, recall, f1))
    macro_precision = float(np.mean([m[0] for m in per_class]))
    macro_recall = float(np.mean([m[1] for m in per_class]))
    macro_f1 = float(np.mean([m[2] for m in per_class]))
    return accuracy, macro_precision, macro_recall, macro_f1, cm

def evaluate_model(model, label_names, image_paths, actual_names, model_name, is_vgg=False):
    expected_count = model.output_shape[-1]
    if len(label_names) != expected_count:
        raise ValueError(
            f"{model_name}: model outputs {expected_count} classes but labels file has "
            f"{len(label_names)} labels."
        )

    y_true, y_pred, confidences = [], [], []
    total = len(image_paths)
    for start in range(0, total, BATCH_SIZE):
        batch_paths = image_paths[start:start + BATCH_SIZE]
        actual_batch = actual_names[start:start + BATCH_SIZE]
        cnn_batch, vgg_batch = preprocess_batch(batch_paths)
        inputs = vgg_batch if is_vgg else cnn_batch
        outputs = model.predict(inputs, verbose=0)
        indices = np.argmax(outputs, axis=1)
        for i, idx in enumerate(indices):
            y_true.append(actual_batch[i])
            y_pred.append(label_names[int(idx)])
            confidences.append(float(outputs[i][int(idx)]))
        done = min(start + len(batch_paths), total)
        print(f"{model_name}: processed {done}/{total} images")

    # Ensure labels actually correspond to the validation folder classes.
    unknown = sorted(set(y_true) - set(label_names))
    if unknown:
        raise ValueError(
            f"{model_name}: validation folder classes not present in its labels file: {unknown[:10]}. "
            "Check class-label order/names before trusting metrics."
        )

    accuracy, precision, recall, f1, cm = metrics_numpy(y_true, y_pred, label_names)
    return {
        "name": model_name,
        "y_true": y_true,
        "y_pred": y_pred,
        "confidence": np.asarray(confidences),
        "accuracy": float(accuracy),
        "macro_precision": float(precision),
        "macro_recall": float(recall),
        "macro_f1": float(f1),
        "labels": label_names,
        "confusion_matrix": cm,
    }

def main():
    print("Loading models...")
    cnn_model = tf.keras.models.load_model(CNN_PATH, compile=False)
    vgg_model = tf.keras.models.load_model(VGG_PATH, compile=False)
    cnn_labels = load_labels(CNN_LABELS_PATH)
    vgg_labels = load_labels(VGG_LABELS_PATH)
    image_paths, actual_names, folder_classes = collect_validation_images()

    print("=" * 72)
    print("CNN vs VGG19 FINAL — VALIDATION COMPARISON")
    print(f"Validation images: {len(image_paths)}")
    print(f"Validation classes: {len(folder_classes)}")
    print(f"Results directory: {RESULTS_DIR}")
    print("=" * 72)

    print("\nEvaluating CNN...")
    cnn = evaluate_model(cnn_model, cnn_labels, image_paths, actual_names, "CNN", is_vgg=False)
    print("\nEvaluating VGG19 final...")
    vgg = evaluate_model(vgg_model, vgg_labels, image_paths, actual_names, "VGG19", is_vgg=True)

    results = [cnn, vgg]
    metric_names = ["Accuracy", "Macro precision", "Macro recall", "Macro F1", "Mean confidence"]
    metric_values = {
        "CNN": [
            cnn["accuracy"], cnn["macro_precision"], cnn["macro_recall"],
            cnn["macro_f1"], float(np.mean(cnn["confidence"]))
        ],
        "VGG19": [
            vgg["accuracy"], vgg["macro_precision"], vgg["macro_recall"],
            vgg["macro_f1"], float(np.mean(vgg["confidence"]))
        ],
    }

    print("\n" + "=" * 72)
    print("FINAL RESULTS")
    print("=" * 72)
    for result in results:
        print(f"\n{result['name']}")
        print(f"Accuracy        : {result['accuracy'] * 100:.2f}%")
        print(f"Macro precision : {result['macro_precision'] * 100:.2f}%")
        print(f"Macro recall    : {result['macro_recall'] * 100:.2f}%")
        print(f"Macro F1        : {result['macro_f1'] * 100:.2f}%")
        print(f"Mean confidence : {np.mean(result['confidence']) * 100:.2f}%")
        cm = result["confusion_matrix"]
        report = {}
        for i, label in enumerate(result["labels"]):
            tp = int(cm[i, i]); fp = int(cm[:, i].sum() - tp); fn = int(cm[i, :].sum() - tp)
            p = tp / (tp + fp) if tp + fp else 0.0
            r = tp / (tp + fn) if tp + fn else 0.0
            f1 = 2 * p * r / (p + r) if p + r else 0.0
            report[label] = {"precision": p, "recall": r, "f1-score": f1, "support": int(cm[i, :].sum())}
        with open(os.path.join(RESULTS_DIR, f"{result['name'].lower()}_classification_report.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

    # Bar chart for overall metrics
    x = np.arange(len(metric_names))
    width = 0.36
    fig, ax = plt.subplots(figsize=(11, 6))
    bars1 = ax.bar(x - width / 2, [v * 100 for v in metric_values["CNN"]], width, label="CNN")
    bars2 = ax.bar(x + width / 2, [v * 100 for v in metric_values["VGG19"]], width, label="VGG19")
    ax.set_ylabel("Score (%)")
    ax.set_title("CNN vs VGG19 — PlantVillage Validation Set")
    ax.set_xticks(x)
    ax.set_xticklabels(metric_names, rotation=12, ha="right")
    ax.set_ylim(0, 105)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.legend()
    for bars in (bars1, bars2):
        ax.bar_label(bars, fmt="%.1f", padding=2, fontsize=8)
    fig.tight_layout()
    chart_path = os.path.join(RESULTS_DIR, "cnn_vs_vgg19_comparison.png")
    fig.savefig(chart_path, dpi=180, bbox_inches="tight")
    plt.close(fig)

    # Confusion matrices (one image per model; 38 classes can make these large)
    for result in results:
        cm = result["confusion_matrix"]
        fig, ax = plt.subplots(figsize=(18, 16))
        im = ax.imshow(cm, interpolation="nearest", aspect="auto")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        ax.set_xticks(np.arange(len(result["labels"])))
        ax.set_yticks(np.arange(len(result["labels"])))
        ax.set_xticklabels(result["labels"], rotation=90, fontsize=7)
        ax.set_yticklabels(result["labels"], fontsize=7)
        ax.set_xlabel("Predicted label")
        ax.set_ylabel("True label")
        ax.set_title(f"{result['name']} Confusion Matrix")
        fig.tight_layout()
        cm_path = os.path.join(RESULTS_DIR, f"{result['name'].lower()}_confusion_matrix.png")
        fig.savefig(cm_path, dpi=160, bbox_inches="tight")
        plt.close(fig)

    summary = {
        "validation_images": len(image_paths),
        "validation_classes": folder_classes,
        "metrics": {
            name: {metric: float(value) for metric, value in zip(metric_names, vals)}
            for name, vals in metric_values.items()
        },
        "note": "Mean confidence is not accuracy. Compare accuracy and macro F1; verify class-label mappings.",
        "chart": chart_path,
    }
    with open(os.path.join(RESULTS_DIR, "comparison_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\nSaved files:")
    print(f"  Overall graph: {chart_path}")
    print(f"  CNN confusion matrix: {os.path.join(RESULTS_DIR, 'cnn_confusion_matrix.png')}")
    print(f"  VGG19 confusion matrix: {os.path.join(RESULTS_DIR, 'vgg19_confusion_matrix.png')}")
    print(f"  Summary JSON: {os.path.join(RESULTS_DIR, 'comparison_summary.json')}")
    print("\nUse the model with higher validation accuracy and macro F1, provided class labels match.")
    print("Note: this compares CNN and VGG19 final, not VGG19 95plus.")

if __name__ == "__main__":
    main()
