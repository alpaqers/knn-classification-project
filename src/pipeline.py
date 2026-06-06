from pathlib import Path

from src import database
from src.aggregation import build_store_monthly_performance
from src.config import DATABASE_PATH, INPUT_DIR, PLOTS_DIR, REPORTS_DIR, ensure_directories
from src.data_generator import generate_sample_data
from src.data_importer import import_csv_to_sqlite
from src.ml_pipeline import train_knn_model
from src.output_writer import write_dashboard_outputs
from src.reporting import write_reports
from src.visualization import generate_plots


def run_pipeline(source: str, input_dir: Path = INPUT_DIR, database_path: Path = DATABASE_PATH) -> dict:
    ensure_directories()
    if source == "generated":
        generate_sample_data(input_dir)
    elif source != "csv":
        raise ValueError("source must be 'csv' or 'generated'")

    import_summary = import_csv_to_sqlite(input_dir, database_path, replace=True)
    with database.connect(database_path) as connection:
        performance = build_store_monthly_performance(connection)
        metrics = train_knn_model(performance, REPORTS_DIR)
        output_files = write_dashboard_outputs(performance, metrics, connection)

    plot_paths = generate_plots(performance, metrics, PLOTS_DIR)
    write_reports(performance, metrics, REPORTS_DIR, database_path, PLOTS_DIR)
    return {
        "import_summary": import_summary,
        "records": len(performance),
        "metrics": metrics,
        "plots": [str(path) for path in plot_paths],
        "output_files": {key: str(path) for key, path in output_files.items()},
        "database_path": str(database_path),
    }
