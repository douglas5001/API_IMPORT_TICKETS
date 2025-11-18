import os
from typing import Generator, Optional

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session


# Se estamos rodando testes, ignore .env normal
if os.getenv("PYTEST_RUNNING") == "1":
    load_dotenv(".env.test", override=True)
else:
    load_dotenv()


DB_USER: Optional[str] = os.getenv("DB_USER")
DB_PASSWORD: Optional[str] = os.getenv("DB_PASSWORD")
DB_HOST: Optional[str] = os.getenv("DB_HOST")
DB_PORT: Optional[str] = os.getenv("DB_PORT")
DB_NAME: Optional[str] = os.getenv("DB_NAME")

DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")

# Se URL de teste está ativa, sobrescreve tudo
if os.getenv("PYTEST_RUNNING") == "1":
    DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/test_db"


if not DATABASE_URL:
    if all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
        DATABASE_URL = (
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
            f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        raise RuntimeError("Variáveis de banco ausentes!")


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
