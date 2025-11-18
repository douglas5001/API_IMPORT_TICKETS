import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator

if os.getenv("PYTEST_RUNNING") != "1":
    load_dotenv()  # ambiente normal (dev/prod)


if os.getenv("PYTEST_RUNNING") == "1":
    TEST_DB_USER = "postgres"
    TEST_DB_PASS = "postgres"
    TEST_DB_HOST = "localhost"   
    TEST_DB_PORT = "5432"
    TEST_DB_NAME = "test_db"

    DATABASE_URL = (
        f"postgresql+psycopg2://{TEST_DB_USER}:{TEST_DB_PASS}"
        f"@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
    )

else:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        if all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
            DATABASE_URL = (
                f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
                f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            )
        else:
            raise RuntimeError("❌ Variáveis de banco ausentes no ambiente!")


engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
