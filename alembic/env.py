from logging.config import fileConfig
import sys
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# ----------------------------------------
# Coloca a raiz do projeto no sys.path
# (API_IMPORT_TICKETS)
# ----------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # .../API_IMPORT_TICKETS
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Agora conseguimos importar "app"
from app.config.database import Base, engine
from app.models import ticket_model
from app.models import ticket_log_model
# importa o model para registrar no Base.metadata
# se depois tiver mais models, importa aqui também
# from app.models import user_model

# Config do Alembic (alembic.ini)
config = context.config

# Logging padrão do Alembic
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# metadata que o Alembic vai inspecionar pra autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Rodar migrations em modo offline (gera SQL)."""
    url = str(engine.url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Rodar migrations conectando no banco (modo normal)."""
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
