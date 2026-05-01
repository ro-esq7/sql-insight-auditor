"""
parse_sql.py

Deterministic SQL parser for the sql-insight-auditor skill.

This script extracts structural pieces from a SQL query so the AI agent
does not have to rely on prose alone when documenting the query.

Usage:
python .agents/skills/sql-insight-auditor/scripts/parse_sql.py inputs/normal_case.sql outputs/normal_case_parsed_summary.json
"""

# Step 1: Import libraries
import json
import re
import sys
from pathlib import Path


# Step 2: Define reusable regex patterns to identify common SQL aggregate functions.
AGGREGATE_PATTERN = re.compile(
    r"\b(COUNT|SUM|AVG|MIN|MAX)\s*\(",
    re.IGNORECASE
)


# Step 3: Read the SQL file
def read_sql_file(input_path: str) -> str:
    """Read SQL text from a file."""
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f"Input SQL file not found: {input_path}")

    return path.read_text(encoding="utf-8")


# Step 4: Clean the SQL text
def clean_sql(sql: str) -> str:
    """
    Remove SQL comments and normalize whitespace.

    This makes the query easier to parse with regular expressions.
    """
    sql = re.sub(r"--.*", "", sql)
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)
    sql = re.sub(r"\s+", " ", sql)
    return sql.strip()


# Step 5: Extract a SQL clause
def extract_clause(sql: str, start_keyword: str, end_keywords: list[str]) -> str:
    """
    Extract text between a start keyword and the nearest following end keyword.

    Example:
    SELECT field_1, field_2 FROM table_name WHERE field_1 > 0

    If start_keyword = SELECT and end_keywords = [FROM],
    this returns: field_1, field_2
    """
    start_pattern = rf"\b{start_keyword}\b"
    start_match = re.search(start_pattern, sql, flags=re.IGNORECASE)

    if not start_match:
        return ""

    start_index = start_match.end()
    remaining_sql = sql[start_index:]

    end_positions = []
    for keyword in end_keywords:
        end_match = re.search(rf"\b{keyword}\b", remaining_sql, flags=re.IGNORECASE)
        if end_match:
            end_positions.append(end_match.start())

    if end_positions:
        end_index = min(end_positions)
        return remaining_sql[:end_index].strip()

    return remaining_sql.strip()


# Step 6: Split comma-separated SQL fields
def split_comma_items(text: str) -> list[str]:
    """
    Split comma-separated SQL items while respecting parentheses.

    This helps avoid splitting inside expressions like:
    DATE_TRUNC('month', order_date)
    """
    if not text:
        return []

    items = []
    current = []
    depth = 0

    for char in text:
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(depth - 1, 0)

        if char == "," and depth == 0:
            item = "".join(current).strip()
            if item:
                items.append(item)
            current = []
        else:
            current.append(char)

    final_item = "".join(current).strip()
    if final_item:
        items.append(final_item)

    return items


# Step 7: Extract source tables
def extract_tables(sql: str) -> list[str]:
    """
    Extract table names that appear after FROM or JOIN.
    """
    table_matches = re.findall(
        r"\b(?:FROM|JOIN)\s+([a-zA-Z0-9_.$`]+)",
        sql,
        flags=re.IGNORECASE
    )

    cleaned_tables = []
    for table in table_matches:
        cleaned = table.replace("`", "").strip()
        if cleaned and cleaned not in cleaned_tables:
            cleaned_tables.append(cleaned)

    return cleaned_tables


# Step 8: Extract JOIN clauses
def extract_joins(sql: str) -> list[str]:
    """
    Extract JOIN clauses from the query.
    """
    join_pattern = re.compile(
        r"\b((?:LEFT|RIGHT|INNER|FULL|OUTER|CROSS)?\s*JOIN\s+.*?)(?=\bLEFT\b|\bRIGHT\b|\bINNER\b|\bFULL\b|\bOUTER\b|\bCROSS\b|\bWHERE\b|\bGROUP BY\b|\bORDER BY\b|$)",
        flags=re.IGNORECASE
    )

    joins = [match.group(1).strip() for match in join_pattern.finditer(sql)]
    return joins


# Step 9: Extract WHERE filters
def extract_filters(where_clause: str) -> list[str]:
    """
    Split the WHERE clause into individual filters using AND as the separator.
    """
    if not where_clause:
        return []

    filters = re.split(r"\bAND\b", where_clause, flags=re.IGNORECASE)
    return [filter_text.strip() for filter_text in filters if filter_text.strip()]


# Step 10: Identify date-related filters
def identify_date_filters(filters: list[str]) -> list[str]:
    """
    Identify filters that appear to involve dates.
    """
    date_keywords = ["date", "month", "year", "current_date", "date_sub", "date_trunc"]

    date_filters = []
    for item in filters:
        lowered = item.lower()
        if any(keyword in lowered for keyword in date_keywords):
            date_filters.append(item)

    return date_filters


# Step 11: Identify aggregate metrics
def identify_aggregate_metrics(select_fields: list[str]) -> list[str]:
    """
    Identify selected fields that use common aggregate functions.
    """
    metrics = []
    for field in select_fields:
        if AGGREGATE_PATTERN.search(field):
            metrics.append(field)

    return metrics


# Step 12: Build documentation risk flags
def build_risk_flags(parsed: dict) -> list[str]:
    """
    Create simple risk flags based on the parsed SQL structure.
    """
    risks = []

    if not parsed["tables"]:
        risks.append("No source tables were identified. The query may use nested logic or unsupported syntax.")

    if not parsed["filters"]:
        risks.append("No WHERE filters were identified. Confirm whether the query intentionally includes all available records.")

    if parsed["joins"]:
        risks.append("Query includes joins. Confirm join keys and join type to avoid duplicate or unmatched records.")

    if parsed["aggregate_metrics"] and not parsed["group_by"]:
        risks.append("Aggregate metrics were identified without GROUP BY fields. Confirm whether this should return one overall summary row.")

    if parsed["date_filters"]:
        risks.append("Date filters were identified. Confirm whether the date window matches the business question.")

    if not parsed["aggregate_metrics"]:
        risks.append("No aggregate metrics were identified. Confirm whether the query is intended to return row-level data.")

    return risks


# Step 13: Parse the SQL into a structured dictionary
def parse_sql(sql_text: str) -> dict:
    """
    Parse SQL text into a structured summary.
    """
    sql = clean_sql(sql_text)

    select_clause = extract_clause(sql, "SELECT", ["FROM"])
    from_clause = extract_clause(sql, "FROM", ["WHERE", "GROUP BY", "ORDER BY"])
    where_clause = extract_clause(sql, "WHERE", ["GROUP BY", "ORDER BY"])
    group_by_clause = extract_clause(sql, "GROUP BY", ["ORDER BY"])
    order_by_clause = extract_clause(sql, "ORDER BY", [])

    select_fields = split_comma_items(select_clause)
    filters = extract_filters(where_clause)

    parsed = {
        "select_fields": select_fields,
        "from_clause": from_clause,
        "tables": extract_tables(sql),
        "joins": extract_joins(sql),
        "filters": filters,
        "group_by": split_comma_items(group_by_clause),
        "order_by": split_comma_items(order_by_clause),
        "date_filters": identify_date_filters(filters),
        "aggregate_metrics": identify_aggregate_metrics(select_fields),
        "parser_limitations": [
            "This parser is intentionally lightweight and works best for common analytical SQL.",
            "Complex nested queries, CTEs, vendor-specific syntax, and deeply nested expressions may require manual review."
        ]
    }

    parsed["risk_flags"] = build_risk_flags(parsed)

    return parsed


# Step 14: Write the parsed summary to JSON
def write_json(output_path: str, data: dict) -> None:
    """
    Write parsed output to a JSON file.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )


# Step 15: Build a default output path when one is not provided
def build_default_output_path(input_path: str) -> str:
    """
    Create a case-specific output file name based on the input SQL file name.

    Example:
    inputs/normal_case.sql becomes outputs/normal_case_parsed_summary.json
    """
    input_file = Path(input_path)
    output_file_name = f"{input_file.stem}_parsed_summary.json"

    return str(Path("outputs") / output_file_name)


# Step 16: Run the script from the command line
def main() -> None:
    """
    Main command-line workflow.

    The script supports two formats:

    Option 1: Provide only the input SQL file.
    The script will automatically create a case-specific output file.

    Example:
    python parse_sql.py inputs/normal_case.sql

    Option 2: Provide both the input SQL file and the output JSON file.

    Example:
    python parse_sql.py inputs/normal_case.sql outputs/normal_case_parsed_summary.json
    """
    if len(sys.argv) not in [2, 3]:
        print(
            "Usage: python parse_sql.py <input_sql_file> [output_json_file]",
            file=sys.stderr
        )
        sys.exit(1)

    input_path = sys.argv[1]

    if len(sys.argv) == 3:
        output_path = sys.argv[2]
    else:
        output_path = build_default_output_path(input_path)

    try:
        sql_text = read_sql_file(input_path)
        parsed_summary = parse_sql(sql_text)
        write_json(output_path, parsed_summary)
        print(f"Parsed SQL summary written to: {output_path}")

    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


# Step 17: Only run main() when this file is executed directly
if __name__ == "__main__":
    main()
