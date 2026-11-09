"""Download the IBM Telco Customer Churn sample data and load a cleaned table into DuckDB."""
from pathlib import Path
from urllib.request import urlretrieve
import duckdb

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "telco_customer_churn.csv"
DB = ROOT / "data" / "churn.duckdb"
URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"


def main():
    RAW.parent.mkdir(exist_ok=True)
    if not RAW.exists():
        print("Downloading data...")
        urlretrieve(URL, RAW)

    con = duckdb.connect(str(DB))
    con.execute(f"""
        CREATE OR REPLACE TABLE customers AS
        SELECT
            customerID AS customer_id,
            gender,
            SeniorCitizen = 1 AS is_senior,
            Partner = 'Yes' AS has_partner,
            Dependents = 'Yes' AS has_dependents,
            tenure AS tenure_months,
            -- group tenure so churn can be compared across customer age
            CASE WHEN tenure <= 6 THEN '0-6 months'
                 WHEN tenure <= 12 THEN '7-12 months'
                 WHEN tenure <= 24 THEN '13-24 months'
                 WHEN tenure <= 48 THEN '25-48 months'
                 ELSE '49+ months' END AS tenure_band,
            PhoneService AS phone_service,
            InternetService AS internet_service,
            OnlineSecurity AS online_security,
            TechSupport AS tech_support,
            Contract AS contract,
            PaperlessBilling = 'Yes' AS paperless_billing,
            PaymentMethod AS payment_method,
            MonthlyCharges AS monthly_charges,
            -- brand-new customers have a blank total; treat it as missing, not zero
            TRY_CAST(NULLIF(TRIM(CAST(TotalCharges AS VARCHAR)), '') AS DOUBLE) AS total_charges,
            CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END AS churned
        FROM read_csv('{RAW}', header=true, all_varchar=false)
    """)
    rows, churned = con.execute("SELECT COUNT(*), SUM(churned) FROM customers").fetchone()
    blanks = con.execute("SELECT COUNT(*) FROM customers WHERE total_charges IS NULL").fetchone()[0]
    print(f"Loaded {rows:,} customers, {churned:,} churned, {blanks} with blank total charges")
    con.close()


if __name__ == "__main__":
    main()
