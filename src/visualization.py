import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from src.aggregation import FEATURE_COLUMNS


def generate_plots(performance: pd.DataFrame, metrics: dict, plots_dir: Path) -> list[Path]:
    plots_dir.mkdir(parents=True, exist_ok=True)
    paths = [
        _plot_class_counts(performance, plots_dir),
        _plot_revenue_by_class(performance, plots_dir),
        _plot_k_scores(metrics, plots_dir),
        _plot_confusion_matrix(metrics, plots_dir),
        _plot_pca_classes(performance, plots_dir),
        _plot_pca_predictions(performance, metrics, plots_dir),
    ]
    return paths


def _plot_class_counts(frame: pd.DataFrame, plots_dir: Path) -> Path:
    path = plots_dir / "class_counts.png"
    counts = frame["performance_class"].value_counts().sort_index()
    ax = counts.plot(kind="bar", color=["#c84c4c", "#d7a843", "#3f8f6b"])
    ax.set_title("Liczba rekordów w klasach efektywności")
    ax.set_xlabel("Klasa")
    ax.set_ylabel("Liczba rekordów")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def _plot_revenue_by_class(frame: pd.DataFrame, plots_dir: Path) -> Path:
    path = plots_dir / "avg_revenue_by_class.png"
    grouped = frame.groupby("performance_class")["monthly_revenue"].mean().sort_index()
    ax = grouped.plot(kind="bar", color="#4778a8")
    ax.set_title("Średni miesięczny przychód według klasy")
    ax.set_xlabel("Klasa")
    ax.set_ylabel("Średni przychód")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def _plot_k_scores(metrics: dict, plots_dir: Path) -> Path:
    path = plots_dir / "knn_k_comparison.png"
    results = pd.DataFrame(metrics["k_results"])
    plt.plot(results["k"], results["accuracy"], marker="o", label="accuracy")
    plt.plot(results["k"], results["f1_macro"], marker="o", label="F1 macro")
    plt.title("Porównanie jakości modelu dla różnych k")
    plt.xlabel("k")
    plt.ylabel("Wynik")
    plt.xticks(results["k"])
    plt.ylim(0, 1.05)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def _plot_confusion_matrix(metrics: dict, plots_dir: Path) -> Path:
    path = plots_dir / "confusion_matrix.png"
    matrix = metrics["confusion_matrix"]
    labels = metrics["labels"]
    fig, ax = plt.subplots()
    image = ax.imshow(matrix, cmap="Blues")
    ax.set_xticks(range(len(labels)), labels=labels, rotation=35, ha="right")
    ax.set_yticks(range(len(labels)), labels=labels)
    ax.set_xlabel("Predykcja")
    ax.set_ylabel("Rzeczywista klasa")
    ax.set_title("Macierz pomyłek")
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            ax.text(j, i, str(value), ha="center", va="center", color="black")
    fig.colorbar(image)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def _plot_pca_classes(frame: pd.DataFrame, plots_dir: Path) -> Path:
    path = plots_dir / "knn_pca_classification_space.png"
    pca_frame = _pca_frame(frame)
    colors = {"low_efficiency": "#c84c4c", "medium_efficiency": "#d7a843", "high_efficiency": "#3f8f6b"}
    for label, group in pca_frame.groupby("performance_class"):
        plt.scatter(group["PC1"], group["PC2"], label=label, alpha=0.8, color=colors[label])
    plt.title("Wizualizacja klas po PCA")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def _plot_pca_predictions(frame: pd.DataFrame, metrics: dict, plots_dir: Path) -> Path:
    path = plots_dir / "knn_pca_predictions.png"
    pca_frame = _pca_frame(frame)
    pca_frame["predicted_class"] = metrics.get("all_predictions", frame["performance_class"].tolist())
    pca_frame["is_correct"] = pca_frame["performance_class"] == pca_frame["predicted_class"]
    colors = {"low_efficiency": "#c84c4c", "medium_efficiency": "#d7a843", "high_efficiency": "#3f8f6b"}
    for label, group in pca_frame.groupby("predicted_class"):
        plt.scatter(group["PC1"], group["PC2"], label=label, alpha=0.75, color=colors[label])
    errors = pca_frame[~pca_frame["is_correct"]]
    if not errors.empty:
        plt.scatter(errors["PC1"], errors["PC2"], facecolors="none", edgecolors="black", linewidths=1.5, label="błędne")
    plt.title("Wizualizacja predykcji kNN po PCA")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def _pca_frame(frame: pd.DataFrame) -> pd.DataFrame:
    scaled = StandardScaler().fit_transform(frame[FEATURE_COLUMNS])
    points = PCA(n_components=2, random_state=42).fit_transform(scaled)
    pca_frame = pd.DataFrame(points, columns=["PC1", "PC2"])
    pca_frame["performance_class"] = frame["performance_class"].to_numpy()
    return pca_frame
