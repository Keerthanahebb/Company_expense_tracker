from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine
from app.ml.inference import predict

router = APIRouter()

@router.post("/process-expenses")
def process_expenses():
    processed=0
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT expense_id, description
            FROM expenses
            WHERE category_id IS NULL
        """)).fetchall()

        for row in rows:

            expense_id = row[0]
            description = row[1]

            category_name, confidence, version = predict(description)

            category = conn.execute(text("""
                SELECT category_id
                FROM expense_categories
                WHERE category_name = :name
            """), {"name": category_name}).fetchone()

            if category:

                conn.execute(text("""
                    UPDATE expenses
                    SET category_id=:cat,
                        confidence=:conf,
                        model_version=:version,
                        processed_at=NOW()
                    WHERE expense_id=:id
                """), {
                    "cat": category[0],
                    "conf": confidence,
                    "version": version,
                    "id": expense_id
                })

                processed += 1

    return {"processed_expenses": processed}