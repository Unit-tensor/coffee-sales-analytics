import pandas as pd
import json

# load the data
df = pd.read_excel("data/Coffee_Shop_Sales.xlsx")
print(df.shape)
print(df.columns.tolist())
print(df.dtypes)

# %%
print(df.head())
print(df.isnull().sum())

# revenue col doesn't exist so making it
df["revenue"] = df["transaction_qty"] * df["unit_price"]

# transaction_time is datetime.time object, pulling out just the hour
df["hour"] = df["transaction_time"].apply(lambda x: x.hour if hasattr(x, "hour") else int(float(str(x)) * 24))

df["month_num"] = df["transaction_date"].dt.month
df["month_name"] = df["transaction_date"].dt.strftime("%b")
df["weekday"] = df["transaction_date"].dt.day_name()
df["weekday_num"] = df["transaction_date"].dt.dayofweek

print(df["hour"].value_counts().sort_index())


# quick overall numbers
total_rev = df["revenue"].sum()
total_txns = len(df)
avg_order = df["revenue"].mean()

print(f"total revenue: {total_rev:.2f}")
print(f"transactions: {total_txns}")
print(f"avg order: {avg_order:.2f}")


# monthly breakdown
monthly = (
    df.groupby(["month_num", "month_name"])
    .agg(
        transactions=("transaction_id", "count"),
        revenue=("revenue", "sum"),
        avg_order=("revenue", "mean")
    )
    .reset_index()
    .sort_values("month_num")
)

monthly["mom_pct"] = monthly["revenue"].pct_change() * 100
monthly["rev_share"] = monthly["revenue"] / monthly["revenue"].sum() * 100

print(monthly)

# %%
# store level
store = (
    df.groupby("store_location")
    .agg(
        transactions=("transaction_id", "count"),
        revenue=("revenue", "sum"),
        avg_order=("revenue", "mean")
    )
    .reset_index()
    .sort_values("revenue", ascending=False)
)

store["rev_share"] = store["revenue"] / store["revenue"].sum() * 100
print(store)


# categories - curious how coffee vs tea splits
cat = (
    df.groupby("product_category")
    .agg(transactions=("transaction_id", "count"), revenue=("revenue", "sum"))
    .reset_index()
    .sort_values("revenue", ascending=False)
)

cat["rev_share"] = cat["revenue"] / cat["revenue"].sum() * 100
cat["avg_rev_per_txn"] = cat["revenue"] / cat["transactions"]
print(cat)


# top products
top_prods = (
    df.groupby("product_detail")
    .agg(transactions=("transaction_id", "count"), revenue=("revenue", "sum"))
    .reset_index()
    .sort_values("revenue", ascending=False)
    .head(20)
    .reset_index(drop=True)
)

top_prods["rank"] = range(1, 21)
top_prods["avg_price"] = top_prods["revenue"] / top_prods["transactions"]
print(top_prods[["rank", "product_detail", "revenue", "avg_price"]].head(10))


# hourly - want to see the morning rush
hourly = (
    df.groupby("hour")
    .agg(transactions=("transaction_id", "count"), revenue=("revenue", "sum"))
    .reset_index()
)

hourly["rev_share"] = hourly["revenue"] / hourly["revenue"].sum() * 100
hourly["avg_per_txn"] = hourly["revenue"] / hourly["transactions"]

# peak hours check
peak = hourly[hourly["hour"].between(8, 10)]["revenue"].sum()
total_hourly = hourly["revenue"].sum()
print(f"8-10am share: {peak/total_hourly*100:.1f}%")

print(hourly)


# weekday
weekday = (
    df.groupby(["weekday_num", "weekday"])
    .agg(transactions=("transaction_id", "count"), revenue=("revenue", "sum"))
    .reset_index()
    .sort_values("weekday_num")
)

weekday["avg_order"] = weekday["revenue"] / weekday["transactions"]
weekday["rev_share"] = weekday["revenue"] / weekday["revenue"].sum() * 100
print(weekday)


# monthly by store - for the deep dive sheet
store_monthly = (
    df.groupby(["month_num", "month_name", "store_location"])["revenue"]
    .sum()
    .reset_index()
)

pivot = store_monthly.pivot(
    index=["month_num", "month_name"],
    columns="store_location",
    values="revenue"
).reset_index()

pivot.columns.name = None
pivot["total"] = pivot[["Astoria", "Hell's Kitchen", "Lower Manhattan"]].sum(axis=1)

# mom for each store
for col in ["Astoria", "Hell's Kitchen", "Lower Manhattan", "total"]:
    pivot[f"{col}_mom"] = pivot[col].pct_change() * 100

print(pivot)


# saving data as json so the html dashboard can read it
# TODO: could probably do this cleaner but works for now

out = {
    "kpis": {
        "total_revenue": round(total_rev, 2),
        "total_transactions": total_txns,
        "avg_order_value": round(avg_order, 2),
        "best_month": monthly.loc[monthly["revenue"].idxmax(), "month_name"],
        "best_month_revenue": round(monthly["revenue"].max(), 2),
    },
    "monthly": [
        {
            "month": r["month_name"],
            "transactions": int(r["transactions"]),
            "revenue": round(r["revenue"], 2),
            "avg_order": round(r["avg_order"], 2),
            "mom_pct": round(r["mom_pct"], 2) if pd.notna(r["mom_pct"]) else None,
        }
        for _, r in monthly.iterrows()
    ],
    "stores": [
        {
            "name": r["store_location"],
            "transactions": int(r["transactions"]),
            "revenue": round(r["revenue"], 2),
            "avg_order": round(r["avg_order"], 2),
            "rev_share": round(r["rev_share"], 2),
        }
        for _, r in store.iterrows()
    ],
    "categories": [
        {
            "name": r["product_category"],
            "transactions": int(r["transactions"]),
            "revenue": round(r["revenue"], 2),
            "rev_share": round(r["rev_share"], 2),
        }
        for _, r in cat.iterrows()
    ],
    "top_products": [
        {
            "rank": int(r["rank"]),
            "name": r["product_detail"],
            "transactions": int(r["transactions"]),
            "revenue": round(r["revenue"], 2),
            "avg_price": round(r["avg_price"], 2),
        }
        for _, r in top_prods.iterrows()
    ],
    "hourly": [
        {
            "hour": int(r["hour"]),
            "transactions": int(r["transactions"]),
            "revenue": round(r["revenue"], 2),
            "rev_share": round(r["rev_share"], 2),
        }
        for _, r in hourly.iterrows()
    ],
    "weekday": [
        {
            "day": r["weekday"],
            "transactions": int(r["transactions"]),
            "revenue": round(r["revenue"], 2),
            "avg_order": round(r["avg_order"], 2),
        }
        for _, r in weekday.iterrows()
    ],
    "store_monthly": [
        {
            "month": r["month_name"],
            "Astoria": round(r["Astoria"], 2),
            "Hells_Kitchen": round(r["Hell's Kitchen"], 2),
            "Lower_Manhattan": round(r["Lower Manhattan"], 2),
            "Total": round(r["total"], 2),
        }
        for _, r in pivot.iterrows()
    ],
}

with open("output/dashboard_data.json", "w") as f:
    json.dump(out, f, indent=2)

print("saved to output/dashboard_data.json")
