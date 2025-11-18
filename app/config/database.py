import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------------
# NÃO carregar .env durante execução de testes
# -------------------------------------
if os.getenv("PYTEST_CURRENT_TEST") is None:
    load_dotenv()
# -------------------------------------

# ---- Variáveis individuais ----
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# ---- Monta a URL automaticamente ----
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    if all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
        DATABASE_URL = (
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
            f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        raise RuntimeError(
            "❌ Variáveis de banco ausentes! "
            "Defina DATABASE_URL ou todas: DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME."
        )

# ---- SQLAlchemy ----
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
