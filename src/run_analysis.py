"""Run every query in sql/, save the results as CSVs, and draw the charts used in the README."""
from pathlib import Path
import duckdb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "churn.duckdb"
OUT = ROOT / "outputs"
CHARTS = OUT / "charts"
BLUE, RED = "#2f6690", "#c0392b"


def bar_chart(df, x, y, title, path, highlight_max=True):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = [RED if (highlight_max and v == df[y].max()) else BLUE for v in df[y]]
    bars = ax.bar(df[x].astype(str), df[y], color=colors)
    ax.bar_label(bars, labels=[f"{v:.1f}%" for v in df[y]], padding=3)
    ax.set_title(title, fontsize=13, loc="left")
    ax.set_ylabel("Churn rate (%)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_ylim(0, df[y].max() * 1.2)
    plt.xticks(rotation=15 if df[x].astype(str).str.len().max() > 12 else 0)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main():
    CHARTS.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB), read_only=True)

    results = {}
    for sql_file in sorted((ROOT / "sql").glob("*.sql")):
        df = con.execute(sql_file.read_text()).df()
        results[sql_file.stem] = df
        df.to_csv(OUT / f"{sql_file.stem}.csv", index=False)
        print(f"\n== {sql_file.stem}\n{df.to_string(index=False)}")

    bar_chart(results["02_churn_by_contract"], "contract", "churn_rate_pct",
              "Churn rate by contract type", CHARTS / "churn_by_contract.png")
    bar_chart(results["03_churn_by_tenure"], "tenure_band", "churn_rate_pct",
              "Churn rate by customer tenure", CHARTS / "churn_by_tenure.png")
    bar_chart(results["04_churn_by_payment"], "payment_method", "churn_rate_pct",
              "Churn rate by payment method", CHARTS / "churn_by_payment.png")

    # one flat file with every customer, for building the dashboard in Tableau Public
    con.execute(f"COPY customers TO '{OUT / 'customers_clean.csv'}' (HEADER)")
    print(f"\nSaved results and charts to {OUT}")


if __name__ == "__main__":
    main()
