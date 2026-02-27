import random
import psycopg2
from faker import Faker

fake = Faker()

# ================= DB CONNECTION =================
conn = psycopg2.connect(
    host="localhost",
    database="expense_tracker",
    user="postgres",
    password="Hebb#kee@123"  # ⚠️ CHANGE if your password is different
)
conn.autocommit = True
cur = conn.cursor()

# ================= CONFIG =================
NUM_EMPLOYEES = 50
NUM_EXPENSES = 5000

payment_methods = ["Credit Card", "UPI", "Cash", "Debit Card"]
categories = ["Travel", "Food", "Office Supplies", "Software", "Client Meeting"]
departments = ["Engineering", "Marketing", "HR", "Finance", "Sales"]

# ================= INSERT DEPARTMENTS =================
cur.execute("SELECT COUNT(*) FROM departments;")
if cur.fetchone()[0] == 0:
    for dept in departments:
        budget = random.randint(200000, 800000)
        cur.execute(
            "INSERT INTO departments (dept_name, monthly_budget) VALUES (%s, %s)",
            (dept, budget),
        )

# ================= INSERT CATEGORIES =================
cur.execute("SELECT COUNT(*) FROM expense_categories;")
if cur.fetchone()[0] == 0:
    for cat in categories:
        cur.execute(
            "INSERT INTO expense_categories (category_name) VALUES (%s)",
            (cat,),
        )

# ================= GET IDS =================
cur.execute("SELECT dept_id FROM departments")
dept_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT category_id FROM expense_categories")
category_ids = [row[0] for row in cur.fetchall()]

# ================= INSERT EMPLOYEES =================
cur.execute("SELECT COUNT(*) FROM employees;")
if cur.fetchone()[0] == 0:
    for _ in range(NUM_EMPLOYEES):
        name = fake.name()
        email = fake.unique.email()
        dept_id = random.choice(dept_ids)
        join_date = fake.date_between(start_date="-3y", end_date="today")

        cur.execute(
            """
            INSERT INTO employees (employee_name, email, dept_id, join_date)
            VALUES (%s, %s, %s, %s)
            """,
            (name, email, dept_id, join_date),
        )

# ================= GET EMPLOYEE IDS =================
cur.execute("SELECT employee_id FROM employees")
employee_ids = [row[0] for row in cur.fetchall()]

# ================= GENERATE EXPENSES =================
print("Generating expenses...")

for _ in range(NUM_EXPENSES):
    employee_id = random.choice(employee_ids)
    category_id = random.choice(category_ids)
    amount = round(random.uniform(100, 20000), 2)
    description = fake.sentence(nb_words=6)
    expense_date = fake.date_time_between(start_date="-1y", end_date="now")
    payment_method = random.choice(payment_methods)

    cur.execute(
        """
        INSERT INTO expenses (
            employee_id,
            category_id,
            amount,
            description,
            expense_date,
            payment_method
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            employee_id,
            category_id,
            amount,
            description,
            expense_date,
            payment_method,
        ),
    )

print("✅ Synthetic data generation complete!")

cur.close()
conn.close()