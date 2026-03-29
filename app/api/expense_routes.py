from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine

router = APIRouter()

@router.post("/add-expense")

def add_expense(employee_id:int, description:str, amount:float):

    with engine.begin() as conn:

        conn.execute(text("""
            INSERT INTO expenses
            (employee_id, description, amount, expense_date)
            VALUES (:emp, :desc, :amt, NOW())
        """),{
            "emp":employee_id,
            "desc":description,
            "amt":amount
        })

    return {"status":"expense added"}