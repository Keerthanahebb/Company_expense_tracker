from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import os

from dotenv import load_dotenv

load_dotenv()

url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password=os.getenv("DB_PASSWORD"),
    host="localhost",
    database=os.getenv("DB_NAME"),
)

engine = create_engine(url)