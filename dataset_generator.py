import random
from faker import Faker
from sqlalchemy import text
from app.database import engine

fake = Faker()

# ================= CONFIG =================
NUM_EMPLOYEES = 50
NUM_EXPENSES = 5000

payment_methods = ["Credit Card", "UPI", "Cash", "Debit Card"]

categories = ["Travel", "Food", "Office Supplies", "Software", "Client Meeting"]

departments = ["Engineering", "Marketing", "HR", "Finance", "Sales"]

# ================= CATEGORY KEYWORDS =================

category_keywords = {
    "Travel": [
        "flight booking",
        "uber ride",
        "hotel stay",
        "cab charges",
        "train ticket",
    ],
    "Food": [
        "team lunch",
        "client dinner",
        "coffee meeting",
        "snacks for meeting",
        "business lunch",
    ],
    "Software": [
        "software license",
        "cloud subscription",
        "analytics tool",
        "CRM upgrade",
        "SaaS renewal",
    ],
    "Client Meeting": [
        "client meeting",
        "business discussion",
        "project meeting",
        "vendor meeting",
        "presentation meeting",
    ],
    "Office Supplies": [
        "stationery purchase",
        "printer ink",
        "office chair",
        "whiteboard markers",
        "notebooks",
    ],
}

locations = [
    "office",
    "client site",
    "branch",
    "head office",
    "conference hall",
]

# ================= LIGHT NOISE =================

def add_light_noise(text):

    if random.random() < 0.2:
        text = text.replace("meeting", "meting")

    if random.random() < 0.2:
        text = text.replace("for", "fr")

    if random.random() < 0.1:
        text = text.replace(" ", "")

    if random.random() < 0.3:
        text = text.lower()

    return text


# ================= DESCRIPTION =================

def generate_realistic_description(category):

    base = random.choice(category_keywords[category])

    simple_templates = [
        "{activity}",
        "{activity} for work",
        "{activity} - official",
        "{activity} expense",
        "{activity} for office",
        "{activity} during meeting",
    ]

    desc = random.choice(simple_templates).format(activity=base)

    # Add small real detail
    if random.random() < 0.5:
        desc += f" at {random.choice(locations)}"

    # Light human-like noise
    desc = add_light_noise(desc)

    # Slight ambiguity (rare)
    if random.random() < 0.15:
        desc += f", also {random.choice(category_keywords[random.choice(categories)])}"

    return desc


# ================= MAIN =================

with engine.begin() as conn:

    # print("⚠️ Resetting database...")

    # conn.execute(text("TRUNCATE TABLE expenses RESTART IDENTITY CASCADE"))
    # conn.execute(text("TRUNCATE TABLE employees RESTART IDENTITY CASCADE"))
    # conn.execute(text("TRUNCATE TABLE expense_categories RESTART IDENTITY CASCADE"))
    # conn.execute(text("TRUNCATE TABLE departments RESTART IDENTITY CASCADE"))

    print("🔹 Inserting master data...")

    # Departments
    for dept in departments:
        conn.execute(text("""
            INSERT INTO departments (dept_name, monthly_budget)
            VALUES (:d, :b)
        """), {"d": dept, "b": random.randint(200000, 800000)})

    # Categories
    for cat in categories:
        conn.execute(text("""
            INSERT INTO expense_categories (category_name)
            VALUES (:c)
        """), {"c": cat})

    dept_ids = [r[0] for r in conn.execute(text("SELECT dept_id FROM departments"))]

    cat_rows = conn.execute(text("""
        SELECT category_id, category_name FROM expense_categories
    """))
    category_map = {r[0]: r[1] for r in cat_rows}

    print("🔹 Creating employees...")

    for _ in range(NUM_EMPLOYEES):
        conn.execute(text("""
            INSERT INTO employees (employee_name, email, dept_id, join_date)
            VALUES (:n, :e, :d, :j)
        """), {
            "n": fake.name(),
            "e": fake.unique.email(),
            "d": random.choice(dept_ids),
            "j": fake.date_between(start_date="-3y", end_date="today")
        })

    emp_ids = [r[0] for r in conn.execute(text("SELECT employee_id FROM employees"))]

    print("🔹 Generating realistic expenses...")

    for _ in range(NUM_EXPENSES):

        cat_id = random.choice(list(category_map.keys()))

        if random.random() < 0.05:
            cat_id = random.choice(list(category_map.keys()))

        cat_name = category_map[cat_id]

        conn.execute(text("""
            INSERT INTO expenses (
                employee_id,
                category_id,
                amount,
                description,
                expense_date,
                payment_method
            )
            VALUES (:emp, :cat, :amt, :desc, :date, :pay)
        """), {
            "emp": random.choice(emp_ids),
            "cat": cat_id,
            "amt": round(random.uniform(500, 15000), 2),
            "desc": generate_realistic_description(cat_name),
            "date": fake.date_time_between(start_date="-1y", end_date="now"),
            "pay": random.choice(payment_methods)
        })

print("✅ Realistic dataset generated successfully!")