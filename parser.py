import logging
from utils import read_file, write_json
from processor import (
    cast_numeric_fields,
    filter_by_city,
    filter_by_min_salary,
    filter_by_max_age,
    uppercase_names,
    add_salary_bracket,
    compute_aggregates,
)

logger = logging.getLogger(__name__)

def run_pipeline(
    input_file: str,
    output_file: str,
    city: str | None = None,
    min_salary: int | None = None,
    max_age: int | None = None,
    uppercase: bool = False,
    add_bracket: bool = False,
    show_aggregates: bool = False,
) -> dict:
    logger.info("=== Pipeline started ===")

    # Step 1 — Extract
    data = read_file(input_file)

    # Step 2 — Cast string types to int (CSV gives everything as string)
    data = cast_numeric_fields(data)

    # Step 3 — Filter
    if city:
        data = filter_by_city(data, city)
    if min_salary is not None:
        data = filter_by_min_salary(data, min_salary)
    if max_age is not None:
        data = filter_by_max_age(data, max_age)

    # Step 4 — Transform
    if uppercase:
        data = uppercase_names(data)
    if add_bracket:
        data = add_salary_bracket(data)

    # Step 5 — Aggregate (optional)
    result = {"records": data}
    if show_aggregates:
        result["aggregates"] = compute_aggregates(data)

    # Step 6 — Load (write output JSON)
    write_json(data, output_file)
    logger.info("=== Pipeline complete ===")

    return result