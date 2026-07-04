# from sqlalchemy.engine import URL
# from sqlalchemy import create_engine,text
# import os

# from dotenv import load_dotenv

# load_dotenv(override=True)


# url = URL.create(
#     drivername="postgresql+psycopg2",
#     username="postgres.cvgtykriqcsbsbcwvgft",
#     password=os.getenv("DB_PASSWORD"),
#     host=os.environ.get("DB_HOST"),
#     # host="aws-1-ap-northeast-1.pooler.supabase.com",
#     port=os.getenv("port"),
#     # database=os.getenv("database"),
#     database="postgres"
# )

# print("DB HOST:", os.getenv("DB_HOST"))
# print("DB HOST:", os.getenv("port"))
# print("DB HOST:", os.getenv("DB_NAME"))

# # print("DB URL:", os.getenv("DB_URL"))
# # DATABASE_URL = os.getenv("DB_URL")

# engine = create_engine(
#     url,
#     connect_args={"sslmode": "require"}  # REQUIRED for Supabase
# )

# engine = create_engine(url)



# from sqlalchemy.engine import URL
# from sqlalchemy import create_engine, text
# import os
# from dotenv import load_dotenv

# # Load env
# load_dotenv()

# # Debug (temporary)
# print("DB_USER:", os.getenv("DB_USER"))
# print("DB_HOST:", os.getenv("DB_HOST"))
# print("DB_PORT:", os.getenv("DB_PORT"))
# print("DB_NAME:", os.getenv("DB_NAME"))

# # Create URL
# url = URL.create(
#     drivername="postgresql+psycopg2",
#     username=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASSWORD"),
#     host=os.getenv("DB_HOST"),
#     port=int(os.getenv("DB_PORT")),
#     database=os.getenv("DB_NAME")
# )

# # Create engine
# engine = create_engine(
#     url,
#     connect_args={"sslmode": "require"}
# )

# # Test connection
# with engine.connect() as conn:
#     result = conn.execute(text("SELECT 1"))
#     print("✅ DB Connected:", result.fetchone())



from sqlalchemy.engine import URL
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load env (safe no-op if .env doesn't exist, e.g. in CI)
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = None

def _build_engine():
    """Build the SQLAlchemy engine lazily, only when actually needed."""
    global engine
    if engine is not None:
        return engine

    missing = [
        name for name, val in [
            ("DB_USER", DB_USER),
            ("DB_PASSWORD", DB_PASSWORD),
            ("DB_HOST", DB_HOST),
            ("DB_PORT", DB_PORT),
            ("DB_NAME", DB_NAME),
        ] if not val
    ]
    if missing:
        raise RuntimeError(
            f"Cannot connect to database — missing env vars: {', '.join(missing)}"
        )

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB_NAME,
    )

    engine = create_engine(url, connect_args={"sslmode": "require"})
    return engine


def get_engine():
    return _build_engine()


def test_connection():
    """Call this manually (e.g. python -m app.database) to verify DB connectivity.
    Does NOT run automatically on import."""
    eng = _build_engine()
    with eng.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ DB Connected:", result.fetchone())


if __name__ == "__main__":
    test_connection()