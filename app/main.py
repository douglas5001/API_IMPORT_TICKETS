from fastapi import FastAPI
from app.config.config import config
from app.utils.logging import setup_logging
# from app.config.database import Base, engine
from app.controllers import ticket_controller
from app.controllers.user import auth_controller
setup_logging()



# DEV: cria as tabelas que ainda não existem / Ou você pode criar as tabelas pelo Alembic seguindo o RADME
# Base.metadata.create_all(bind=engine)

app = FastAPI(title=config.app_name)

app.include_router(ticket_controller.router, prefix="/api/v1")
app.include_router(auth_controller.router, prefix="/api/v1")

@app.get("/health")
def ping():
    return {"status": "ok"}




