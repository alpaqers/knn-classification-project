from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.aggregation import FEATURE_COLUMNS


def train_knn_model(performance: pd.DataFrame, reports_dir: Path) -> dict:
    X = performance[FEATURE_COLUMNS]
    y = performance["performance_class"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    results = []
    best = None
    for k in [3, 5, 7, 9]:
        model = Pipeline(
            [
                ("scaler", StandardScaler()),
                ("knn", KNeighborsClassifier(n_neighbors=k)),
            ]
        )
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        metrics = {
            "k": k,
            "accuracy": float(accuracy_score(y_test, predictions)),
            "precision": float(precision_score(y_test, predictions, average="macro", zero_division=0)),
            "precision_macro": float(precision_score(y_test, predictions, average="macro", zero_division=0)),
            "recall": float(recall_score(y_test, predictions, average="macro", zero_division=0)),
            "recall_macro": float(recall_score(y_test, predictions, average="macro", zero_division=0)),
            "f1_score": float(f1_score(y_test, predictions, average="macro", zero_division=0)),
            "f1_macro": float(f1_score(y_test, predictions, average="macro", zero_division=0)),
        }
        results.append(metrics)
        if best is None or metrics["f1_score"] > best["metrics"]["f1_score"]:
            best = {"model": model, "metrics": metrics, "predictions": predictions}

    labels = sorted(y.unique())
    report = classification_report(y_test, best["predictions"], labels=labels, zero_division=0)
    matrix = confusion_matrix(y_test, best["predictions"], labels=labels)
    final_model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("knn", KNeighborsClassifier(n_neighbors=best["metrics"]["k"])),
        ]
    )
    final_model.fit(X, y)
    all_predictions = final_model.predict(X)
    output = {
        "best_k": best["metrics"]["k"],
        "accuracy": best["metrics"]["accuracy"],
        "precision": best["metrics"]["precision"],
        "precision_macro": best["metrics"]["precision_macro"],
        "recall": best["metrics"]["recall"],
        "recall_macro": best["metrics"]["recall_macro"],
        "f1_score": best["metrics"]["f1_score"],
        "f1_macro": best["metrics"]["f1_macro"],
        "k_results": results,
        "labels": labels,
        "confusion_matrix": matrix.tolist(),
        "classification_report": report,
        "all_predictions": all_predictions.tolist(),
    }
    write_model_results(output, reports_dir)
    return output


def write_model_results(metrics: dict, reports_dir: Path) -> None:
    reports_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Wyniki modelu kNN",
        "",
        f"Najlepsza wartość k: **{metrics['best_k']}**",
        "",
        "| Metryka | Wartość |",
        "|---|---:|",
        f"| Accuracy | {metrics['accuracy']:.4f} |",
        f"| Precision macro | {metrics['precision']:.4f} |",
        f"| Recall macro | {metrics['recall']:.4f} |",
        f"| F1-score macro | {metrics['f1_score']:.4f} |",
        "",
        "## Porównanie wartości k",
        "",
        "| k | Accuracy | Precision | Recall | F1-score |",
        "|---:|---:|---:|---:|---:|",
    ]
    for item in metrics["k_results"]:
        lines.append(
            f"| {item['k']} | {item['accuracy']:.4f} | {item['precision']:.4f} | "
            f"{item['recall']:.4f} | {item['f1_score']:.4f} |"
        )
    lines.extend(["", "## Classification report", "", "```text", metrics["classification_report"], "```"])
    (reports_dir / "model_results.md").write_text("\n".join(lines), encoding="utf-8")
