-- How many customers left, and how much monthly revenue left with them?
SELECT
    COUNT(*) AS customers,
    SUM(churned) AS churned_customers,
    ROUND(100.0 * AVG(churned), 1) AS churn_rate_pct,
    ROUND(SUM(monthly_charges), 0) AS total_monthly_revenue,
    ROUND(SUM(CASE WHEN churned = 1 THEN monthly_charges END), 0) AS churned_monthly_revenue,
    ROUND(100.0 * SUM(CASE WHEN churned = 1 THEN monthly_charges END) / SUM(monthly_charges), 1) AS pct_revenue_lost
FROM customers;
