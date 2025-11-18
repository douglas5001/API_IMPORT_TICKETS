from fastapi import FastAPI
from app.config.config import config
from app.utils.logging import setup_logging
# from app.config.database import Base, engine
from app.controllers import ticket_controller

setup_logging()

# DEV: cria as tabelas que ainda não existem / Ou você pode criar as tabelas pelo Alembic seguindo o RADME
# Base.metadata.create_all(bind=engine)

app = FastAPI(title=config.app_name)

app.include_router(ticket_controller.router, prefix="/api/v1")


@app.get("/ping")
def ping():
    return {"status": "ok"}
