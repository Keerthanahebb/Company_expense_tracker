import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sqlalchemy import text
from app.database import get_engine


def generate_forecast(dept_id: int, periods: int = 6):
    """
    Forecast monthly spending for a department and compare it
    with the allocated monthly budget from the departments table.
    """

    engine = get_engine()

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
    df = df.resample("ME").sum().fillna(0)

    # -----------------------------
    # 2. Train ARIMA model
    # -----------------------------
    model = ARIMA(df["total_spend"], order=(1, 1, 1))
    fitted_model = model.fit()

    forecast_values = fitted_model.forecast(steps=periods)

    forecast_index = pd.date_range(
        start=df.index[-1] + pd.offsets.MonthEnd(),
        periods=periods,
        freq="ME"
    )

    forecast_df = pd.DataFrame({
        "month": forecast_index,
        "predicted_spend": forecast_values.values
    })

    # -----------------------------
    # 2b. Clip negative forecasts to zero
    # -----------------------------
    # ARIMA is unconstrained and can mathematically predict negative
    # values for a quantity (spending) that can never be negative in
    # reality. Clip here rather than silently returning misleading numbers.
    had_negative_forecast = (forecast_df["predicted_spend"] < 0).any()
    forecast_df["predicted_spend"] = forecast_df["predicted_spend"].clip(lower=0)

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
    # 4b. Sanity check for data quality issues
    # -----------------------------
    avg_predicted = forecast_df["predicted_spend"].mean()
    data_warning = None

    if monthly_budget > 0 and avg_predicted > 0:
        ratio = monthly_budget / avg_predicted
        if ratio > 10 or ratio < 0.1:
            data_warning = (
                f"Budget-to-forecast ratio is {ratio:.1f}x — this likely indicates "
                f"a unit mismatch (e.g., annual vs monthly budget) or insufficient "
                f"historical transaction data for dept_id={dept_id}, rather than a "
                f"genuine spending trend. Verify department budget and expense data scale."
            )
    elif avg_predicted == 0 and had_negative_forecast:
        data_warning = (
            f"ARIMA produced negative forecasts for dept_id={dept_id}, which were "
            f"clipped to zero. This usually means historical expense data for this "
            f"department is too sparse or noisy for a stable forecast. Consider "
            f"gathering more historical data or using a log-transformed model."
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

    response = {
        "dept_id": dept_id,
        "forecast_months": periods,
        "forecast": result
    }

    if data_warning:
        response["data_quality_warning"] = data_warning
    if had_negative_forecast:
        response["note"] = "Some forecasted values were negative and have been clipped to zero."

    return response