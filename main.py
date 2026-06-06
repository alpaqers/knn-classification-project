import argparse

from src.data_validator import ValidationError
from src.pipeline import run_pipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Shoe store monthly efficiency classification pipeline")
    parser.add_argument("--source", choices=["csv", "generated"], required=True, help="Data source mode")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = run_pipeline(args.source)
    except ValidationError as exc:
        print(f"Validation error: {exc}")
        return 1
    except Exception as exc:
        print(f"Pipeline error: {exc}")
        return 1

    print("Pipeline finished successfully.")
    print(f"Imported rows: {result['import_summary']}")
    print(f"Store-month records: {result['records']}")
    print(f"Best k: {result['metrics']['best_k']}")
    print(f"F1-score macro: {result['metrics']['f1_score']:.4f}")
    print(f"SQLite database: {result['database_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
