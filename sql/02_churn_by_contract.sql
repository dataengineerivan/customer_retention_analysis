-- Does contract length change how likely a customer is to leave?
SELECT
    contract,
    COUNT(*) AS customers,
    SUM(churned) AS churned_customers,
    ROUND(100.0 * AVG(churned), 1) AS churn_rate_pct
FROM customers
GROUP BY contract
ORDER BY churn_rate_pct DESC;
