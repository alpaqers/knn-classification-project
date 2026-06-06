import json
import sqlite3
from pathlib import Path

import pandas as pd

from src.config import OUTPUT_DIR
from src.dashboard_utils import prepare_store_summary


def write_dashboard_outputs(
    performance: pd.DataFrame,
    metrics: dict,
    connection: sqlite3.Connection,
    output_dir: Path = OUTPUT_DIR,
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    stores = pd.read_sql_query(
        "SELECT store_id, store_name, city, region, location_type, store_size, employee_count FROM dim_store",
        connection,
    )
    store_summary = prepare_store_summary(performance, stores)

    monthly_path = output_dir / "store_monthly_performance.csv"
    summary_path = output_dir / "store_summary.csv"
    knn_path = output_dir / "knn_results.csv"
    metrics_path = output_dir / "model_metrics.json"

    performance.to_csv(monthly_path, index=False)
    store_summary.to_csv(summary_path, index=False)
    _knn_results_frame(metrics).to_csv(knn_path, index=False)
    metrics_path.write_text(json.dumps(_model_metrics_payload(metrics), ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "monthly": monthly_path,
        "summary": summary_path,
        "knn_results": knn_path,
        "model_metrics": metrics_path,
    }


def _knn_results_frame(metrics: dict) -> pd.DataFrame:
    rows = []
    for item in metrics["k_results"]:
        rows.append(
            {
                "k": item["k"],
                "accuracy": item["accuracy"],
                "precision_macro": item.get("precision_macro", item.get("precision")),
                "recall_macro": item.get("recall_macro", item.get("recall")),
                "f1_macro": item.get("f1_macro", item.get("f1_score")),
            }
        )
    return pd.DataFrame(rows)


def _model_metrics_payload(metrics: dict) -> dict:
    return {
        "best_k": metrics["best_k"],
        "accuracy": metrics["accuracy"],
        "precision_macro": metrics.get("precision_macro", metrics.get("precision")),
        "recall_macro": metrics.get("recall_macro", metrics.get("recall")),
        "f1_macro": metrics.get("f1_macro", metrics.get("f1_score")),
    }
