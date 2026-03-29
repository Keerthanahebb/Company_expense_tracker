# import pandas as pd
# from statsmodels.tsa.arima.model import ARIMA
# from app.database import engine

# def generate_forecast(department_id, periods=3):

#     df = pd.read_sql("""
#         SELECT DATE_TRUNC('month', expense_date) AS month,
#                SUM(amount) AS total
#         FROM expenses e
#         JOIN employees emp ON e.employee_id = emp.employee_id
#         WHERE emp.dept_id = %s
#         GROUP BY month
#         ORDER BY month
#     """, engine, params=(department_id,))

#     if len(df) < 6:
#         return {"error": "Not enough data"}

#     df["month"] = pd.to_datetime(df["month"])
#     df.set_index("month", inplace=True)

#     model = ARIMA(df["total"], order=(1,1,1))
#     fitted = model.fit()

#     forecast = fitted.forecast(steps=periods)

#     return forecast.to_dict()



import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sqlalchemy import text
from app.database import engine


def generate_forecast(dept_id: int, periods: int = 6):
    """
    Forecast monthly spending for a department and compare it
    with the allocated monthly budget from the departments table.
    """

    # -----------------------------
    # 1. Fetch historical monthly spending
    # -----------------------------
    query = text("""
        SELECT 
            DATE_TRUNC('month', e.expense_date) AS month,
            SUM(e.amount) AS total_spend
        FROM expenses e
        JOIN employees emp
            ON e.employee_id = emp.employee_id
        WHERE emp.dept_id = :dept
        GROUP BY month
        ORDER BY month
    """)

    df = pd.read_sql(query, engine, params={"dept": dept_id})

    if df.empty or len(df) < 6:
        return {"error": "Not enough historical data to forecast"}

    # convert month column
    df["month"] = pd.to_datetime(df["month"])
    df.set_index("month", inplace=True)

    # ensure continuous monthly timeline
    df = df.resample("M").sum().fillna(0)

    # -----------------------------
    # 2. Train ARIMA model
    # -----------------------------
    model = ARIMA(df["total_spend"], order=(1, 1, 1))
    fitted_model = model.fit()

    forecast_values = fitted_model.forecast(steps=periods)

    forecast_index = pd.date_range(
        start=df.index[-1] + pd.offsets.MonthEnd(),
        periods=periods,
        freq="M"
    )

    forecast_df = pd.DataFrame({
        "month": forecast_index,
        "predicted_spend": forecast_values.values
    })

    # -----------------------------
    # 3. Get department monthly budget
    # -----------------------------
    budget_query = text("""
        SELECT monthly_budget
        FROM departments
        WHERE dept_id = :dept
    """)

    budget_df = pd.read_sql(budget_query, engine, params={"dept": dept_id})

    if budget_df.empty:
        return {"error": "Department budget not found"}

    monthly_budget = float(budget_df.iloc[0]["monthly_budget"])

    forecast_df["monthly_budget"] = monthly_budget

    # -----------------------------
    # 4. Calculate variance
    # -----------------------------
    forecast_df["variance"] = (
        forecast_df["predicted_spend"] - forecast_df["monthly_budget"]
    )

    # -----------------------------
    # 5. Format API response
    # -----------------------------
    result = []

    for _, row in forecast_df.iterrows():
        result.append({
            "month": str(row["month"].date()),
            "predicted_spend": float(row["predicted_spend"]),
            "monthly_budget": monthly_budget,
            "variance": float(row["variance"])
        })

    return {
        "dept_id": dept_id,
        "forecast_months": periods,
        "forecast": result
    }