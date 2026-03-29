from sqlalchemy import create_engine,URL
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
import re

# ================= DB CONNECTION =================
url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password=os.getenv("DB_PASSWORD"),
    host="localhost",
    database="expense_tracker",
)

engine = create_engine(url)

query = """
SELECT description, c.category_name
FROM expenses e
JOIN expense_categories c
ON e.category_id = c.category_id
"""




def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text



df = pd.read_sql(query, engine)

df = df.dropna()
df["description"] = df["description"].apply(clean_text)



# MODEL tRAINING 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib

X = df["description"]
y = df["category_name"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)



model = LogisticRegression(max_iter=300)
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

joblib.dump(model, "app/models/category_model.pkl")
joblib.dump(vectorizer, "app/models/tfidf_vectorizer.pkl")


from sklearn.metrics import confusion_matrix

print(confusion_matrix(y_test, y_pred ))

print(y.value_counts())

