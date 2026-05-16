import logging

logger = logging.getLogger(__name__)

def filter_by_city(data: list[dict], city: str) -> list[dict]:
    result = [r for r in data if r.get("city", "").lower() == city.lower()]
    logger.info(f"Filter by city='{city}': {len(data)} → {len(result)} records")
    return result

def filter_by_min_salary(data: list[dict], min_salary: int) -> list[dict]:
    result = [r for r in data if int(r.get("salary", 0)) >= min_salary]
    logger.info(f"Filter by salary>={min_salary}: {len(data)} → {len(result)} records")
    return result

def filter_by_max_age(data: list[dict], max_age: int) -> list[dict]:
    result = [r for r in data if int(r.get("age", 0)) <= max_age]
    logger.info(f"Filter by age<={max_age}: {len(data)} → {len(result)} records")
    return result


def uppercase_names(data: list[dict]) -> list[dict]:
    for record in data:
        if "name" in record:
            record["name"] = record["name"].upper()
    logger.info("Transformation applied: names uppercased")
    return data

def cast_numeric_fields(data: list[dict]) -> list[dict]:
    for record in data:
        try:
            record["age"] = int(record["age"])
        except (ValueError, KeyError):
            pass
        try:
            record["salary"] = int(record["salary"])
        except (ValueError, KeyError):
            pass
    logger.info("Transformation applied: numeric fields cast to int")
    return data

def add_salary_bracket(data: list[dict]) -> list[dict]:
    for record in data:
        sal = int(record.get("salary", 0))
        if sal < 50000:
            record["bracket"] = "Low"
        elif sal < 70000:
            record["bracket"] = "Mid"
        else:
            record["bracket"] = "High"
    logger.info("Transformation applied: salary brackets added")
    return data


def compute_aggregates(data: list[dict]) -> dict:
    if not data:
        return {"total_records": 0}
    salaries = [int(r.get("salary", 0)) for r in data]
    ages     = [int(r.get("age",    0)) for r in data]
    aggregates = {
        "total_records": len(data),
        "avg_salary":    round(sum(salaries) / len(salaries), 2),
        "min_salary":    min(salaries),
        "max_salary":    max(salaries),
        "avg_age":       round(sum(ages) / len(ages), 2),
    }
    logger.info(f"Aggregates computed: {aggregates}")
    return aggregates