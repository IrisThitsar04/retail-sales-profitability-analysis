# Retail Sales and Profitability Analysis Project

## Project Overview

This project analyses the Global Superstore Orders dataset to understand retail sales performance, profitability patterns, discount impact, and loss drivers across customer segments, markets, product categories, shipping modes, and individual transactions. The project combines exploratory data analysis, dashboard development, and data orchestration to create a repeatable analytics workflow.

The main goal is to understand where the business generates strong profitability and where profit erosion occurs, especially across markets, product categories, discount levels, and shipping costs.

The project includes:

- Exploratory data analysis using Jupyter Notebook
- Data preparation and feature engineering using Python and pandas
- Tableau dashboard development for business insights
- Dagster data orchestration for automated pipeline execution
- KPI validation using Dagster-generated summary metrics

---

## Business Problem

Retail organisations often generate sales across multiple regions, markets, product categories, and customer segments. However, high sales do not always mean high profitability and does not guarantee strong business performance if certain transactions, products, or regions are creating losses.

This project investigates the following business questions:

- Which customer segments generate the highest sales and profit?
- Which markets are the strongest and weakest in terms of profitability?
- Which product categories and sub-categories contribute most to profit loss?
- How does discounting affect profitability?
- Which shipping modes are most commonly used across markets?
- Which transactions create the highest losses?
- What areas should the business review to reduce profit erosion?

---

## Dataset

The project uses the **Global Superstore** dataset.

The main dataset used for analysis is the **Orders** sheet from the raw Excel file.

The People and Returns sheets were briefly inspected for context, but the main analysis, dashboard, and pipeline outputs are based on the Orders dataset.

---

## Project Structure

```text
Retail_Profitability_Analysis_Project/
│
├── data/
│   ├── raw/
│   │   └── Global_Superstore.xls
│   │
│   ├── processed/
│   │   ├── orders_dashboard_dagster_ver.csv
│   │   └── orders_dashboard_notebook_ver.csv
│   └── outputs/
│       └── summary_metrics.csv
│
├── notebook/
│   └── retail_profitability_eda.ipynb
│
├── pipeline/
│   ├── __init__.py
│   ├── assets.py
│   └── definitions.py
│
├── dashboards/
│   ├── Market_and_Shipping_Analysis_Dashboard.png
│   └── Profitability_and_Discount_Dashboard.png
│
├── tableau_workbook/
│   └── Retail_Sales_Profitability_Dashboard.twbx
│
├── dagster_screenshots/
│   ├── Figure 1/ Dagster Asset Graph.png
│   ├── Figure 2/ Successful Dagster Materialization Run.png
│   ├── Figure 3/ Tableau-Ready Dataset Metadata.png
│   ├── Figure 4/ Summary Metrics Metadata.png
│   ├── Figure 5/ Generated Summary Metrics File.png
│   ├── Figure 6/ Summary Metrics CSV Output.png
│   └── Figure 7/ Notebook and Dagster Output Files.png
│
├── README.md
└── requirements.txt
```

---

## Tools and Technologies

| Tool             | Purpose                                             |
| ---------------- | --------------------------------------------------- |
| Python           | Data analysis and transformation                    |
| pandas           | Data cleaning, feature engineering, KPI calculation |
| Jupyter Notebook | Exploratory data analysis and calculation testing   |
| Tableau          | Dashboard development and visualisation             |
| Dagster          | Data orchestration and pipeline monitoring          |
| Excel/CSV        | Raw input and processed output files                |


---

## Project Workflow

The project follows this workflow:

1. **Raw Excel Dataset**  
   The original Superstore Excel dataset is used as the starting point.

2. **Jupyter Notebook EDA**  
   The Jupyter Notebook is used for exploration, data quality checks, KPI development, and initial business analysis.

3. **Tableau Dashboard**  
   Tableau is used to visualise sales, profit, loss, discount, category, market, and segment insights.

4. **Dagster Pipeline**  
   After the analysis logic is confirmed, Dagster is used to convert the key workflow steps into an automated and repeatable data pipeline.

5. **Processed Tableau-Ready Dataset**  
   The cleaned and modified dataset is exported for dashboard development.

6. **Dagster KPI Validation**  
   Dagster is used to validate important KPI outputs and improve reliability of the workflow.

---
## Jupyter Notebook

Notebook file: `notebook/retail_profitability_eda.ipynb`

The notebook includes:

- Dataset loading and initial inspection
- Data quality checks, including data types, missing values, and duplicates
- Feature creation for analysis and dashboard use, including loss, positive profit, and discount band columns
- Segment, market, category, and sub-category profitability analysis
- Shipping mode analysis across markets and order priorities
- Discount impact analysis across overall sales and product categories
- Market profitability risk analysis using loss percentage of sales
- Transaction-level review of highest loss-making and profit-generating orders
- Summary findings with business recommendations
- Export of the modified Orders dataset for Tableau dashboard development
  
---

## Key Analysis Areas

### Segment Analysis

The analysis examines sales, profit, order volume, average profit, and total loss across customer segments.

### Market Analysis

The project compares sales, profit, order count, and profitability risk across different markets such as APAC, EU, US, LATAM, EMEA, Africa, and Canada.

### Shipping Mode Analysis

Shipping mode usage is analysed across markets to understand customer delivery preferences and how they relate to order priority.

### Category and Sub-Category Analysis

The project identifies which product categories and sub-categories generate the highest sales, profit, and losses.

### Discount Analysis

Discount levels are analysed to understand their impact on profitability. Discount bands are created to compare profit performance across different discount ranges.

### Market Profitability Risk

Loss percentage of sales is calculated by market to identify regions with higher exposure to margin erosion.

### Transaction-Level Analysis

The project compares the top loss-making transactions and top profit-generating transactions to identify patterns linked to high losses and strong profitability.

---

## Feature Engineering

Additional columns are created to support analysis and dashboard development:

```python
orders['Loss'] = orders['Profit'].apply(lambda x: x if x < 0 else 0)
orders['Positive Profit'] = orders['Profit'].apply(lambda x: x if x > 0 else 0)
orders['discount_bands'] = pd.cut(
    orders['Discount'],
    bins=[-0.1, 0.1, 0.3, 0.5, 0.7, 1],
    labels=['0-10%', '10-30%', '30-50%', '50-70%', '70%+']
)
```
These features make the dataset easier to use in dashboard tools.


## Tableau Dashboards

Two Tableau dashboards were developed using the processed Orders dataset prepared from the Global Superstore data. The dashboards focus on profitability, discount impact, market performance, and shipping behaviour.

### Dashboard 1: Profitability and Discount Performance Analysis

This dashboard provides an overview of business profitability and identifies the main drivers of sales, profit, and loss. It focuses on customer segments, product categories, discount bands, and transaction-level loss patterns.

**KPIs Included:**
- Total Sales
- Net Profit
- Total Transactions
- Average Discount
- Total Loss

**Charts Included:**
- Category Performance by selected metric: Total Sales, Net Profit, or Total Loss Amount
- Top Loss-Making Sub Categories
- Profit by Discount Band
- Sales and Profit by Segment, including Total Sales, Net Profit, Average Profit per Transaction, and Total Loss Amount
- Top 10 Loss-Making Transactions

### Dashboard 2: Market and Shipping Analysis

This dashboard analyses geographic performance, market-level risk, and shipping behaviour. It compares market profitability, identifies high-risk markets, and shows how shipping mode usage varies across markets and order priorities.

**KPIs Included:**
- Total Markets
- Total Countries
- Average Shipping Cost
- Highest Sales Market
- Highest Risk Market

**Charts Included:**
- Geographic Map by selected metric: Total Sales, Transaction Count, Net Profit, or Profit Loss
- Loss Percentage of Sales by Market
- Ship Mode Distribution by selected view: Market or Order Priority
- Sales, Profit, and Profit Margin by Market

---

## Dagster Data Orchestration

Dagster was used to automate the data preparation and validation workflow.

The pipeline is defined using Dagster assets in:
`pipeline/assets.py`

The Dagster project is registered in:
`pipeline/definitions.py`

### Asset Flow

| Asset                  | Purpose                                                                   |
| ---------------------- | ------------------------------------------------------------------------- |
| `raw_orders`           | Loads the Orders sheet from the raw Global Superstore Excel file          |
| `cleaned_orders`       | Performs basic validation, numeric conversion, and missing-value handling |
| `engineered_orders`    | Creates reusable calculated fields for analysis and dashboard preparation |
| `tableau_ready_orders` | Exports the processed dataset for Tableau                                 |
| `summary_metrics`      | Generates KPI values for dashboard validation                             |
---

### Data Cleaning and Validation

The pipeline performs basic validation steps to ensure the required fields are suitable for analysis.

The required numeric columns include:
- Sales
- Profit
- Discount
- Shipping Cost
The pipeline checks that these columns exist, converts them to numeric format, and removes rows with missing or invalid values in these required fields.

Although the Jupyter Notebook confirmed that the dataset was already mostly clean, these checks were included in the Dagster pipeline as defensive validation steps. This makes the workflow more reliable if the dataset is updated in the future.


### Feature Engineering

The pipeline creates additional fields used for analysis and dashboard preparation.

| Field             | Description                                                                |
| ----------------- | -------------------------------------------------------------------------- |
| `discount_band`   | Groups discount values into bands such as No Discount, 1-10%, 10-20%, etc. |
| `Loss`            | Keeps negative profit values and assigns 0 to profitable transactions      |
| `Loss_Amount`     | Converts negative profit values into positive loss amounts                 |
| `Positive_Profit` | Keeps positive profit values and assigns 0 to loss-making transactions     |

These fields support clearer analysis of profitability, discount impact, and loss-making transactions.

---

KPI Validation with Dagster

The summary_metrics asset was created to cross-check the KPI values shown in Tableau.

The summary metrics output is saved to:

`data/outputs/summary_metrics.csv`

The KPI values are also shown in the Dagster UI metadata after materialization.

This allows the Tableau dashboard values to be compared against independently calculated pipeline values.

---

### Output Files

The pipeline generates two main output files.

| Output File                                 | Purpose                                                    |
| ------------------------------------------- | ---------------------------------------------------------- |
| `data/processed/orders_dashboard_ready.csv` | Processed dataset for Tableau dashboard development        |
| `data/outputs/summary_metrics.csv`          | KPI summary file used to validate Tableau dashboard values |

---

## Running the Dagster Pipeline

From the project root folder, activate the virtual environment and run:

```python dagster dev -f pipeline/definitions.py```

In the Dagster UI:

Go to the Assets page
Select all assets
Click Materialize selected
Confirm that all assets complete successfully
Check metadata for tableau_ready_orders and summary_metrics

## Screenshots 

Screenshots including the evidence of Dagster include:

- Dagster asset graph
- Successful materialization run
- tableau-ready dataset metadata
- summary metrics metadata
- Generated summary metrics file
- summary metrics csv output
- notebook and dagster output files

These screenshots demonstrate that the workflow was successfully executed and that the dashboard outputs were validated against the Dagster pipeline.
