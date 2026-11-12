#!/usr/bin/env python3
"""
Create CNN vs VGG19 training graphs from Keras CSVLogger history files.

Run from project root:
  python ml/scripts/plot_cnn_vgg19.py

Or pass explicit history files:
  python ml/scripts/plot_cnn_vgg19.py --cnn ml/models/cnn_history.csv --vgg ml/models/vgg19_retrained_gpu_history.csv

Each history CSV should contain Keras columns such as:
  epoch, accuracy, val_accuracy, loss, val_loss

Outputs PNG graphs into ml/models/graphs/.
The script never loads, changes, or stops training/model files.
"""
import argparse
from pathlib import Path
import sys

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = ROOT / "ml" / "models"
OUT_DIR = MODEL_DIR / "graphs"

CNN_CANDIDATES = [
    MODEL_DIR / "cnn_training_history.csv",
    MODEL_DIR / "cnn_history.csv",
    MODEL_DIR / "cnn_disease_history.csv",
    MODEL_DIR / "training_history_cnn.csv",
    MODEL_DIR / "cnn_training_log.csv",
]
VGG_CANDIDATES = [
    MODEL_DIR / "vgg19_retrained_gpu_history.csv",
    MODEL_DIR / "vgg19_retrained_history.csv",
    MODEL_DIR / "vgg19_training_history.csv",
    MODEL_DIR / "training_history_vgg19.csv",
    MODEL_DIR / "vgg19_history.csv",
]

def find_history(explicit, candidates, label):
    if explicit:
        p = Path(explicit).expanduser()
        if not p.is_absolute():
            p = ROOT / p
        if not p.is_file():
            raise FileNotFoundError(f"{label} history file not found: {p}")
        return p
    for p in candidates:
        if p.is_file():
            return p
    return None

def load_history(path, label):
    df = pd.read_csv(path)
    # Remove whitespace from CSV column names, if present.
    df.columns = [str(c).strip() for c in df.columns]
    # A CSVLogger typically starts epochs at 0. Display epochs starting at 1.
    if "epoch" in df.columns:
        epochs = pd.to_numeric(df["epoch"], errors="coerce").fillna(range(len(df))).to_numpy() + 1
    else:
        epochs = range(1, len(df) + 1)
    required = {"accuracy", "val_accuracy", "loss", "val_loss"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"{label} history {path} is missing columns: {sorted(missing)}. "
            f"Found columns: {list(df.columns)}"
        )
    return {
        "label": label,
        "path": path,
        "epochs": epochs,
        "accuracy": pd.to_numeric(df["accuracy"], errors="coerce"),
        "val_accuracy": pd.to_numeric(df["val_accuracy"], errors="coerce"),
        "loss": pd.to_numeric(df["loss"], errors="coerce"),
        "val_loss": pd.to_numeric(df["val_loss"], errors="coerce"),
    }

def plot_curves(histories, metric, ylabel, title, filename):
    fig, ax = plt.subplots(figsize=(10, 6))
    has_data = False
    for h in histories:
        for key, style, suffix in [
            (metric, "-", "train"),
            ("val_" + metric, "--", "validation"),
        ]:
            series = h[key]
            if series.notna().any():
                ax.plot(
                    h["epochs"], series,
                    linestyle=style, marker="o", markersize=3,
                    label=f'{h["label"]} {suffix}',
                )
                has_data = True
    if not has_data:
        plt.close(fig)
        return
    ax.set_xlabel("Epoch")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / filename, dpi=160)
    plt.close(fig)
    print("Saved:", OUT_DIR / filename)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cnn", help="CNN Keras CSV history path")
    parser.add_argument("--vgg", help="VGG19 Keras CSV history path")
    args = parser.parse_args()

    cnn_path = find_history(args.cnn, CNN_CANDIDATES, "CNN")
    vgg_path = find_history(args.vgg, VGG_CANDIDATES, "VGG19")
    histories = []
    if cnn_path:
        histories.append(load_history(cnn_path, "CNN"))
    else:
        print("CNN history CSV not found in common locations.")
    if vgg_path:
        histories.append(load_history(vgg_path, "VGG19"))
    else:
        print("VGG19 history CSV not found yet (training may not have written one).")

    if not histories:
        print("\nNo usable CSV history files found.")
        print("Expected CSVLogger files with accuracy, val_accuracy, loss, val_loss.")
        print("Pass exact file paths using --cnn and --vgg.")
        sys.exit(2)

    print("\nLoaded histories:")
    for h in histories:
        val_acc = h["val_accuracy"].dropna()
        val_loss = h["val_loss"].dropna()
        print(f"- {h['label']}: {h['path']}")
        if not val_acc.empty:
            print(f"  Best validation accuracy: {val_acc.max() * 100:.2f}%")
        if not val_loss.empty:
            print(f"  Lowest validation loss: {val_loss.min():.4f}")

    plot_curves(
        histories, "accuracy", "Accuracy",
        "CNN vs VGG19 — Training and Validation Accuracy",
        "cnn_vs_vgg19_accuracy.png",
    )
    plot_curves(
        histories, "loss", "Loss",
        "CNN vs VGG19 — Training and Validation Loss",
        "cnn_vs_vgg19_loss.png",
    )

    # Compare each model's best validation accuracy only if both histories exist.
    if len(histories) >= 2:
        names, values = [], []
        for h in histories:
            val = h["val_accuracy"].dropna()
            if not val.empty:
                names.append(h["label"])
                values.append(float(val.max()) * 100)
        if values:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            fig, ax = plt.subplots(figsize=(7, 5))
            bars = ax.bar(names, values)
            ax.set_ylabel("Best validation accuracy (%)")
            ax.set_title("CNN vs VGG19 — Best Validation Accuracy")
            ax.set_ylim(0, 100)
            ax.grid(axis="y", alpha=0.3)
            for bar, val in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                        f"{val:.2f}%", ha="center", va="bottom")
            fig.tight_layout()
            out = OUT_DIR / "cnn_vs_vgg19_best_validation_accuracy.png"
            fig.savefig(out, dpi=160)
            plt.close(fig)
            print("Saved:", out)
    else:
        print("\nOnly one model history is available. The script plotted its curves;")
        print("to make the CNN vs VGG19 final comparison, provide both history CSVs.")

if __name__ == "__main__":
    main()
 