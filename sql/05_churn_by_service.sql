-- For internet customers, do support add-ons go with lower churn?
SELECT
    internet_service,
    tech_support,
    online_security,
    COUNT(*) AS customers,
    ROUND(100.0 * AVG(churned), 1) AS churn_rate_pct
FROM customers
WHERE internet_service <> 'No'
GROUP BY ALL
HAVING COUNT(*) >= 100
ORDER BY churn_rate_pct DESC;
