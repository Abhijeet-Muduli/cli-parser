import argparse
import logging
import sys
from pathlib import Path

try:
    from rich.console import Console
    from rich.table import Table
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from parser import run_pipeline

Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)
console = Console() if RICH_AVAILABLE else None

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="cli-data-parser",
        description="CLI tool to filter, transform & aggregate employee data",
    )
    # Required
    p.add_argument("--input",      required=True, help="Path to .csv or .json file")
    p.add_argument("--output",     required=True, help="Path for output JSON file")
    # Filters
    p.add_argument("--city",       type=str, help="Keep only records from this city")
    p.add_argument("--min-salary", type=int, help="Keep records with salary >= VALUE")
    p.add_argument("--max-age",    type=int, help="Keep records with age <= VALUE")
    # Transforms
    p.add_argument("--uppercase",  action="store_true", help="Uppercase all names")
    p.add_argument("--bracket",    action="store_true", help="Add Low/Mid/High salary bracket")
    # Extras
    p.add_argument("--aggregate",  action="store_true", help="Print summary statistics")
    return p

def print_records_table(records: list[dict]) -> None:
    if not records:
        rprint("[yellow]⚠️  No records match the given filters.[/yellow]")
        return
    table = Table(title="Processed Records", show_header=True, header_style="bold cyan")
    for key in records[0].keys():
        table.add_column(key.capitalize(), style="white")
    for row in records:
        table.add_row(*[str(v) for v in row.values()])
    console.print(table)

def print_aggregates(agg: dict) -> None:
    rprint("\n[bold magenta]── Aggregates ──[/bold magenta]")
    for k, v in agg.items():
        rprint(f"  [cyan]{k}[/cyan]: [bold]{v}[/bold]")

def print_fallback(records, agg):
    print("\n=== Processed Records ===")
    for r in records:
        print(r)
    if agg:
        print("\n=== Aggregates ===")
        for k, v in agg.items():
            print(f"  {k}: {v}")

def main():
    arg_parser = build_parser()
    args = arg_parser.parse_args()
    logger.info(f"Args received: {vars(args)}")

    try:
        result = run_pipeline(
            input_file      = args.input,
            output_file     = args.output,
            city            = args.city,
            min_salary      = args.min_salary,
            max_age         = args.max_age,
            uppercase       = args.uppercase,
            add_bracket     = args.bracket,
            show_aggregates = args.aggregate,
        )

        records = result["records"]
        agg     = result.get("aggregates")

        if RICH_AVAILABLE:
            rprint(f"\n[bold green]✅ Done! {len(records)} record(s) written → {args.output}[/bold green]")
            print_records_table(records)
            if agg:
                print_aggregates(agg)
        else:
            print(f"\nDone! {len(records)} record(s) written to {args.output}")
            print_fallback(records, agg)

    except FileNotFoundError as e:
        logger.error(e)
        rprint(f"[bold red]❌ File not found: {e}[/bold red]") if RICH_AVAILABLE else print(f"ERROR: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(e)
        rprint(f"[bold red]❌ Bad input: {e}[/bold red]") if RICH_AVAILABLE else print(f"ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error")
        rprint(f"[bold red]❌ Unexpected error: {e}[/bold red]") if RICH_AVAILABLE else print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()