# SQL Insight Audit

## Business Question

The business context describes this as the edge-case query, using rolling customer logic, CTEs, and anti-join logic. The goal is to translate the SQL into a clear explanation for a non-technical audience while identifying source tables, fields, metrics, filters, joins, date logic, assumptions, and risks or limitations.

## Query Purpose

This query appears intended to count customers who had historical activity but do not have recent activity. In business terms, it is likely estimating lapsed customers using a rolling date cutoff.

## Query Logic Summary

The parsed summary identifies `customer_transactions_table` as the underlying source table and also identifies two table-like references, `historical_customers` and `recent_customers`, which are CTEs in the SQL. The visible SQL builds one CTE for recent customers and another for historical customers, then compares those two customer sets.

The final query uses a `LEFT JOIN` from historical customers to recent customers on `customer_id`. It then filters to rows where the recent customer match is null. This pattern is commonly used to find records that exist in one group but not another. In this case, it means customers who appear historically but not recently.

## Tables Referenced

The parser identified these references:

- `customer_transactions_table`
- `historical_customers`
- `recent_customers`

`historical_customers` and `recent_customers` are CTEs rather than physical source tables. The physical source table visible in the SQL is `customer_transactions_table`.

## Fields and Metrics

The parsed summary identified this selected field:

- `DISTINCT customer_id`

The parsed summary did not identify any aggregate metrics. This is a parser limitation for this CTE-based query. Manual review of the visible SQL shows a final expression:

- `COUNT(DISTINCT h.customer_id) AS lapse_customers`

Because this metric was not captured in `outputs/edge_case_parsed_summary.json`, it should be treated as manually observed SQL context rather than parser-extracted metric metadata.

## Joins

The parser identified this join:

- `LEFT JOIN recent_customers r ON h.customer_id = r.customer_id`

This join compares historical customers to recent customers by `customer_id`. The visible `WHERE r.customer_id IS NULL` condition makes the join behave like an anti-join, keeping historical customers who do not have a matching recent customer record.

## Filters

The parser identified one long filter expression:

- `order_date >= DATE_SUB(CURRENT_DATE(), 1095) ), historical_customers AS ( SELECT DISTINCT customer_id FROM customer_transactions_table WHERE order_date < DATE_SUB(CURRENT_DATE(), 1095) ) SELECT COUNT(DISTINCT h.customer_id) AS lapse_customers FROM historical_customers h LEFT JOIN recent_customers r ON h.customer_id = r.customer_id WHERE r.customer_id IS NULL;`

This long filter is a limitation caused by the CTE structure. Manual review of the SQL shows the main logical filters are:

- `order_date >= DATE_SUB(CURRENT_DATE(), 1095)`: Defines the recent-customer group using a rolling date window.
- `order_date < DATE_SUB(CURRENT_DATE(), 1095)`: Defines the historical-customer group before that same rolling cutoff.
- `r.customer_id IS NULL`: Keeps only historical customers who do not appear in the recent-customer group.

## Grouping and Ordering

The parser did not identify any `GROUP BY` fields.

The parser did not identify any `ORDER BY` fields.

The visible SQL also does not show grouping or ordering in the final query. It appears intended to return one overall count rather than a grouped report.

## Assumptions

- `customer_id` reliably identifies the same customer across historical and recent records.
- `order_date` is the correct date field for determining whether a customer is recent or historical.
- `DATE_SUB(CURRENT_DATE(), 1095)` is the intended rolling cutoff for the business definition.
- The value `1095` is intended to approximate a three-year window.
- A customer with activity before the rolling cutoff and no activity on or after the cutoff should be considered lapsed.

## Risks and Caveats

- The parser is intentionally lightweight and only partially captured this CTE-based query. It flattened CTE logic into one long filter and did not identify the final `COUNT(DISTINCT h.customer_id)` expression as an aggregate metric.
- The rolling date logic depends on `CURRENT_DATE()`, so the result can change depending on the day the query is run.
- The `1095`-day cutoff should be confirmed with stakeholders because it may not exactly match a business definition such as "three years," especially around leap years.
- The anti-join logic depends on `LEFT JOIN recent_customers r ON h.customer_id = r.customer_id` plus `WHERE r.customer_id IS NULL`. If customer identifiers are missing, duplicated, changed, or inconsistent, the lapsed-customer count may be unreliable.
- The query only considers whether a customer had activity before or after the cutoff. It does not account for customer status, account closures, refunds, cancellations, revenue thresholds, or other business rules that might affect a lapsed-customer definition.
- The SQL was not executed, and this audit does not validate whether the returned count is correct against a database.

## Stakeholder Summary

This query appears to count customers who had older transaction activity but no recent transaction activity. It uses a rolling date cutoff to separate recent and historical customers, then uses a left join anti-join pattern to find historical customers missing from the recent group. The result is likely a lapsed-customer count, but the CTE parsing limitations, rolling date definition, join behavior, and customer identifier quality should be confirmed before using the result as an official retention or lifecycle metric.
