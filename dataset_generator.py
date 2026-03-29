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



# ===================== TEMPLATES =====================

sentence_templates = [
    "Expense incurred for {activity} related to {purpose} at {location}.",
    "Payment made towards {activity} during the {event}.",
    "Charges for {activity} including applicable taxes and service fees.",
    "Reimbursement for {activity} as part of {project}.",
    "Corporate expense for {activity} conducted in {city}.",
    "Approved expense for {activity} aligned with {purpose}.",
]

purposes = [
    "client engagement",
    "business expansion",
    "quarterly review",
    "internal audit",
    "project execution",
    "strategy planning",
]

locations = [
    "corporate office",
    "client site",
    "regional branch",
    "headquarters",
    "conference venue",
]

events = [
    "annual summit",
    "strategy workshop",
    "quarterly business review",
    "client onboarding session",
]

projects = [
    "Project Alpha",
    "Digital Transformation Initiative",
    "Market Expansion Plan",
    "Client Acquisition Drive",
]

extra_phrases = [
    "Approved by finance department.",
    "As per company policy guidelines.",
    "Including applicable GST and service charges.",
    "Reviewed during monthly operations meeting.",
    "Urgent requirement for ongoing activities.",
    "Documented for audit and compliance purposes.",
]

# ===================== CATEGORY KEYWORDS =====================

category_keywords = {
    "Travel": [
        "flight booking for client meeting",
        "airport transfer for regional review",
        "hotel stay during strategy session",
        "cab charges for office visit",
        "train ticket for project discussion",
    ],
    "Food": [
        "team lunch after client presentation",
        "working dinner during travel",
        "refreshments for internal meeting",
        "catering services for training session",
        "business breakfast with vendor",
    ],
    "Software": [
        "software license renewal for reporting",
        "cloud subscription for remote meeting",
        "analytics tool purchase for finance team",
        "CRM upgrade for client management",
        "enterprise SaaS renewal for operations",
    ],
    "Client Meeting": [
        "client strategy meeting at hotel",
        "business review session with partner",
        "quarterly planning discussion over lunch",
        "onsite discussion with vendor",
        "presentation meeting at corporate office",
    ],
    "Office Supplies": [
        "stationery purchase for client presentation",
        "printer ink for travel documents",
        "office chair replacement for meeting room",
        "whiteboard markers for strategy session",
        "notebooks and folders for workshop",
    ],
}

# ===================== NOISE FUNCTION =====================

def add_noise(text):

    # Add reference number (ERP style)
    if random.random() < 0.3:
        text += f" Ref#{random.randint(1000, 9999)}."

    # Minor typo simulation
    if random.random() < 0.1:
        text = text.replace("meeting", "meetng")

    # Random uppercase word
    if random.random() < 0.1:
        words = text.split()
        if len(words) > 3:
            idx = random.randint(0, len(words) - 1)
            words[idx] = words[idx].upper()
            text = " ".join(words)

    return text


# ===================== DESCRIPTION GENERATOR =====================

def generate_complex_description(category_name):

    base_activity = random.choice(category_keywords[category_name])
    template = random.choice(sentence_templates)

    description = template.format(
        activity=base_activity,
        purpose=random.choice(purposes),
        location=random.choice(locations),
        event=random.choice(events),
        project=random.choice(projects),
        city=fake.city()
    )

    description += " " + random.choice(extra_phrases)
    description = add_noise(description)

    return description


# ================= FETCH REQUIRED IDS =================
cur.execute("SELECT employee_id FROM employees")
employee_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT category_id, category_name FROM expense_categories")
category_map = {row[0]: row[1] for row in cur.fetchall()}

print("Generating structured realistic expenses...")

# ================= GENERATE EXPENSES =================
for _ in range(NUM_EXPENSES):

    employee_id = random.choice(employee_ids)

    category_id = random.choice(list(category_map.keys()))
    category_name = category_map[category_id]   

    # description = random.choice(category_keywords[category_name])
    # description = add_noise(description)
    description = generate_complex_description(category_name)

    amount = round(random.uniform(500, 15000), 2)
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

# print("Generating expenses...")

# for _ in range(NUM_EXPENSES):
#     employee_id = random.choice(employee_ids)
#     category_id = random.choice(category_ids)
#     amount = round(random.uniform(100, 20000), 2)
#     description = fake.sentence(nb_words=6)
#     expense_date = fake.date_time_between(start_date="-1y", end_date="now")
#     payment_method = random.choice(payment_methods)

#     cur.execute(
#         """
#         INSERT INTO expenses (
#             employee_id,
#             category_id,
#             amount,
#             description,
#             expense_date,
#             payment_method
#         )
#         VALUES (%s, %s, %s, %s, %s, %s)
#         """,
#         (
#             employee_id,
#             category_id,
#             amount,
#             description,
#             expense_date,
#             payment_method,
#         ),
#     )

print("✅ Synthetic data generation complete!")

cur.close()
conn.close()