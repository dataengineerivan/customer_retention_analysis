-- The segment to target first: new, month-to-month customers paying by electronic check
SELECT
    CASE WHEN contract = 'Month-to-month'
          AND tenure_months <= 12
          AND payment_method = 'Electronic check'
         THEN 'High risk segment' ELSE 'Everyone else' END AS segment,
    COUNT(*) AS customers,
    ROUND(100.0 * AVG(churned), 1) AS churn_rate_pct,
    ROUND(100.0 * SUM(churned) / (SELECT SUM(churned) FROM customers), 1) AS pct_of_all_churn,
    ROUND(SUM(CASE WHEN churned = 1 THEN monthly_charges END), 0) AS churned_monthly_revenue
FROM customers
GROUP BY ALL
ORDER BY segment DESC;
