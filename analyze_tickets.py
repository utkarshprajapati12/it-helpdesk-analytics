"""Step 2: Clean helpdesk tickets, check SLA, load into SQLite, run SQL queries."""
import re
import sqlite3

import pandas as pd

# SLA: maximum hours allowed to resolve each priority
SLA_HOURS = {"Critical": 4, "High": 8, "Medium": 24, "Low": 72}

# ---------- 1. Load and clean ----------
df = pd.read_csv("tickets.csv")
print("Raw tickets:", len(df))

df = df.drop_duplicates(subset="ticket_id")
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
df["resolved_at"] = pd.to_datetime(df["resolved_at"], errors="coerce")

# ---------- 2. Calculated columns ----------
df["resolution_hours"] = (df["resolved_at"] - df["created_at"]).dt.total_seconds() / 3600
df["resolution_hours"] = df["resolution_hours"].round(2)
df["sla_hours"] = df["priority"].map(SLA_HOURS)
df["sla_breached"] = (df["resolution_hours"] > df["sla_hours"]).astype(int)
df["created_month"] = df["created_at"].dt.strftime("%Y-%m")

print("Clean tickets:", len(df))

# ---------- 3. Quick pandas summary ----------
print("\n=== Average resolution hours by priority ===")
print(df.groupby("priority")["resolution_hours"].mean().round(1).reindex(["Critical", "High", "Medium", "Low"]))

by_category = (
    df.groupby("category")
    .agg(
        tickets=("ticket_id", "count"),
        avg_hours=("resolution_hours", "mean"),
        sla_breach_pct=("sla_breached", lambda x: 100 * x.mean()),
    )
    .round(1)
    .sort_values("sla_breach_pct", ascending=False)
)
by_category.to_csv("category_summary.csv")
print("\n=== Category summary (saved to category_summary.csv) ===")
print(by_category.to_string())

# ---------- 4. Load into SQLite ----------
conn = sqlite3.connect("tickets.db")
df.to_sql("tickets", conn, if_exists="replace", index=False)

# ---------- 5. Run every query in queries.sql ----------
sql_text = open("queries.sql", encoding="utf-8").read()
parts = re.split(r"-- name:\s*(\w+)\n", sql_text)[1:]
queries = {name: query.strip().rstrip(";") for name, query in zip(parts[::2], parts[1::2])}

for name, query in queries.items():
    result = pd.read_sql(query, conn)
    print(f"\n=== SQL: {name} ===")
    print(result.to_string(index=False))

conn.close()
