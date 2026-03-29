from sklearn.ensemble import IsolationForest
import pandas as pd
from app.database import engine
import joblib
import numpy as np

MODEL_PATH = "app/models/anomaly_model.pkl"

def train_anomaly_model():
    df = pd.read_sql("SELECT amount FROM expenses", engine)
    if df.empty:
        return

    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(df[["amount"]])

    joblib.dump(model, MODEL_PATH)

def detect_anomaly(amount: float) -> bool:
    model = joblib.load(MODEL_PATH)
    prediction = model.predict([[amount]])
    return prediction[0] == -1