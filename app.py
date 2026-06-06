from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.aggregation import FEATURE_COLUMNS
from src.config import PLOTS_DIR
from src.dashboard_utils import (
    MONTH_LABELS,
    format_currency,
    format_percent,
    format_score,
    generate_dashboard_summary,
    generate_store_insight,
    load_knn_results,
    load_model_metrics,
    load_monthly_performance,
    load_store_summary,
    prepare_feature_scatter_data,
    translate_efficiency_class,
)


st.set_page_config(page_title="Efektywność oddziałów", page_icon="📊", layout="wide")

CLASS_ORDER = ["low_efficiency", "medium_efficiency", "high_efficiency"]
CLASS_COLORS = {
    "low_efficiency": "#c84c4c",
    "medium_efficiency": "#d7a843",
    "high_efficiency": "#3f8f6b",
}
FEATURE_LABELS = {
    "monthly_revenue": "miesięczny przychód",
    "orders_count": "liczba transakcji",
    "avg_order_value": "średnia wartość transakcji",
    "return_rate": "udział zwrotów",
    "discount_share": "udział rabatów",
    "sales_per_employee": "sprzedaż na pracownika",
    "unique_customers": "unikalni klienci",
    "unique_products": "unikalne produkty",
    "performance_score": "performance score",
}


@st.cache_data
def load_dashboard_data() -> tuple[pd.DataFrame | None, pd.DataFrame | None, pd.DataFrame | None, dict | None]:
    return (
        load_monthly_performance(),
        load_store_summary(),
        load_knn_results(),
        load_model_metrics(),
    )


def main() -> None:
    st.title("Dashboard efektywności oddziałów")
    st.caption("Klasyfikacja miesięcznej efektywności sklepów obuwniczych")

    monthly, store_summary, knn_results, metrics = load_dashboard_data()
    if any(item is None for item in [monthly, store_summary, knn_results, metrics]):
        show_missing_results()
        return

    monthly = enrich_monthly(monthly)
    store_summary = enrich_store_summary(store_summary)

    tabs = st.tabs(
        ["Dashboard", "Oddziały", "Wyniki miesięczne", "Szczegóły oddziału", "Porównanie oddziałów", "Model kNN"]
    )
    with tabs[0]:
        render_dashboard(monthly, store_summary, metrics)
    with tabs[1]:
        render_stores(store_summary)
    with tabs[2]:
        render_monthly_results(monthly)
    with tabs[3]:
        render_store_details(monthly, store_summary)
    with tabs[4]:
        render_store_comparison(monthly)
    with tabs[5]:
        render_model_tab(monthly, knn_results, metrics)

def show_missing_results() -> None:
    st.info(
        "Brakuje plików wynikowych. Uruchom pipeline z terminala, np. "
        "`python main.py --source generated` albo `python main.py --source csv`, a następnie odśwież dashboard."
    )
    st.write("Dashboard prezentuje gotowe wyniki z katalogu `output/` i nie importuje ani nie generuje danych.")


def enrich_monthly(monthly: pd.DataFrame) -> pd.DataFrame:
    frame = monthly.copy()
    frame["month_label"] = frame["month"].map(MONTH_LABELS)
    frame["period_label"] = frame["year"].astype(str) + "-" + frame["month"].astype(int).astype(str).str.zfill(2)
    frame["class_label"] = frame["performance_class"].map(translate_efficiency_class)
    return frame


def enrich_store_summary(store_summary: pd.DataFrame) -> pd.DataFrame:
    frame = store_summary.copy()
    frame["dominant_class_label"] = frame["dominant_class"].map(translate_efficiency_class)
    return frame


def render_dashboard(monthly: pd.DataFrame, store_summary: pd.DataFrame, metrics: dict) -> None:
    cols = st.columns(6)
    cols[0].metric("Oddziały", monthly["store_id"].nunique())
    cols[1].metric("Miesiące", monthly["month"].nunique())
    cols[2].metric("Rekordy", len(monthly))
    cols[3].metric("Najlepsze k", metrics["best_k"])
    cols[4].metric("F1 macro", f"{metrics['f1_macro']:.3f}")
    cols[5].metric("Accuracy", f"{metrics['accuracy']:.3f}")

    st.subheader("Podsumowanie biznesowe")
    st.write(generate_dashboard_summary(store_summary, metrics))

    left, right = st.columns(2)
    with left:
        class_counts = monthly.groupby("class_label", as_index=False).size()
        st.plotly_chart(
            px.bar(class_counts, x="class_label", y="size", labels={"class_label": "Klasa", "size": "Liczba rekordów"}),
            use_container_width=True,
        )
    with right:
        ranking = store_summary.sort_values("avg_score", ascending=False)
        st.plotly_chart(
            px.bar(ranking, x="avg_score", y="store_name", orientation="h", labels={"avg_score": "Średni score", "store_name": "Oddział"}),
            use_container_width=True,
        )

    left, right = st.columns(2)
    with left:
        attention = store_summary.sort_values("low_months", ascending=False)
        st.plotly_chart(
            px.bar(attention, x="low_months", y="store_name", orientation="h", labels={"low_months": "Miesiące niskiej efektywności", "store_name": "Oddział"}),
            use_container_width=True,
        )
    with right:
        render_score_heatmap(monthly)


def render_score_heatmap(monthly: pd.DataFrame) -> None:
    periods = sorted(monthly["period_label"].unique())
    heatmap_data = monthly.pivot_table(index="store_name", columns="period_label", values="performance_score")
    heatmap_data = heatmap_data[periods]
    fig = px.imshow(
        heatmap_data,
        aspect="auto",
        color_continuous_scale="RdYlGn",
        labels={"x": "Okres", "y": "Oddział", "color": "Score"},
    )
    st.plotly_chart(fig, use_container_width=True)


def render_stores(store_summary: pd.DataFrame) -> None:
    st.subheader("Wykaz oddziałów")
    columns = {
        "store_name": "Nazwa oddziału",
        "city": "Miasto",
        "region": "Region",
        "location_type": "Typ lokalizacji",
        "store_size": "Rozmiar sklepu",
        "employee_count": "Pracownicy",
        "avg_score": "Średni score",
        "dominant_class_label": "Dominująca klasa",
        "low_months": "Miesiące niskie",
        "medium_months": "Miesiące średnie",
        "high_months": "Miesiące wysokie",
        "avg_revenue": "Średni przychód",
        "avg_sales_per_employee": "Sprzedaż na pracownika",
    }
    display = store_summary[list(columns)].rename(columns=columns)
    st.dataframe(display, use_container_width=True)
    st.download_button("Pobierz tabelę CSV", display.to_csv(index=False).encode("utf-8"), "store_summary.csv", "text/csv")


def render_monthly_results(monthly: pd.DataFrame) -> None:
    st.subheader("Wyniki miesięczne")
    st.write("Jeden wiersz oznacza jeden oddział w jednym miesiącu.")

    col1, col2, col3, col4 = st.columns(4)
    selected_stores = col1.multiselect("Oddział", sorted(monthly["store_name"].unique()), default=sorted(monthly["store_name"].unique()))
    selected_years = col2.multiselect("Rok", sorted(monthly["year"].unique()), default=sorted(monthly["year"].unique()))
    selected_months = col3.multiselect("Miesiąc", [MONTH_LABELS[i] for i in range(1, 13)], default=[MONTH_LABELS[i] for i in range(1, 13)])
    selected_classes = col4.multiselect(
        "Klasa efektywności",
        [translate_efficiency_class(value) for value in CLASS_ORDER],
        default=[translate_efficiency_class(value) for value in CLASS_ORDER],
    )
    filtered = monthly[
        monthly["store_name"].isin(selected_stores)
        & monthly["year"].isin(selected_years)
        & monthly["month_label"].isin(selected_months)
        & monthly["class_label"].isin(selected_classes)
    ]
    display = monthly_display(filtered)
    st.dataframe(display, use_container_width=True)
    st.download_button("Pobierz przefiltrowane wyniki CSV", display.to_csv(index=False).encode("utf-8"), "monthly_results.csv", "text/csv")


def render_store_details(monthly: pd.DataFrame, store_summary: pd.DataFrame) -> None:
    st.subheader("Szczegóły oddziału")
    selected = st.selectbox("Wybierz oddział", sorted(monthly["store_name"].unique()))
    store_monthly = monthly[monthly["store_name"] == selected].sort_values(["year", "month"])
    summary = store_summary[store_summary["store_name"] == selected].iloc[0]

    cols = st.columns(4)
    cols[0].metric("Średni score", format_score(float(summary["avg_score"])))
    cols[1].metric("Dominująca klasa", summary["dominant_class_label"])
    cols[2].metric("Najlepszy okres", store_period(summary, "best"))
    cols[3].metric("Najsłabszy okres", store_period(summary, "worst"))
    cols = st.columns(4)
    cols[0].metric("Średni przychód", format_currency(float(summary["avg_revenue"])))
    cols[1].metric("Średni udział zwrotów", format_percent(float(summary["avg_return_rate"])))
    cols[2].metric("Średni udział rabatów", format_percent(float(summary["avg_discount_share"])))
    cols[3].metric("Sprzedaż na pracownika", format_currency(float(summary["avg_sales_per_employee"])))

    st.write(generate_store_insight(selected, store_monthly, summary))
    render_line_chart(store_monthly, "performance_score", "Performance score")
    render_line_chart(store_monthly, "monthly_revenue", "Miesięczny przychód")
    render_line_chart(store_monthly, "return_rate", "Udział zwrotów")
    st.dataframe(monthly_display(store_monthly), use_container_width=True)


def render_store_comparison(monthly: pd.DataFrame) -> None:
    st.subheader("Porównanie oddziałów")
    stores = sorted(monthly["store_name"].unique())
    selected = st.multiselect("Wybierz od 2 do 4 oddziałów", stores, default=stores[:3])
    selected = selected[:4]
    if len(selected) < 2:
        st.info("Wybierz co najmniej dwa oddziały.")
        return
    filtered = monthly[monthly["store_name"].isin(selected)].sort_values(["year", "month"])
    render_multi_line_chart(filtered, "performance_score", "Performance score")
    render_multi_line_chart(filtered, "monthly_revenue", "Miesięczny przychód")

    comparison = (
        filtered.groupby("store_name", as_index=False)
        .agg(
            avg_score=("performance_score", "mean"),
            avg_revenue=("monthly_revenue", "mean"),
            avg_orders_count=("orders_count", "mean"),
            avg_return_rate=("return_rate", "mean"),
            avg_discount_share=("discount_share", "mean"),
            avg_sales_per_employee=("sales_per_employee", "mean"),
            low_months=("performance_class", lambda s: int((s == "low_efficiency").sum())),
            high_months=("performance_class", lambda s: int((s == "high_efficiency").sum())),
        )
    )
    st.dataframe(comparison, use_container_width=True)
    best_score = comparison.sort_values("avg_score", ascending=False).iloc[0]
    best_revenue = comparison.sort_values("avg_revenue", ascending=False).iloc[0]
    most_returns = comparison.sort_values("avg_return_rate", ascending=False).iloc[0]
    st.write(
        f"Najwyższy średni score ma {best_score['store_name']}. "
        f"Najwyższy średni przychód ma {best_revenue['store_name']}. "
        f"Największy średni udział zwrotów ma {most_returns['store_name']}."
    )


def render_model_tab(monthly: pd.DataFrame, knn_results: pd.DataFrame, metrics: dict) -> None:
    st.subheader("Model kNN")
    cols = st.columns(5)
    cols[0].metric("Najlepsze k", metrics["best_k"])
    cols[1].metric("Accuracy", f"{metrics['accuracy']:.3f}")
    cols[2].metric("Precision macro", f"{metrics['precision_macro']:.3f}")
    cols[3].metric("Recall macro", f"{metrics['recall_macro']:.3f}")
    cols[4].metric("F1 macro", f"{metrics['f1_macro']:.3f}")

    st.write(
        f"Najlepszy wynik uzyskano dla k = {metrics['best_k']}. "
        f"F1-score macro wynosi {metrics['f1_macro']:.3f}. Wynik należy traktować demonstracyjnie, "
        "ponieważ zbiór danych jest syntetyczny i niewielki."
    )
    st.dataframe(knn_results, use_container_width=True)
    st.plotly_chart(
        px.line(knn_results, x="k", y=["f1_macro", "accuracy"], markers=True, labels={"value": "Wynik", "variable": "Metryka"}),
        use_container_width=True,
    )

    left, right = st.columns(2)
    show_image(left, PLOTS_DIR / "confusion_matrix.png", "Macierz pomyłek")
    show_image(right, PLOTS_DIR / "knn_pca_classification_space.png", "PCA 2D - klasy rzeczywiste")
    show_image(st, PLOTS_DIR / "knn_pca_predictions.png", "PCA 2D - predykcje modelu")

    st.write(
        "Model kNN klasyfikuje rekordy na podstawie podobieństwa do najbliższych sąsiadów. "
        "PCA pokazuje dane w uproszczonej przestrzeni 2D: jeden punkt oznacza jeden oddział w jednym miesiącu."
    )
    st.caption(
        "Wykres PCA jest uproszczeniem. Oryginalny model działa w przestrzeni wielu cech, więc odległości 2D są tylko intuicyjną wizualizacją."
    )
    render_feature_explorer(monthly)


def render_feature_explorer(monthly: pd.DataFrame) -> None:
    st.subheader("Eksploracja cech modelu")
    feature_options = FEATURE_COLUMNS + ["performance_score"]
    col1, col2 = st.columns(2)
    x_feature = col1.selectbox("Cecha na osi X", feature_options, index=0, format_func=lambda value: FEATURE_LABELS[value])
    y_feature = col2.selectbox("Cecha na osi Y", feature_options, index=5, format_func=lambda value: FEATURE_LABELS[value])
    data = prepare_feature_scatter_data(monthly)
    fig = px.scatter(
        data,
        x=x_feature,
        y=y_feature,
        color="performance_class",
        color_discrete_map=CLASS_COLORS,
        hover_data=["store_name", "period_label", "performance_score", "class_label"],
        labels={x_feature: FEATURE_LABELS[x_feature], y_feature: FEATURE_LABELS[y_feature], "performance_class": "Klasa"},
    )
    st.plotly_chart(fig, use_container_width=True)
    st.write("Ten wykres pozwala sprawdzić, jak wybrane cechy biznesowe wpływają na rozdzielenie klas efektywności.")


def monthly_display(frame: pd.DataFrame) -> pd.DataFrame:
    columns = {
        "store_name": "Oddział",
        "year": "Rok",
        "month_label": "Miesiąc",
        "period_label": "Okres",
        "monthly_revenue": "Miesięczny przychód",
        "orders_count": "Liczba transakcji",
        "avg_order_value": "Średnia wartość transakcji",
        "return_rate": "Udział zwrotów",
        "discount_share": "Udział rabatów",
        "sales_per_employee": "Sprzedaż na pracownika",
        "unique_customers": "Unikalni klienci",
        "unique_products": "Unikalne produkty",
        "performance_score": "Performance score",
        "class_label": "Klasa efektywności",
    }
    return frame[list(columns)].rename(columns=columns)


def render_line_chart(frame: pd.DataFrame, value: str, title: str) -> None:
    fig = px.line(frame, x="period_label", y=value, markers=True, labels={"period_label": "Okres", value: title})
    st.plotly_chart(fig, use_container_width=True)


def render_multi_line_chart(frame: pd.DataFrame, value: str, title: str) -> None:
    fig = px.line(
        frame,
        x="period_label",
        y=value,
        color="store_name",
        markers=True,
        labels={"period_label": "Okres", value: title, "store_name": "Oddział"},
    )
    st.plotly_chart(fig, use_container_width=True)


def show_image(container, path: Path, caption: str) -> None:
    if path.exists():
        container.image(str(path), caption=caption)
    else:
        container.info(f"Brak pliku: {path.name}")


def store_period(summary: pd.Series, prefix: str) -> str:
    period_column = f"{prefix}_period"
    if period_column in summary and pd.notna(summary[period_column]):
        return str(summary[period_column])
    month_column = f"{prefix}_month"
    if month_column in summary and pd.notna(summary[month_column]):
        return MONTH_LABELS.get(int(summary[month_column]), str(summary[month_column]))
    return "brak danych"


if __name__ == "__main__":
    main()
