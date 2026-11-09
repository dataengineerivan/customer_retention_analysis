-- When in the customer lifecycle does churn happen?
SELECT
    tenure_band,
    COUNT(*) AS customers,
    SUM(churned) AS churned_customers,
    ROUND(100.0 * AVG(churned), 1) AS churn_rate_pct,
    -- share of all churned customers that fall in this band
    ROUND(100.0 * SUM(churned) / (SELECT SUM(churned) FROM customers), 1) AS pct_of_all_churn
FROM customers
GROUP BY tenure_band
ORDER BY MIN(tenure_months);
