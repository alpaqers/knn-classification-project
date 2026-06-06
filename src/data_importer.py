from pathlib import Path

from src import database
from src.data_validator import validate_input_directory


def import_csv_to_sqlite(input_dir: Path, database_path: Path, replace: bool = True) -> dict[str, int]:
    data = validate_input_directory(input_dir)
    with database.connect(database_path) as connection:
        return database.import_data(connection, data, replace=replace)
