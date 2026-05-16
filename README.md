# CLI Data Parser
A command-line tool that reads employee data from a CSV or JSON file, applies filters, transformations, and aggregations, then outputs clean structured JSON. Built with Python's standard library plus rich for colourful terminal output.

cli-data-parser/
│
├── main.py            # CLI entry point — run this file
├── parser.py          # Pipeline orchestrator (ETL flow)
├── processor.py       # Filter / Transform / Aggregate logic
├── utils.py           # File I/O helpers (read CSV/JSON, write JSON)
│
├── data/
│   ├── employees.csv  # Sample CSV input
│   └── employees.json # Sample JSON input
│
├── output/
│   └── result.json    # Generated output file
│
└── logs/
    └── app.log        # Auto-generated log file

Tech Stack
Library    Type      Purpose
argparse   Built-in  CLI argument parsing
csv        Built-in  Read CSV files
json       Built-in  Read/write JSON files
logging    Built-in  Log events to file and console
pathlib    Built-in  Cross-platform file path handling
rich       Install   Colourful tables and terminal output
typer      Install   Modern CLI alternative

Installation:

Step 1- Clone or create the project folder
mkdir cli-data-parser
cd cli-data-parser
mkdir data output logs

Step 2 — Create all files
touch main.py parser.py processor.py utils.py
touch data/employees.csv data/employees.json

Step 3 — Install external libraries
pip install rich typer

Commands for Powershell:

## 1. Basic — read all records from CSV
python main.py --input data/employees.csv --output output/result.json

## 2. Filter by city
python main.py --input data/employees.csv --output output/result.json --city Kolkata

## 3. Filter + transform names to uppercase + show aggregates
python main.py --input data/employees.csv --output output/result.json --city Kolkata --uppercase --aggregate

## 4. Add salary bracket (Low / Mid / High) + aggregates
python main.py --input data/employees.csv --output output/result.json --bracket --aggregate

## 5. Filter by minimum salary
python main.py --input data/employees.csv --output output/result.json --min-salary 60000

## 6. Filter by maximum age
python main.py --input data/employees.csv --output output/result.json --max-age 27

## 7. Read from JSON instead of CSV
python main.py --input data/employees.json --output output/result.json --city Delhi --aggregate

How It Works — Pipeline Flow:

User runs CLI command
        ↓
Parse --flags with argparse (main.py)
        ↓
Read input file — auto-detect CSV or JSON (utils.py)
        ↓
Cast string fields to int — age, salary (processor.py)
        ↓
Apply Filters — city / min-salary / max-age (processor.py)
        ↓
Apply Transforms — uppercase / bracket (processor.py)
        ↓
Compute Aggregates (optional) (processor.py)
        ↓
Handle errors with try/except (main.py)
        ↓
Log all operations → logs/app.log (logging module)
        ↓
Save structured JSON → output/result.json (utils.py)
        ↓
Display Rich table in terminal (main.py)

This was built as a learning project for CLI tooling, data processing, and Python best practices.
