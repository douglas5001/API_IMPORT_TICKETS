import os
from dotenv import load_dotenv

os.environ["PYTEST_RUNNING"] = "1"


load_dotenv(".env.test")

import pytest
from fastapi.testclient import TestClient

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
