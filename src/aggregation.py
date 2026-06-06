import sqlite3

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


PERFORMANCE_CLASSES = ["low_efficiency", "medium_efficiency", "high_efficiency"]
FEATURE_COLUMNS = [
    "monthly_revenue",
    "orders_count",
    "avg_order_value",
    "return_rate",
    "discount_share",
    "sales_per_employee",
    "unique_customers",
    "unique_products",
]


def build_store_monthly_performance(connection: sqlite3.Connection) -> pd.DataFrame:
    query = """
    SELECT
        s.store_id,
        s.store_name,
        d.year,
        d.month,
        SUM(f.revenue) AS monthly_revenue,
        COUNT(f.sale_id) AS orders_count,
        AVG(f.revenue) AS avg_order_value,
        AVG(CAST(f.is_returned AS REAL)) AS return_rate,
        CASE
            WHEN SUM(f.revenue + f.discount_amount) = 0 THEN 0
            ELSE SUM(f.discount_amount) / SUM(f.revenue + f.discount_amount)
        END AS discount_share,
        SUM(f.revenue) / MAX(s.employee_count) AS sales_per_employee,
        COUNT(DISTINCT f.customer_id) AS unique_customers,
        COUNT(DISTINCT f.product_id) AS unique_products
    FROM fact_sales f
    JOIN dim_store s ON s.store_id = f.store_id
    JOIN dim_date d ON d.date_id = f.date_id
    GROUP BY s.store_id, s.store_name, d.year, d.month
    ORDER BY s.store_id, d.year, d.month
    """
    frame = pd.read_sql_query(query, connection)
    if frame.empty:
        raise ValueError("No data available for store-month aggregation")
    frame = add_performance_score_and_class(frame)
    frame.to_sql("store_monthly_performance", connection, if_exists="replace", index=False)
    connection.commit()
    return frame


def add_performance_score_and_class(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    scaler = MinMaxScaler()
    scaled = pd.DataFrame(scaler.fit_transform(result[FEATURE_COLUMNS]), columns=FEATURE_COLUMNS, index=result.index)

    result["performance_score"] = (
        0.26 * scaled["monthly_revenue"]
        + 0.18 * scaled["sales_per_employee"]
        + 0.14 * scaled["avg_order_value"]
        + 0.14 * scaled["unique_customers"]
        + 0.08 * scaled["orders_count"]
        + 0.06 * scaled["unique_products"]
        - 0.09 * scaled["return_rate"]
        - 0.07 * scaled["discount_share"]
    )

    low_cut = result["performance_score"].quantile(0.33)
    high_cut = result["performance_score"].quantile(0.66)
    result["performance_class"] = np.select(
        [
            result["performance_score"] <= low_cut,
            result["performance_score"] >= high_cut,
        ],
        ["low_efficiency", "high_efficiency"],
        default="medium_efficiency",
    )
    return result
