from pathlib import Path

import pandas as pd

from src.config import ID_COLUMNS, REQUIRED_COLUMNS, REQUIRED_TABLES


class ValidationError(ValueError):
    pass


def _csv_path(input_dir: Path, table: str) -> Path:
    return input_dir / f"{table}.csv"


def load_csv_files(input_dir: Path) -> dict[str, pd.DataFrame]:
    input_dir = Path(input_dir)
    if not input_dir.exists():
        raise ValidationError(f"Input directory does not exist: {input_dir}")

    missing = [f"{table}.csv" for table in REQUIRED_TABLES if not _csv_path(input_dir, table).exists()]
    if missing:
        raise ValidationError(f"Missing required CSV files: {', '.join(missing)}")

    data: dict[str, pd.DataFrame] = {}
    for table in REQUIRED_TABLES:
        path = _csv_path(input_dir, table)
        try:
            frame = pd.read_csv(path)
        except pd.errors.EmptyDataError as exc:
            raise ValidationError(f"{path.name} is empty") from exc
        if frame.empty:
            raise ValidationError(f"{path.name} has no rows")
        missing_columns = [col for col in REQUIRED_COLUMNS[table] if col not in frame.columns]
        if missing_columns:
            raise ValidationError(f"{path.name} is missing columns: {', '.join(missing_columns)}")
        data[table] = frame[REQUIRED_COLUMNS[table]].copy()
    return data


def validate_dataframes(data: dict[str, pd.DataFrame]) -> None:
    for table, frame in data.items():
        id_col = ID_COLUMNS[table]
        if frame[id_col].isna().any():
            raise ValidationError(f"{table}.{id_col} contains empty values")
        if frame[id_col].duplicated().any():
            raise ValidationError(f"{table}.{id_col} contains duplicate identifiers")

    _validate_numeric(data)
    _validate_dates(data["dim_date"])
    _validate_foreign_keys(data)


def validate_input_directory(input_dir: Path) -> dict[str, pd.DataFrame]:
    data = load_csv_files(input_dir)
    validate_dataframes(data)
    return data


def _validate_numeric(data: dict[str, pd.DataFrame]) -> None:
    checks = [
        ("dim_store", "employee_count", lambda s: s > 0, "must be positive"),
        ("dim_product", "base_price", lambda s: s > 0, "must be positive"),
        ("fact_sales", "quantity", lambda s: s > 0, "must be positive"),
        ("fact_sales", "revenue", lambda s: s >= 0, "cannot be negative"),
        ("fact_sales", "discount_amount", lambda s: s >= 0, "cannot be negative"),
    ]
    for table, column, predicate, message in checks:
        values = pd.to_numeric(data[table][column], errors="coerce")
        if values.isna().any() or not predicate(values).all():
            raise ValidationError(f"{table}.{column} {message}")

    returned = pd.to_numeric(data["fact_sales"]["is_returned"], errors="coerce")
    if returned.isna().any() or not returned.isin([0, 1]).all():
        raise ValidationError("fact_sales.is_returned must contain only 0 or 1")


def _validate_dates(dim_date: pd.DataFrame) -> None:
    parsed = pd.to_datetime(dim_date["date"], errors="coerce")
    if parsed.isna().any():
        raise ValidationError("dim_date.date contains invalid dates")

    numeric_columns = ["day", "month", "quarter", "year"]
    numeric = {}
    for column in numeric_columns:
        values = pd.to_numeric(dim_date[column], errors="coerce")
        if values.isna().any():
            raise ValidationError(f"dim_date.{column} contains invalid numeric values")
        numeric[column] = values.astype(int)

    if not numeric["day"].between(1, 31).all():
        raise ValidationError("dim_date.day must be between 1 and 31")
    if not numeric["month"].between(1, 12).all():
        raise ValidationError("dim_date.month must be between 1 and 12")
    if not numeric["quarter"].between(1, 4).all():
        raise ValidationError("dim_date.quarter must be between 1 and 4")

    years = pd.to_numeric(dim_date["year"], errors="coerce")
    if years.isna().any():
        raise ValidationError("dim_date.year contains invalid numeric values")

    if not (parsed.dt.day.to_numpy() == numeric["day"].to_numpy()).all():
        raise ValidationError("dim_date.day must match dim_date.date")
    if not (parsed.dt.month.to_numpy() == numeric["month"].to_numpy()).all():
        raise ValidationError("dim_date.month must match dim_date.date")
    if not (parsed.dt.year.to_numpy() == numeric["year"].to_numpy()).all():
        raise ValidationError("dim_date.year must match dim_date.date")

    expected_quarter = ((numeric["month"] - 1) // 3 + 1).astype(int)
    if not (expected_quarter.to_numpy() == numeric["quarter"].to_numpy()).all():
        raise ValidationError("dim_date.quarter must match dim_date.month")


def _validate_foreign_keys(data: dict[str, pd.DataFrame]) -> None:
    fact = data["fact_sales"]
    relationships = [
        ("store_id", "dim_store"),
        ("product_id", "dim_product"),
        ("customer_id", "dim_customer"),
        ("date_id", "dim_date"),
    ]
    for column, dimension in relationships:
        valid_ids = set(data[dimension][column])
        invalid = fact.loc[~fact[column].isin(valid_ids), column]
        if not invalid.empty:
            sample = invalid.iloc[0]
            raise ValidationError(f"fact_sales.{column} contains invalid foreign key: {sample}")
