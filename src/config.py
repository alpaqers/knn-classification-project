from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = ROOT_DIR / "output"
PLOTS_DIR = OUTPUT_DIR / "plots"
REPORTS_DIR = ROOT_DIR / "reports"
DOCS_DIR = ROOT_DIR / "docs"
DATABASE_PATH = DATA_DIR / "output" / "shoe_stores_dw.sqlite"

REQUIRED_TABLES = [
    "dim_store",
    "dim_product",
    "dim_customer",
    "dim_date",
    "fact_sales",
]

REQUIRED_COLUMNS = {
    "dim_store": [
        "store_id",
        "store_name",
        "city",
        "region",
        "location_type",
        "store_size",
        "opening_date",
        "employee_count",
    ],
    "dim_product": [
        "product_id",
        "product_name",
        "category",
        "brand",
        "gender",
        "base_price",
    ],
    "dim_customer": ["customer_id", "age_group", "city", "customer_type"],
    "dim_date": ["date_id", "date", "day", "month", "month_name", "quarter", "year", "season"],
    "fact_sales": [
        "sale_id",
        "store_id",
        "product_id",
        "customer_id",
        "date_id",
        "quantity",
        "revenue",
        "discount_amount",
        "is_returned",
    ],
}

ID_COLUMNS = {
    "dim_store": "store_id",
    "dim_product": "product_id",
    "dim_customer": "customer_id",
    "dim_date": "date_id",
    "fact_sales": "sale_id",
}


def ensure_directories() -> None:
    for path in [DATA_DIR, INPUT_DIR, DATA_DIR / "output", OUTPUT_DIR, PLOTS_DIR, REPORTS_DIR, DOCS_DIR]:
        path.mkdir(parents=True, exist_ok=True)
