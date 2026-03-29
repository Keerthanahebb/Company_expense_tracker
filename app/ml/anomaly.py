import pandas as pd
from sklearn.ensemble import IsolationForest
from app.database import engine

def detect_department_anomalies():

    query = """
    SELECT 
        e.expense_id,
        e.amount,
        emp.dept_id
    FROM expenses e
    JOIN employees emp
    ON e.employee_id = emp.employee_id
    """

    df = pd.read_sql(query, engine)

    if df.empty:
        return []

    results = []

    departments = df["dept_id"].unique()

    for dept in departments:

        dept_df = df[df["dept_id"] == dept]

        # Skip if too few records
        if len(dept_df) < 10:
            continue

        model = IsolationForest(
            contamination=0.02,
            random_state=42
        )

        dept_df["anomaly"] = model.fit_predict(dept_df[["amount"]])

        anomalies = dept_df[dept_df["anomaly"] == -1]

        for _, row in anomalies.iterrows():

            results.append({
                "expense_id": int(row["expense_id"]),
                "department_id": int(row["dept_id"]),
                "amount": float(row["amount"]),
                "anomaly": True
            })

    return results