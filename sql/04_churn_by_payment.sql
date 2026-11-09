-- Are some payment methods tied to higher churn?
SELECT
    payment_method,
    COUNT(*) AS customers,
    ROUND(100.0 * AVG(churned), 1) AS churn_rate_pct
FROM customers
GROUP BY payment_method
ORDER BY churn_rate_pct DESC;
