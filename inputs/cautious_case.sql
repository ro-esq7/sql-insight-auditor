SELECT * FROM quarterly_sales_table q
JOIN customer_transactions_table c
WHERE sale_date > '2024-01-01'
   OR customer_status = 'active'
   AND revenue > 0
ORDER BY sale_date;