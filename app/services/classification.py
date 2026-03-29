import joblib
import pandas as pd
from app.database import engine
from app.services.cleaning import clean_text

# Load model
model = joblib.load("app/models/category_model.pkl")
vectorizer = joblib.load("app/models/tfidf_vectorize.pkl")

def predict_category(description: str) -> str:
    cleaned = clean_text(description)
    vec = vectorizer.transform([cleaned])
    return model.predict(vec)[0]

def auto_classify_null_expenses():

    df = pd.read_sql(
        "SELECT expense_id, description FROM expenses WHERE category IS NULL",
        engine
    )

    if df.empty:
        return {"message": "No unclassified expenses found"}

    for index, row in df.iterrows():
        predicted = predict_category(row["description"])

        # Update DB
        engine.execute(
            f"""
            UPDATE expenses
            SET category = '{predicted}'
            WHERE expense_id = {row['expense_id']}
            """
        )

    return {"message": f"{len(df)} expenses classified successfully"}