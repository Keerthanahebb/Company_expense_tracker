from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine
from app.ml.inference import predict
from app.ml.logger import logger   # 👈 ADD THIS

router = APIRouter()

@router.post("/process-expenses")
def process_expenses():

    processed = 0

    try:
        logger.info("Started processing expenses")

        with engine.begin() as conn:

            rows = conn.execute(text("""
                SELECT expense_id, description
                FROM expenses
                WHERE category_id IS NULL
            """)).fetchall()

            logger.info(f"Found {len(rows)} unprocessed expenses")

            for row in rows:

                expense_id = row[0]
                description = row[1]

                # 🔹 Log input
                logger.info(f"Processing expense_id={expense_id}, desc={description}")

                category_name, confidence, version = predict(description)

                # 🔹 Log prediction
                logger.info(
                    f"Prediction: {category_name}, confidence={confidence}, model={version}"
                )

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

        logger.info(f"Processing completed. Total processed: {processed}")

        return {"processed_expenses": processed}

    except Exception as e:
        logger.error(f"Error in processing expenses: {str(e)}")
        return {"error": str(e)}