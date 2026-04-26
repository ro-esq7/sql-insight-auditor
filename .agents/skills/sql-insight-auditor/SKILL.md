---
name: sql-insight-auditor
description: Parses a SQL query, identifies its tables, fields, joins, filters, grouping logic, ordering logic, aggregate metrics, date conditions, and possible documentation risks, then produces a stakeholder-ready query audit. Use when the user provides a SQL query and asks to explain, document, review, or summarize what the query is doing for a business or analytics audience.
---

# SQL Insight Auditor

## Purpose

The `sql-insight-auditor` skill will help analysts turn a SQL query into a clear, structured, stakeholder-ready audit. The skill is designed for situations where a query needs to be explained or documented for an audience without executing the SQL or connecting to a live database.

This skill uses a Python script for the deterministic part of the workflow. The script parses the SQL query and extracts the structural elements of the query. The agent then uses that parsed output to create a plain-English explanation, including the query purpose, logic, assumptions, and risks.

## When to Use This Skill

Use this skill when the user provides a SQL query and asks to:

- Explain what the query does.
- Document SQL logic for a business or analytics audience.
- Summarize the tables, fields, filters, joins, and metrics used in a query.
- Translate SQL logic into a stakeholder-ready explanation.
- Identify assumptions, caveats, or documentation risks in a SQL query.
- Create a query audit or query brief.

## When Not to Use This Skill

Do not use this skill when the user is asking to:

- Execute SQL against a database.
- Connect to Databricks, Snowflake, BigQuery, PostgreSQL, MySQL, or another live database.
- Validate whether the returned query results are accurate.
- Optimize SQL performance.
- Rewrite or refactor the SQL query.
- Build a dashboard or visualization.
- Explain a programming language that is not SQL.
- Audit an entire data pipeline instead of one SQL query.

If the user asks for one of those tasks, clarify that this skill is limited to parsing and documenting a provided SQL query.

## Expected Inputs

This skill expects:

1. A SQL query, either pasted directly by the user or saved as a `.sql` file.
2. A short business question or context statement explaining what the query is supposed to answer.

Recommended input files:
```text
- inputs/sample_query.sql
- inputs/business_question.md
```

The SQL query may include common SQL clauses such as:

- `SELECT`
- `FROM`
- `JOIN`
- `WHERE`
- `GROUP BY`
- `ORDER BY`
- aggregate functions such as `COUNT`, `SUM`, `AVG`, `MIN`, and `MAX`

## Required Workflow

Follow these steps in order:

1. Confirm that a SQL query is available.
2. Confirm that a business question or context statement is available. If none is provided, proceed using only the query and note that business context was not provided.
3. Save the SQL query to a `.sql` file if it is not already saved.
4. Run the Python parser script:
```bash
python .agents/skills/sql-insight-auditor/scripts/parse_sql.py inputs/sample_query.sql outputs/parsed_sql_summary.json
```
5. Review the generated parsed summary in:
```text
outputs/parsed_sql_summary.json
```
6. Use the parsed summary as the source of truth for the final explanation.
7. Write the stakeholder-ready query audit using the expected output format below.
8. Save the final audit to:
```text
outputs/stakeholder_explanation.md
```

## Expected Output Format

The final stakeholder-ready audit should use this structure:
```markdown
# SQL Insight Audit

## Business Question

Briefly restate the business question or context provided by the user.

## Query Purpose

Explain the main purpose of the query in plain English.

## Query Logic Summary

Summarize how the query works from start to finish.

## Tables Referenced

List the tables identified by the parser.

## Fields and Metrics

Summarize the selected fields and calculated metrics.

## Joins

Describe any joins used in the query. If no joins are found, state that no joins were identified.

## Filters

List and explain the main filters from the `WHERE` clause.

## Grouping and Ordering

Explain the `GROUP BY` and `ORDER BY` logic, if present.

## Assumptions

List any assumptions needed to interpret the query.

## Risks and Caveats

Identify possible documentation risks, such as missing business context, ambiguous field names, date filters, join behavior, or metrics that require confirmation.

## Stakeholder Summary

Write a concise final explanation that a non-technical stakeholder could understand.
```

## Important Limitations and Checks

- The skill does not execute SQL.
- The skill does not verify that the SQL results are correct.
- The skill does not confirm that the business logic is correct unless the user provides enough context.
- The skill does not connect to any database.
- The skill should not invent table relationships, field definitions, or metric meanings.
- The parsed SQL summary should be treated as the source of truth for structural details.
- If the parser cannot identify a section of the query, say that the section was not identified rather than guessing.
- If the SQL query includes complex nested queries, CTEs, or dialect-specific syntax, mention that the parser may only provide a partial structural summary.
- If business context is missing, the final explanation should clearly state that the explanation is based only on the SQL structure.

## Quality Checklist

Before finalizing the audit, check that:

- The business question is included or its absence is noted.
- Tables referenced in the final audit match the parsed summary.
- Filters referenced in the final audit match the parsed summary.
- Joins referenced in the final audit match the parsed summary.
- Metrics are described cautiously and without unsupported assumptions.
- Risks and caveats are included.
- The final stakeholder summary is written in plain English.