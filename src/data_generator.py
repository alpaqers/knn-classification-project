from pathlib import Path

import numpy as np
import pandas as pd

from src.config import REQUIRED_TABLES


STORE_ROWS = [
    (1, "Warszawa Centrum", "Warszawa", "mazowieckie", "high_street", "large", "2016-03-12", 28, 1.35),
    (2, "Kraków Galeria", "Kraków", "małopolskie", "shopping_mall", "large", "2017-05-20", 24, 1.25),
    (3, "Wrocław Rynek", "Wrocław", "dolnośląskie", "high_street", "medium", "2018-04-18", 18, 1.08),
    (4, "Gdańsk Morena", "Gdańsk", "pomorskie", "shopping_mall", "medium", "2019-09-02", 17, 1.02),
    (5, "Poznań Plaza", "Poznań", "wielkopolskie", "shopping_mall", "medium", "2020-02-10", 16, 0.98),
    (6, "Łódź Manufaktura", "Łódź", "łódzkie", "shopping_mall", "large", "2017-11-15", 22, 1.14),
    (7, "Katowice Silesia", "Katowice", "śląskie", "retail_park", "medium", "2021-06-01", 15, 0.92),
    (8, "Lublin Felicity", "Lublin", "lubelskie", "shopping_mall", "small", "2022-08-22", 11, 0.78),
]

CATEGORIES = ["sneakersy", "buty sportowe", "buty eleganckie", "botki", "kozaki", "sandały", "klapki"]
BRANDS = ["StepWay", "UrbanFoot", "NordShoe", "Elegante", "Runnero", "ComfyWalk", "ModaBut"]
GENDERS = ["women", "men", "unisex", "kids"]
CITIES = ["Warszawa", "Kraków", "Wrocław", "Gdańsk", "Poznań", "Łódź", "Katowice", "Lublin"]
AGE_GROUPS = ["18-25", "26-35", "36-45", "46-60", "60+"]
CUSTOMER_TYPES = ["new", "regular", "loyal", "occasional"]
MONTH_NAMES = {
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


def generate_sample_data(output_dir: Path, seed: int = 42, year: int = 2025) -> dict[str, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    stores = _generate_stores()
    products = _generate_products(rng)
    customers = _generate_customers(rng)
    dates = _generate_dates(year)
    sales = _generate_sales(rng, stores, products, customers, dates)

    data = {
        "dim_store": stores.drop(columns=["sales_weight"]),
        "dim_product": products,
        "dim_customer": customers,
        "dim_date": dates,
        "fact_sales": sales,
    }
    for table in REQUIRED_TABLES:
        data[table].to_csv(output_dir / f"{table}.csv", index=False)
    return data


def _generate_stores() -> pd.DataFrame:
    return pd.DataFrame(
        STORE_ROWS,
        columns=[
            "store_id",
            "store_name",
            "city",
            "region",
            "location_type",
            "store_size",
            "opening_date",
            "employee_count",
            "sales_weight",
        ],
    )


def _generate_products(rng: np.random.Generator, product_count: int = 52) -> pd.DataFrame:
    category_prices = {
        "sneakersy": (220, 420),
        "buty sportowe": (180, 380),
        "buty eleganckie": (260, 560),
        "botki": (230, 470),
        "kozaki": (330, 690),
        "sandały": (120, 280),
        "klapki": (70, 180),
    }
    rows = []
    for product_id in range(1, product_count + 1):
        category = CATEGORIES[(product_id - 1) % len(CATEGORIES)]
        low, high = category_prices[category]
        price = round(float(rng.uniform(low, high)), 2)
        rows.append(
            {
                "product_id": product_id,
                "product_name": f"{category.title()} {product_id:02d}",
                "category": category,
                "brand": rng.choice(BRANDS),
                "gender": rng.choice(GENDERS, p=[0.38, 0.34, 0.22, 0.06]),
                "base_price": price,
            }
        )
    return pd.DataFrame(rows)


def _generate_customers(rng: np.random.Generator, customer_count: int = 440) -> pd.DataFrame:
    rows = []
    for customer_id in range(1, customer_count + 1):
        rows.append(
            {
                "customer_id": customer_id,
                "age_group": rng.choice(AGE_GROUPS, p=[0.20, 0.30, 0.24, 0.18, 0.08]),
                "city": rng.choice(CITIES),
                "customer_type": rng.choice(CUSTOMER_TYPES, p=[0.22, 0.34, 0.18, 0.26]),
            }
        )
    return pd.DataFrame(rows)


def _generate_dates(year: int = 2025) -> pd.DataFrame:
    dates = pd.date_range(f"{year}-01-01", f"{year}-12-31", freq="D")
    rows = []
    for idx, date in enumerate(dates, start=1):
        month = int(date.month)
        rows.append(
            {
                "date_id": int(date.strftime("%Y%m%d")),
                "date": date.strftime("%Y-%m-%d"),
                "day": int(date.day),
                "month": month,
                "month_name": MONTH_NAMES[month],
                "quarter": int((month - 1) // 3 + 1),
                "year": int(date.year),
                "season": _season(month),
            }
        )
    return pd.DataFrame(rows)


def _generate_sales(
    rng: np.random.Generator,
    stores: pd.DataFrame,
    products: pd.DataFrame,
    customers: pd.DataFrame,
    dates: pd.DataFrame,
    sales_count: int = 5600,
) -> pd.DataFrame:
    store_weights = stores["sales_weight"].to_numpy(dtype=float)
    store_weights = store_weights / store_weights.sum()
    product_weights = products["category"].map(_category_base_weight).to_numpy(dtype=float)
    product_weights = product_weights / product_weights.sum()

    rows = []
    for sale_id in range(1, sales_count + 1):
        store = stores.iloc[int(rng.choice(len(stores), p=store_weights))]
        date = dates.iloc[int(rng.integers(0, len(dates)))]
        product = _choose_product_for_month(rng, products, product_weights, int(date["month"]))
        customer_id = int(rng.integers(1, len(customers) + 1))
        quantity = int(rng.choice([1, 1, 1, 2, 2, 3], p=[0.42, 0.2, 0.13, 0.16, 0.06, 0.03]))
        discount_rate = _discount_rate(rng, str(store["store_size"]), int(date["month"]))
        is_returned = int(rng.random() < _return_probability(str(product["category"]), discount_rate))
        gross_revenue = float(product["base_price"]) * quantity
        discount_amount = round(gross_revenue * discount_rate, 2)
        revenue = round(max(gross_revenue - discount_amount, 0), 2)
        if is_returned:
            revenue = round(revenue * rng.uniform(0.0, 0.25), 2)

        rows.append(
            {
                "sale_id": sale_id,
                "store_id": int(store["store_id"]),
                "product_id": int(product["product_id"]),
                "customer_id": customer_id,
                "date_id": int(date["date_id"]),
                "quantity": quantity,
                "revenue": revenue,
                "discount_amount": discount_amount,
                "is_returned": is_returned,
            }
        )
    return pd.DataFrame(rows)


def _choose_product_for_month(
    rng: np.random.Generator, products: pd.DataFrame, base_weights: np.ndarray, month: int
) -> pd.Series:
    seasonal = products["category"].map(lambda category: _seasonal_multiplier(category, month)).to_numpy(dtype=float)
    weights = base_weights * seasonal
    weights = weights / weights.sum()
    return products.iloc[int(rng.choice(len(products), p=weights))]


def _category_base_weight(category: str) -> float:
    return {
        "sneakersy": 1.45,
        "buty sportowe": 1.25,
        "buty eleganckie": 0.88,
        "botki": 0.9,
        "kozaki": 0.74,
        "sandały": 0.95,
        "klapki": 0.72,
    }[category]


def _seasonal_multiplier(category: str, month: int) -> float:
    if category in {"kozaki", "botki"} and month in {1, 2, 10, 11, 12}:
        return 1.9
    if category in {"sandały", "klapki"} and month in {5, 6, 7, 8}:
        return 2.0
    if category in {"sneakersy", "buty sportowe"} and month in {3, 4, 8, 9}:
        return 1.45
    return 1.0


def _discount_rate(rng: np.random.Generator, store_size: str, month: int) -> float:
    base = {"small": 0.11, "medium": 0.08, "large": 0.065}[store_size]
    seasonal_boost = 0.04 if month in {1, 7, 11} else 0.0
    return round(float(np.clip(rng.normal(base + seasonal_boost, 0.035), 0, 0.28)), 3)


def _return_probability(category: str, discount_rate: float) -> float:
    base = 0.055
    if category in {"kozaki", "buty eleganckie"}:
        base += 0.025
    if discount_rate > 0.16:
        base += 0.015
    return base


def _season(month: int) -> str:
    if month in {12, 1, 2}:
        return "winter"
    if month in {3, 4, 5}:
        return "spring"
    if month in {6, 7, 8}:
        return "summer"
    return "autumn"
