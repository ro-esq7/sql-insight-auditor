SELECT
    DATE_TRUNC('month', order_date) AS order_month,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(product_total_amount) AS total_revenue
FROM customer_transactions_table
WHERE order_date >= '2025-01-01'
  AND product_total_amount > 0
GROUP BY
    DATE_TRUNC('month', order_date)
ORDER BY
    order_month;