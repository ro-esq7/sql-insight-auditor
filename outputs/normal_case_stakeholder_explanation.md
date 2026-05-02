# SQL Insight Audit

## Business Question

The business context describes this as a normal monthly sales performance summary query. The goal is to translate the SQL logic into a clear explanation for a non-technical audience, including the query purpose, source table, selected fields, metrics, filters, date logic, grouping logic, assumptions, and risks.

## Query Purpose

This query creates a monthly sales performance summary from `customer_transactions_table`. It reports the number of unique customers, number of unique orders, and total revenue for qualifying transactions beginning on January 1, 2025.

## Query Logic Summary

The query selects records from `customer_transactions_table`, filters to transactions with an `order_date` on or after January 1, 2025, and keeps only rows where `product_total_amount` is greater than zero. It groups the remaining records by the month of `order_date`. For each month, it calculates distinct customer count, distinct order count, and total revenue. The final output is ordered by `order_month`.

## Tables Referenced

- `customer_transactions_table`

## Fields and Metrics

- `DATE_TRUNC('month', order_date) AS order_month`: Converts each order date into a monthly reporting period.
- `COUNT(DISTINCT customer_id) AS total_customers`: Counts unique customers in each month.
- `COUNT(DISTINCT order_id) AS total_orders`: Counts unique orders in each month.
- `SUM(product_total_amount) AS total_revenue`: Sums positive product total amounts in each month.

## Joins

No joins were identified by `outputs/normal_case_parsed_summary.json`. The query uses one source table.

## Filters

- `order_date >= '2025-01-01'`: Includes records dated January 1, 2025 or later.
- `product_total_amount > 0`: Includes only records with a positive product total amount.

## Grouping and Ordering

The query groups by:

- `DATE_TRUNC('month', order_date)`

This creates one summary row per order month.

The query orders by:

- `order_month;`

This sorts the monthly summary by the month field.

## Assumptions

- `order_date` is the correct date field for monthly sales reporting.
- `customer_id` reliably identifies unique customers.
- `order_id` reliably identifies unique orders.
- `product_total_amount` is the intended revenue amount for this summary.
- Excluding zero or negative product amounts is intentional for the monthly sales performance view.

## Risks and Caveats

- The parsed summary flagged a date filter. Stakeholders should confirm that January 1, 2025 is the correct start date.
- The query does not include an end date, so results will include all qualifying records from January 1, 2025 through the latest available data when the query runs.
- `total_revenue` is based on `SUM(product_total_amount)`, but the SQL does not define whether this is gross revenue, net revenue, post-discount revenue, or another business-specific revenue definition.
- The `product_total_amount > 0` filter excludes zero and negative amounts, which may remove refunds, returns, adjustments, or no-cost orders if those records exist in the table.
- The parser was not used to execute the SQL or validate result accuracy against a live database.

## Stakeholder Summary

This query produces a monthly sales performance summary beginning January 2025. For each month, it shows how many unique customers placed orders, how many unique orders were recorded, and the total positive product revenue. It is appropriate for a high-level monthly trend view, as long as the reporting start date, revenue definition, and exclusion of non-positive amounts are confirmed.
