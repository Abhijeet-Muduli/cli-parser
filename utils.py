import csv
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def read_file(filepath: str) -> list[dict]:
    path = Path(filepath)
    if not path.exists():
        logger.error(f"File not found: {filepath}")
        raise FileNotFoundError(f"Input file does not exist: {filepath}")
    suffix = path.suffix.lower()
    if suffix == ".csv":
        logger.info(f"Reading CSV file: {filepath}")
        return _read_csv(filepath)
    elif suffix == ".json":
        logger.info(f"Reading JSON file: {filepath}")
        return _read_json(filepath)
    else:
        raise ValueError(f"Unsupported file type '{suffix}'. Use .csv or .json")

def _read_csv(filepath: str) -> list[dict]:
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    logger.info(f"Loaded {len(data)} records from CSV")
    return data

def _read_json(filepath: str) -> list[dict]:
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("JSON file must contain a list of objects at the top level.")
    logger.info(f"Loaded {len(data)} records from JSON")
    return data

def write_json(data: list[dict], filepath: str) -> None:
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    logger.info(f"Output written to {filepath} ({len(data)} records)")