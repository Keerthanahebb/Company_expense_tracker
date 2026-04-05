import joblib
from sqlalchemy import text
from app.database import engine
from app.ml.preprocessing import clean_text
from app.ml.logger import logger


def load_active_model():

    with engine.connect() as conn:

        result = conn.execute(text("""
            SELECT version_name
            FROM model_registry
            WHERE is_active = TRUE
            ORDER BY trained_at DESC
            LIMIT 1
        """)).fetchone()

    if result is None:
        raise Exception("No active model found. Train the model first.")

    version = result[0]

    model = joblib.load(f"models/{version}/model.pkl")
    vectorizer = joblib.load(f"models/{version}/vectorizer.pkl")

    return model, vectorizer, version


def predict(description):

    model, vectorizer, version = load_active_model()

    logger.info(f"Prediction request received: {description}")
    cleaned = clean_text(description)

    # logger.info(f"Prediction request received: {desc}")

    X = vectorizer.transform([cleaned])

    prediction = model.predict(X)[0]

    logger.info(f"Prediction result: {prediction}")

    confidence = float(max(model.predict_proba(X)[0]))

    return prediction, confidence, version