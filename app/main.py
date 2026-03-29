# from fastapi import FastAPI, HTTPException
# from app.schema import ExpenseCreate
# from app.database import engine
# from app.services.classification import (
#     predict_category,
#     auto_classify_null_expenses
# )
# from app.services.anomaly import detect_anomaly
# from sqlalchemy import text
# import pandas as pd

# app = FastAPI()


# # ================= ADD EXPENSE =================
# @app.post("/expenses")
# def add_expense(expense: ExpenseCreate):

#     predicted_category = predict_category(expense.description)
#     is_anomaly = detect_anomaly(expense.amount)

#     try:
#         with engine.begin() as conn:
#             result = conn.execute(
#                 text("""
#                     INSERT INTO expenses (
#                         employee_id,
#                         description,
#                         amount,
#                         expense_date,
#                         category,
#                         is_anomaly
#                     )
#                     VALUES (:employee_id, :description, :amount,
#                             :expense_date, :category, :is_anomaly)
#                     RETURNING expense_id
#                 """),
#                 {
#                     "employee_id": expense.employee_id,
#                     "description": expense.description,
#                     "amount": expense.amount,
#                     "expense_date": expense.expense_date,
#                     "category": predicted_category,
#                     "is_anomaly": is_anomaly
#                 }
#             )

#             expense_id = result.fetchone()[0]

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

#     return {
#         "expense_id": expense_id,
#         "predicted_category": predicted_category,
#         "is_anomaly": is_anomaly
#     }


# # ================= AUTO CLASSIFY =================
# @app.post("/auto-classify")
# def auto_classify():
#     return auto_classify_null_expenses()


# # ================= GET ALL =================
# @app.get("/expenses")
# def get_expenses():
#     df = pd.read_sql("SELECT * FROM expenses", engine)
#     return df.to_dict(orient="records")





from fastapi import FastAPI

from app.api.model_routes import router as model_router
from app.api.processing_routes import router as process_router
from app.api.anomaly_route import router as anomaly_router
from app.api.drift_routes import router as drift_router
from app.api.forecast_route import router as forecast_router
from app.api.expense_routes import router as expense_router



app = FastAPI(title="Expense Intelligence Platform")

app.include_router(expense_router)
app.include_router(model_router)
app.include_router(process_router)
app.include_router(anomaly_router)
# app.include_router(drift_router)
app.include_router(forecast_router)

