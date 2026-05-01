# Business Question

The goal is to review each SQL query and translate the query logic into a clear explanation for a non-technical audience.

The SQL Insight Auditor should identify the query purpose, source tables, selected fields, metrics, filters, joins, date logic, grouping logic, assumptions, and risks or limitations.

The three test cases represent:

1. A normal monthly sales performance summary query.
2. An edge case using rolling customer logic, CTEs, and anti-join logic.
3. A cautious case using intentionally unclear SQL patterns, including `SELECT *`, a join without a clear `ON` condition, and mixed `AND` / `OR` logic without parentheses.

*All examples use generic public-safe table and field names.*