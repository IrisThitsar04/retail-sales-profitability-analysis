from pathlib import Path

import pandas as pd
from dagster import asset, MaterializeResult, MetadataValue


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_PATH = PROJECT_ROOT / "data" / "raw" / "Global_Superstore.xls"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "data" / "outputs"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


@asset
def raw_orders() -> pd.DataFrame:
    """Load Orders sheet from raw Global Superstore Excel file."""
    df = pd.read_excel(RAW_PATH, sheet_name="Orders")
    return df


@asset
def cleaned_orders(raw_orders: pd.DataFrame) -> pd.DataFrame:
    """Clean basic data types and remove duplicate rows."""
    df = raw_orders.copy()

    df.columns = df.columns.str.strip()
    df = df.drop_duplicates()

    numeric_cols = ["Sales", "Profit", "Discount", "Shipping Cost"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    required_cols = ["Sales", "Profit", "Discount", "Shipping Cost"]
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    df = df.dropna(subset=required_cols)

    return df

@asset
def engineered_orders(cleaned_orders: pd.DataFrame) -> pd.DataFrame:
    """Create calculated fields used in Tableau dashboards."""
    df = cleaned_orders.copy()

    df["discount_band"] = pd.cut(
        df["Discount"],
        bins=[-0.1, 0, 0.1, 0.2, 0.3, 0.5, 1],
        labels=["0", "1-10%", "10-20%", "20-30%", "30-50%", "50%+"],
    )

    df["Loss"] = df["Profit"].apply(lambda x: x if x < 0 else 0)
    df["Loss_Amount"] = df["Profit"].apply(lambda x: abs(x) if x < 0 else 0)
    df["Positive_Profit"] = df["Profit"].apply(lambda x: x if x > 0 else 0)

    return df


@asset
def tableau_ready_orders(engineered_orders: pd.DataFrame) -> MaterializeResult:
    """Export dashboard-ready dataset for Tableau."""
    output_path = PROCESSED_DIR / "orders_dashboard_dagster_ver.csv"
    engineered_orders.to_csv(output_path, index=False)

    return MaterializeResult(
        metadata={
            "rows": len(engineered_orders),
            "columns": len(engineered_orders.columns),
            "output_path": MetadataValue.path(str(output_path)),
        }
    )


@asset
def summary_metrics(engineered_orders: pd.DataFrame) -> MaterializeResult:
    """Generate KPI summary metrics for validation."""
    df = engineered_orders.copy()
    total_sales =  df["Sales"].sum()
    net_profit = df["Profit"].sum()
    total_transactions = len(df)
    average_discount = df["Discount"].mean()
    total_loss = df["Loss_Amount"].sum()
    total_markets = df["Market"].nunique()
    total_regions = df["Region"].nunique()
    total_countries = df["Country"].nunique()
    average_shipping_cost = df["Shipping Cost"].mean()
    sales_by_markets=df.groupby("Market")["Sales"].sum()
    highest_sales_market = sales_by_markets.idxmax()
    highest_sales_market_value = sales_by_markets.max()
    market_loss_risk=(df.groupby("Market")["Loss_Amount"].sum()/df.groupby("Market")["Sales"].sum())
    highest_loss_risk_market = market_loss_risk.idxmax()
    highest_loss_risk_market_value = market_loss_risk.max()*100

    summary = {
        "total_sales": total_sales,
        "net_profit": net_profit,
        "total_transactions": total_transactions,
        "average_discount": average_discount,
        "total_loss": total_loss,
        "total_markets": total_markets,
        "total_regions": total_regions,
        "total_countries": total_countries,
        "average_shipping_cost": average_shipping_cost,
        "highest_sales_market": highest_sales_market,
        "highest_sales_market_value": highest_sales_market_value,
        "highest_loss_risk_market": highest_loss_risk_market,
        "highest_loss_risk_market_value": highest_loss_risk_market_value
    }

    summary_df = pd.DataFrame([summary])

    output_path = OUTPUTS_DIR / "summary_metrics.csv"
    summary_df.to_csv(output_path, index=False)

    return MaterializeResult(
    metadata={
        "output_path": MetadataValue.path(str(output_path)),
        "total_sales": float(round(total_sales, 2)),
        "net_profit": float(round(net_profit, 2)),
        "total_loss": float(round(total_loss, 2)),
        "average_discount": float(round(average_discount, 4)),
        "average_shipping_cost": float(round(average_shipping_cost, 2)),
        "total_transactions": int(total_transactions),
        "total_markets": int(total_markets),
        "total_regions": int(total_regions),
        "total_countries": int(total_countries),
        "highest_sales_market": str(highest_sales_market),
        "highest_sales_market_value": float(round(highest_sales_market_value, 2)),
        "highest_loss_risk_market": str(highest_loss_risk_market),
        "highest_loss_risk_market_value": float(round(highest_loss_risk_market_value, 2)),
    }
)