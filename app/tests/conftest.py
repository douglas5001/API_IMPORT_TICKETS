import os

# ➜ 1) Antes de tudo, avisamos ao sistema que estamos rodando testes
os.environ["PYTEST_RUNNING"] = "1"

# ➜ 2) Carregar .env.test ANTES de importar qualquer coisa
from dotenv import load_dotenv
load_dotenv(".env.test")

import pytest
from fastapi.testclient import TestClient

# ➜ 3) Agora sim podemos importar a app e o banco
from app.main import app
from app.config.database import Base, engine


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    return TestClient(app)
