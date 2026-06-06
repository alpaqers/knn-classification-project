import sqlite3
from pathlib import Path

import pandas as pd

from src.config import REQUIRED_TABLES


SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS dim_store (
    store_id INTEGER PRIMARY KEY,
    store_name TEXT NOT NULL,
    city TEXT NOT NULL,
    region TEXT NOT NULL,
    location_type TEXT NOT NULL,
    store_size TEXT NOT NULL,
    opening_date TEXT NOT NULL,
    employee_count INTEGER NOT NULL CHECK (employee_count > 0)
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    brand TEXT NOT NULL,
    gender TEXT NOT NULL,
    base_price REAL NOT NULL CHECK (base_price > 0)
);

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id INTEGER PRIMARY KEY,
    age_group TEXT NOT NULL,
    city TEXT NOT NULL,
    customer_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    day INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name TEXT NOT NULL,
    quarter INTEGER NOT NULL,
    year INTEGER NOT NULL,
    season TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_sales (
    sale_id INTEGER PRIMARY KEY,
    store_id INTEGER NOT NULL REFERENCES dim_store(store_id),
    product_id INTEGER NOT NULL REFERENCES dim_product(product_id),
    customer_id INTEGER NOT NULL REFERENCES dim_customer(customer_id),
    date_id INTEGER NOT NULL REFERENCES dim_date(date_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    revenue REAL NOT NULL CHECK (revenue >= 0),
    discount_amount REAL NOT NULL CHECK (discount_amount >= 0),
    is_returned INTEGER NOT NULL CHECK (is_returned IN (0, 1))
);
"""


def connect(database_path: Path) -> sqlite3.Connection:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables(connection: sqlite3.Connection) -> None:
    connection.executescript(SCHEMA_SQL)
    connection.commit()


def import_data(connection: sqlite3.Connection, data: dict[str, pd.DataFrame], replace: bool = True) -> dict[str, int]:
    create_tables(connection)
    if replace:
        for table in reversed(REQUIRED_TABLES):
            connection.execute(f"DELETE FROM {table}")
        connection.commit()

    summary = {}
    for table in REQUIRED_TABLES:
        data[table].to_sql(table, connection, if_exists="append", index=False)
        summary[table] = int(len(data[table]))
    connection.commit()
    return summary


def table_names(connection: sqlite3.Connection) -> set[str]:
    rows = connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
    return {row[0] for row in rows}
