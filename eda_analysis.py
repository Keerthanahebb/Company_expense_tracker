import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

# ================= DB CONNECTION =================
load_dotenv()

# password = quote_plus(os.getenv("DB_PASSWORD"))

# engine = create_engine(
#     f"postgresql+psycopg2://postgres:{password}@localhost/expense _tracker"
#     # ⚠️ change password if different
# )

from sqlalchemy.engine import URL

url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password=os.getenv("DB_PASSWORD"),
    host="localhost",
    database="expense_tracker",
)

engine = create_engine(url)

# ================= LOAD DATA =================
query = """
SELECT 
    e.expense_id,
    e.amount,
    e.description,
    e.expense_date,
    e.payment_method,
    emp.employee_name,
    d.dept_name,
    c.category_name
FROM expenses e
JOIN employees emp ON e.employee_id = emp.employee_id
JOIN departments d ON emp.dept_id = d.dept_id
JOIN expense_categories c ON e.category_id = c.category_id
"""

df = pd.read_sql(query, engine)

# print("Data shape:", df.shape)
# print(df.head())

# ================= CLEANING =================
df["expense_date"] = pd.to_datetime(df["expense_date"])
df["month"] = df["expense_date"].dt.to_period("M").astype(str)

# print(df.columns)
# print(df.head())

# ================= EDA 1 — Monthly Spend =================
monthly_spend = df.groupby("month")["amount"].sum().reset_index()

plt.figure(figsize=(10,5))
sns.lineplot(data=monthly_spend, x="month", y="amount")
plt.xticks(rotation=45)
plt.title("Monthly Company Spending")
plt.tight_layout()
plt.show()

# ================= EDA 2 — Category Distribution =================
plt.figure(figsize=(8,5))
sns.barplot(
    data=df.groupby("category_name")["amount"].sum().reset_index(),
    x="category_name",
    y="amount"
)
plt.xticks(rotation=45)
plt.title("Spend by Category")
plt.tight_layout()
plt.show()

# ================= EDA 3 — Department Spend =================
plt.figure(figsize=(8,5))
sns.barplot(
    data=df.groupby("dept_name")["amount"].sum().reset_index(),
    x="dept_name",
    y="amount"
)
plt.xticks(rotation=45)
plt.title("Spend by Department")
plt.tight_layout()
plt.show()

print("✅ EDA completed")