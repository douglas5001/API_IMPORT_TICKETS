import os
from typing import Generator, Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session


DATABASE_URL = os.getenv("DATABASE_URL")

if os.getenv("PYTEST_RUNNING") == "1":
    DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/test_db"

# 🔥 mypy agora sabe que a variável é sempre string
if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL não está definida!")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
