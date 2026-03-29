import os
import joblib
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from app.database import engine
from app.ml.preprocessing import clean_text
from sqlalchemy import text

MODEL_BASE = "models"

def train_model():

    df = pd.read_sql("""
        SELECT e.description, c.category_name
        FROM expenses e
        JOIN expense_categories c ON e.category_id = c.category_id
        WHERE e.category_id IS NOT NULL
    """, engine)

    df["description"] = df["description"].apply(clean_text)

    X_train, X_test, y_train, y_test = train_test_split(
        df["description"],
        df["category_name"],
        test_size=0.3,
        random_state=42
    )

    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression(max_iter=500)
    model.fit(X_train_vec, y_train)

    accuracy = model.score(X_test_vec, y_test)

    version = f"v{datetime.now().strftime('%Y%m%d%H%M%S')}"
    path = os.path.join(MODEL_BASE, version)
    os.makedirs(path)

    joblib.dump(model, f"{path}/model.pkl")
    joblib.dump(vectorizer, f"{path}/vectorizer.pkl")

    with engine.begin() as conn:
        conn.execute(text(
        "UPDATE model_registry SET is_active = FALSE"
    ))

        conn.execute(text("""
            INSERT INTO model_registry(version_name, accuracy, is_active)
            VALUES (:version, :accuracy, TRUE)
        """), {
            "version": version,
            "accuracy": accuracy
        })

        return {"version": version, "accuracy": accuracy}