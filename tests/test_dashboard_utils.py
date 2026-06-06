from pathlib import Path

import pandas as pd

from src.dashboard_utils import (
    format_currency,
    format_percent,
    generate_dashboard_summary,
    generate_store_insight,
    load_model_metrics,
    load_monthly_performance,
    prepare_feature_scatter_data,
    prepare_store_summary,
    translate_efficiency_class,
)


def sample_monthly() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "store_id": 1,
                "store_name": "Warszawa Centrum",
                "year": 2025,
                "month": 1,
                "monthly_revenue": 10000,
                "orders_count": 50,
                "avg_order_value": 200,
                "return_rate": 0.05,
                "discount_share": 0.08,
                "sales_per_employee": 500,
                "unique_customers": 45,
                "unique_products": 20,
                "performance_score": 0.80,
                "performance_class": "high_efficiency",
            },
            {
                "store_id": 1,
                "store_name": "Warszawa Centrum",
                "year": 2025,
                "month": 2,
                "monthly_revenue": 7000,
                "orders_count": 35,
                "avg_order_value": 200,
                "return_rate": 0.08,
                "discount_share": 0.12,
                "sales_per_employee": 350,
                "unique_customers": 31,
                "unique_products": 17,
                "performance_score": 0.30,
                "performance_class": "low_efficiency",
            },
            {
                "store_id": 2,
                "store_name": "Kraków Galeria",
                "year": 2025,
                "month": 1,
                "monthly_revenue": 9000,
                "orders_count": 45,
                "avg_order_value": 200,
                "return_rate": 0.04,
                "discount_share": 0.07,
                "sales_per_employee": 450,
                "unique_customers": 40,
                "unique_products": 18,
                "performance_score": 0.60,
                "performance_class": "medium_efficiency",
            },
        ]
    )


def sample_stores() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "store_id": 1,
                "store_name": "Warszawa Centrum",
                "city": "Warszawa",
                "region": "mazowieckie",
                "location_type": "high_street",
                "store_size": "large",
                "employee_count": 20,
            },
            {
                "store_id": 2,
                "store_name": "Kraków Galeria",
                "city": "Kraków",
                "region": "małopolskie",
                "location_type": "shopping_mall",
                "store_size": "large",
                "employee_count": 18,
            },
        ]
    )


def test_translate_efficiency_class() -> None:
    assert translate_efficiency_class("low_efficiency") == "niska efektywność"
    assert translate_efficiency_class("custom") == "custom"


def test_format_currency_and_percent() -> None:
    assert format_currency(12400) == "12 400 zł"
    assert format_percent(0.062) == "6.2%"


def test_prepare_store_summary_creates_expected_columns() -> None:
    summary = prepare_store_summary(sample_monthly(), sample_stores())
    assert {"avg_score", "dominant_class", "low_months", "high_months", "best_month", "worst_month"}.issubset(summary.columns)
    warsaw = summary[summary["store_name"] == "Warszawa Centrum"].iloc[0]
    assert warsaw["best_month"] == 1
    assert warsaw["worst_month"] == 2
    assert warsaw["best_period"] == "2025-01"
    assert warsaw["worst_period"] == "2025-02"


def test_generate_store_insight_contains_business_values() -> None:
    summary = prepare_store_summary(sample_monthly(), sample_stores())
    warsaw = summary[summary["store_name"] == "Warszawa Centrum"].iloc[0]
    insight = generate_store_insight("Warszawa Centrum", sample_monthly(), warsaw)
    assert "Warszawa Centrum" in insight
    assert "średnia sprzedaż na pracownika" in insight


def test_generate_dashboard_summary_mentions_best_store_and_k() -> None:
    summary = prepare_store_summary(sample_monthly(), sample_stores())
    metrics = {"best_k": 5, "f1_macro": 0.82}
    text = generate_dashboard_summary(summary, metrics)
    assert "Najwyższy średni wynik" in text
    assert "5" in text


def test_prepare_feature_scatter_data_adds_labels() -> None:
    frame = prepare_feature_scatter_data(sample_monthly())
    assert {"month_label", "period_label", "class_label"}.issubset(frame.columns)


def test_missing_dashboard_files_return_none(tmp_path: Path) -> None:
    assert load_monthly_performance(tmp_path) is None
    assert load_model_metrics(tmp_path) is None
