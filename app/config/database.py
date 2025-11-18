import os
from typing import Generator, Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session


if os.getenv("PYTEST_RUNNING") == "1":
    load_dotenv(".env.test", override=True)
else:
    load_dotenv()


DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")


if os.getenv("PYTEST_RUNNING") == "1":
    DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/test_db"




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
