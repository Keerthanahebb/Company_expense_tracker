import pandas as pd
import re
import numpy as np

def clean_text(text):

    if pd.isna(text):
        return ""

    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def add_time_features(df):

    df["expense_date"] = pd.to_datetime(df["expense_date"])

    df["year"] = df["expense_date"].dt.year
    df["month"] = df["expense_date"].dt.month
    df["weekday"] = df["expense_date"].dt.weekday

    return df


def add_amount_features(df):
    df["log_amount"] = df["amount"].apply(lambda x: np.log(x + 1))
    return df


def feature_pipeline(df):

    if "description" in df.columns:
        df["clean_description"] = df["description"].apply(clean_text)

    if "expense_date" in df.columns:
        df = add_time_features(df)

    if "amount" in df.columns:
        df = add_amount_features(df)

    return df

