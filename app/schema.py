from pydantic import BaseModel

class ExpenseCreate(BaseModel):
    employee_id: int
    description: str
    amount: float
    expense_date: str

# CREATE TABLE departments (
#     dept_id SERIAL PRIMARY KEY,
#     dept_name VARCHAR(100) NOT NULL,
#     monthly_budget NUMERIC(12,2),
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );


# CREATE TABLE employees (
#     employee_id SERIAL PRIMARY KEY,
#     employee_name VARCHAR(120) NOT NULL,
#     email VARCHAR(150) UNIQUE,
#     dept_id INT REFERENCES departments(dept_id),
#     join_date DATE,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );


# CREATE TABLE expense_categories (
#     category_id SERIAL PRIMARY KEY,
#     category_name VARCHAR(100) UNIQUE NOT NULL
# );


# CREATE TABLE expenses (
#     expense_id SERIAL PRIMARY KEY,
#     employee_id INT REFERENCES employees(employee_id),
#     category_id INT REFERENCES expense_categories(category_id),
#     amount NUMERIC(10,2) NOT NULL,
#     description TEXT,
#     expense_date TIMESTAMP NOT NULL,
#     payment_method VARCHAR(50),
#     is_anomaly BOOLEAN DEFAULT FALSE,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );



# ALTER TABLE expenses
# ADD COLUMN predicted_category_id INT,
# ADD COLUMN confidence FLOAT,
# ADD COLUMN model_version TEXT,
# ADD COLUMN processed_at TIMESTAMP;



# CREATE TABLE model_registry (
#     version_name TEXT PRIMARY KEY,
#     accuracy FLOAT,
#     trained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     is_active BOOLEAN DEFAULT TRUE
# );

# CREATE TABLE drift_metrics (
#     id SERIAL PRIMARY KEY,
#     avg_confidence FLOAT,
#     drift_score FLOAT,
#     recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# CREATE TABLE monthly_forecasts (
#     id SERIAL PRIMARY KEY,
#     forecast_month DATE,
#     department_id INT,
#     predicted_amount FLOAT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
