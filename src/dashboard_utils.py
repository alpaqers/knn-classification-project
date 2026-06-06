import json
from pathlib import Path

import pandas as pd

from src.config import OUTPUT_DIR


CLASS_LABELS = {
    "low_efficiency": "niska efektywność",
    "medium_efficiency": "średnia efektywność",
    "high_efficiency": "wysoka efektywność",
}

MONTH_LABELS = {
    1: "styczeń",
    2: "luty",
    3: "marzec",
    4: "kwiecień",
    5: "maj",
    6: "czerwiec",
    7: "lipiec",
    8: "sierpień",
    9: "wrzesień",
    10: "październik",
    11: "listopad",
    12: "grudzień",
}


def translate_efficiency_class(value: str) -> str:
    return CLASS_LABELS.get(value, value)


def format_currency(value: float) -> str:
    return f"{value:,.0f} zł".replace(",", " ")


def format_percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def format_score(value: float) -> str:
    return f"{value:.3f}"


def load_monthly_performance(output_dir: Path = OUTPUT_DIR) -> pd.DataFrame | None:
    return _load_csv_if_exists(Path(output_dir) / "store_monthly_performance.csv")


def load_store_summary(output_dir: Path = OUTPUT_DIR) -> pd.DataFrame | None:
    return _load_csv_if_exists(Path(output_dir) / "store_summary.csv")


def load_knn_results(output_dir: Path = OUTPUT_DIR) -> pd.DataFrame | None:
    return _load_csv_if_exists(Path(output_dir) / "knn_results.csv")


def load_model_metrics(output_dir: Path = OUTPUT_DIR) -> dict | None:
    path = Path(output_dir) / "model_metrics.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _load_csv_if_exists(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    return pd.read_csv(path)


def prepare_store_summary(monthly: pd.DataFrame, stores: pd.DataFrame) -> pd.DataFrame:
    class_counts = (
        monthly.pivot_table(
            index="store_id",
            columns="performance_class",
            values="month",
            aggfunc="count",
            fill_value=0,
        )
        .rename(
            columns={
                "low_efficiency": "low_months",
                "medium_efficiency": "medium_months",
                "high_efficiency": "high_months",
            }
        )
        .reset_index()
    )
    for column in ["low_months", "medium_months", "high_months"]:
        if column not in class_counts:
            class_counts[column] = 0

    base = (
        monthly.groupby(["store_id", "store_name"], as_index=False)
        .agg(
            avg_score=("performance_score", "mean"),
            dominant_class=("performance_class", _dominant_class),
            avg_revenue=("monthly_revenue", "mean"),
            avg_orders_count=("orders_count", "mean"),
            avg_return_rate=("return_rate", "mean"),
            avg_discount_share=("discount_share", "mean"),
            avg_sales_per_employee=("sales_per_employee", "mean"),
        )
        .merge(class_counts, on="store_id", how="left")
    )
    best = _best_worst_month(monthly, ascending=False, prefix="best")
    worst = _best_worst_month(monthly, ascending=True, prefix="worst")
    summary = base.merge(best, on="store_id", how="left").merge(worst, on="store_id", how="left")
    store_columns = ["store_id", "city", "region", "location_type", "store_size", "employee_count"]
    return stores[store_columns].merge(summary, on="store_id", how="right")


def prepare_feature_scatter_data(monthly: pd.DataFrame) -> pd.DataFrame:
    frame = monthly.copy()
    frame["month_label"] = frame["month"].map(MONTH_LABELS)
    frame["period_label"] = frame["year"].astype(str) + "-" + frame["month"].astype(int).astype(str).str.zfill(2)
    frame["class_label"] = frame["performance_class"].map(translate_efficiency_class)
    return frame


def generate_store_insight(store_name: str, monthly: pd.DataFrame, summary: pd.Series) -> str:
    dominant = translate_efficiency_class(str(summary["dominant_class"]))
    best_period = _summary_period(summary, "best")
    worst_period = _summary_period(summary, "worst")
    return (
        f"Oddział {store_name} najczęściej osiąga klasę {dominant}. "
        f"Najlepszy wynik uzyskał w okresie: {best_period}, a najsłabszy w okresie: {worst_period}. "
        f"Średni udział zwrotów wynosi {format_percent(float(summary['avg_return_rate']))}, "
        f"a średnia sprzedaż na pracownika wynosi {format_currency(float(summary['avg_sales_per_employee']))}."
    )


def generate_dashboard_summary(store_summary: pd.DataFrame, metrics: dict) -> str:
    best = store_summary.sort_values("avg_score", ascending=False).iloc[0]
    attention = store_summary.sort_values(["low_months", "avg_score"], ascending=[False, True]).iloc[0]
    return (
        f"Najwyższy średni wynik osiąga {best['store_name']} "
        f"({format_score(float(best['avg_score']))}). "
        f"Najwięcej miesięcy wymagających uwagi ma {attention['store_name']} "
        f"({int(attention['low_months'])}). "
        f"Najlepsze k modelu to {metrics.get('best_k')}, "
        f"a F1-score macro wynosi {metrics.get('f1_macro', metrics.get('f1_score', 0)):.3f}."
    )


def _dominant_class(values: pd.Series) -> str:
    return values.value_counts().idxmax()


def _best_worst_month(monthly: pd.DataFrame, ascending: bool, prefix: str) -> pd.DataFrame:
    ordered = monthly.sort_values(["store_id", "performance_score"], ascending=[True, ascending])
    result = ordered.groupby("store_id", as_index=False).first()[["store_id", "year", "month"]]
    result[f"{prefix}_period"] = result["year"].astype(str) + "-" + result["month"].astype(int).astype(str).str.zfill(2)
    return result.rename(columns={"year": f"{prefix}_year", "month": f"{prefix}_month"})


def _summary_period(summary: pd.Series, prefix: str) -> str:
    period_column = f"{prefix}_period"
    if period_column in summary and pd.notna(summary[period_column]):
        return str(summary[period_column])
    month_column = f"{prefix}_month"
    if month_column in summary and pd.notna(summary[month_column]):
        return MONTH_LABELS.get(int(summary[month_column]), str(summary[month_column]))
    return "brak danych"
