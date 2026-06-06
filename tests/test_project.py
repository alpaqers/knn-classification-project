import sqlite3
from pathlib import Path

import pandas as pd
import pytest

from src import database
from src.aggregation import PERFORMANCE_CLASSES, build_store_monthly_performance
from src.config import REQUIRED_TABLES
from src.data_generator import generate_sample_data
from src.data_importer import import_csv_to_sqlite
from src.data_validator import ValidationError, validate_input_directory
from src.ml_pipeline import train_knn_model
from src.visualization import generate_plots


@pytest.fixture()
def generated_dir(tmp_path: Path) -> Path:
    input_dir = tmp_path / "input"
    generate_sample_data(input_dir)
    return input_dir


@pytest.fixture()
def imported_database(generated_dir: Path, tmp_path: Path) -> Path:
    database_path = tmp_path / "dw.sqlite"
    import_csv_to_sqlite(generated_dir, database_path, replace=True)
    return database_path


def test_generator_creates_required_store_count(generated_dir: Path) -> None:
    stores = pd.read_csv(generated_dir / "dim_store.csv")
    assert len(stores) == 8


def test_generator_creates_all_required_csv_files(generated_dir: Path) -> None:
    assert {path.stem for path in generated_dir.glob("*.csv")} == set(REQUIRED_TABLES)


def test_dim_date_contains_12_months_of_2025(generated_dir: Path) -> None:
    dim_date = pd.read_csv(generated_dir / "dim_date.csv")
    assert set(dim_date["month"]) == set(range(1, 13))
    assert set(dim_date["year"]) == {2025}


def test_validator_detects_missing_required_file(generated_dir: Path) -> None:
    (generated_dir / "dim_store.csv").unlink()
    with pytest.raises(ValidationError, match="Missing required CSV"):
        validate_input_directory(generated_dir)


def test_validator_detects_missing_required_column(generated_dir: Path) -> None:
    path = generated_dir / "dim_product.csv"
    frame = pd.read_csv(path).drop(columns=["base_price"])
    frame.to_csv(path, index=False)
    with pytest.raises(ValidationError, match="missing columns"):
        validate_input_directory(generated_dir)


def test_validator_detects_empty_file(generated_dir: Path) -> None:
    (generated_dir / "dim_customer.csv").write_text("", encoding="utf-8")
    with pytest.raises(ValidationError, match="empty"):
        validate_input_directory(generated_dir)


def test_validator_detects_duplicate_dimension_identifier(generated_dir: Path) -> None:
    path = generated_dir / "dim_store.csv"
    frame = pd.read_csv(path)
    frame.loc[1, "store_id"] = frame.loc[0, "store_id"]
    frame.to_csv(path, index=False)
    with pytest.raises(ValidationError, match="duplicate"):
        validate_input_directory(generated_dir)


def test_validator_detects_invalid_foreign_key(generated_dir: Path) -> None:
    path = generated_dir / "fact_sales.csv"
    frame = pd.read_csv(path)
    frame.loc[0, "store_id"] = 9999
    frame.to_csv(path, index=False)
    with pytest.raises(ValidationError, match="invalid foreign key"):
        validate_input_directory(generated_dir)


def test_validator_detects_invalid_is_returned(generated_dir: Path) -> None:
    path = generated_dir / "fact_sales.csv"
    frame = pd.read_csv(path)
    frame.loc[0, "is_returned"] = 2
    frame.to_csv(path, index=False)
    with pytest.raises(ValidationError, match="is_returned"):
        validate_input_directory(generated_dir)


def test_required_tables_are_created(imported_database: Path) -> None:
    with database.connect(imported_database) as connection:
        assert set(REQUIRED_TABLES).issubset(database.table_names(connection))


def test_fact_sales_is_not_empty_after_import(imported_database: Path) -> None:
    with sqlite3.connect(imported_database) as connection:
        count = connection.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0]
    assert count > 0


def test_replace_mode_overwrites_data(generated_dir: Path, tmp_path: Path) -> None:
    database_path = tmp_path / "replace.sqlite"
    first_summary = import_csv_to_sqlite(generated_dir, database_path, replace=True)
    second_summary = import_csv_to_sqlite(generated_dir, database_path, replace=True)
    with sqlite3.connect(database_path) as connection:
        count = connection.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0]
    assert count == first_summary["fact_sales"] == second_summary["fact_sales"]


def test_aggregation_returns_data(imported_database: Path) -> None:
    with database.connect(imported_database) as connection:
        performance = build_store_monthly_performance(connection)
    assert not performance.empty
    assert len(performance) >= 90


def test_performance_class_contains_expected_values(imported_database: Path) -> None:
    with database.connect(imported_database) as connection:
        performance = build_store_monthly_performance(connection)
    assert set(performance["performance_class"]).issubset(set(PERFORMANCE_CLASSES))


def test_ml_pipeline_returns_required_metrics(imported_database: Path, tmp_path: Path) -> None:
    with database.connect(imported_database) as connection:
        performance = build_store_monthly_performance(connection)
    metrics = train_knn_model(performance, tmp_path / "reports")
    assert {"accuracy", "precision", "recall", "f1_score"}.issubset(metrics)


def test_plots_are_saved(imported_database: Path, tmp_path: Path) -> None:
    with database.connect(imported_database) as connection:
        performance = build_store_monthly_performance(connection)
    metrics = train_knn_model(performance, tmp_path / "reports")
    paths = generate_plots(performance, metrics, tmp_path / "plots")
    assert paths
    assert all(path.exists() and path.stat().st_size > 0 for path in paths)
