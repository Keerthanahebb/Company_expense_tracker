# import psycopg2
# import os
# from dotenv import load_dotenv

# # ================= DB CONNECTION =================
# load_dotenv()

# try:
#     conn = psycopg2.connect(
#         host="localhost",
#         # port=5432,
#         database="expense _tracker",
#         user="postgres",
#         password="Hebb#kee@123"
#     )
#     print("✅ Connected to postgres DB")
#     conn.close()

# except Exception as e:
#     print("❌ Error:", e)




from sqlalchemy import text
from app.database import engine

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ DB Connected:", result.fetchone())

except Exception as e:
    print("❌ DB Connection Failed:", e)