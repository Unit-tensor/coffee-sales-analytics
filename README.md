# ☕ Coffee Shop Sales Analytics

End-to-end sales analysis and dashboard project for a 3-location NYC
coffee shop chain covering 149,116 transactions from January–June 2023.

## 📌 Project Overview

Analyzed 6 months of point-of-sale data to uncover revenue trends,
peak traffic windows, top-performing products, and store-level performance.
Delivered findings as both an interactive HTML dashboard and a structured
Excel analytics workbook.

## 📷 Preview

![Dashboard Preview](coffee-shop-sales-analytics/assets/dashboard_preview.jpg)

## 📁 Project Structure

```
coffee-shop-sales-analytics/
│
├── README.md
└── project/
    ├── data/
    │   └── Coffee_Shop_Sales.xlsx          ← raw transaction dataset (149K rows)
    ├── analysis/
    │   └── coffee_analysis.py              ← pandas analysis script
    ├── output/
    │   ├── Coffee_Shop_Analytics.xlsx      ← 5-sheet Excel workbook (221 live formulas)
    │   └── coffee_shop_dashboard.html      ← interactive HTML dashboard
    └── assets/
        └── dashboard_preview.jpg           ← dashboard screenshot
```

## 📊 Key Findings

- **$698.8K total revenue** across Astoria, Hell's Kitchen, and Lower Manhattan
- Revenue grew **103% from Jan → Jun** ($81.7K to $166.5K)
- **Peak hours: 8–10 AM** — account for ~36% of daily revenue
- **Coffee (38.6%)** and **Tea (28.1%)** dominate category revenue
- All 3 stores perform within **2.8% of each other** in revenue — highly balanced
- **Friday** is the strongest weekday; **Saturday** is the slowest

## 🛠 Tools & Stack

| Tool | Purpose |
|------|---------|
| Python (pandas) | Data cleaning, aggregation, analysis |
| openpyxl | Excel workbook creation with live formulas |
| Chart.js | Interactive HTML dashboard |
| Excel | Formula recalculation & verification |

## 📋 Excel Workbook — Sheet Breakdown

| Sheet | Contents |
|-------|---------|
| 📊 Dashboard | KPI cards, monthly summary table, store comparison |
| 🛒 Product Analysis | Top 20 products, category breakdown with color scale |
| ⏰ Time Analysis | Hourly traffic, weekday patterns, peak hours highlighted |
| 🏪 Store Deep Dive | Month-over-month revenue by location, indexed trend |
| 📋 Raw Data (Sample) | 1,000 filterable transactions with AutoFilter |

## 🚀 How to Run

1. Clone the repo:
```bash
git clone https://github.com/Unit-tensor/coffee-shop-sales-analytics.git
cd coffee-shop-sales-analytics
```

2. Install dependencies:
```bash
pip install pandas openpyxl
```

3. Run the analysis:
```bash
python coffee-shop-sales-analytics/analysis/coffee_analysis.py
```

4. Open the dashboard:
```
Open coffee-shop-sales-analytics/output/coffee_shop_dashboard.html in any browser
```

## 📦 Dataset

- **Source:** Coffee_Shop_Sales.xlsx
- **Period:** January 1 – June 30, 2023
- **Rows:** 149,116 transactions
- **Stores:** Astoria · Hell's Kitchen · Lower Manhattan
- **Fields:** Transaction ID, Date, Time, Quantity, Store, Product, Unit Price, Category
