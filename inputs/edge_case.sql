WITH recent_customers AS (
    SELECT DISTINCT
        customer_id
    FROM customer_transactions_table
    WHERE order_date >= DATE_SUB(CURRENT_DATE(), 1095)
),

historical_customers AS (
    SELECT DISTINCT
        customer_id
    FROM customer_transactions_table
    WHERE order_date < DATE_SUB(CURRENT_DATE(), 1095)
)

SELECT
    COUNT(DISTINCT h.customer_id) AS lapse_customers
FROM historical_customers h
LEFT JOIN recent_customers r
    ON h.customer_id = r.customer_id
WHERE r.customer_id IS NULL;