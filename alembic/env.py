# ruff: noqa: F401

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# --- Imports do APP DEVEM VIR DEPOIS do Alembic ---
from app.config.database import Base, engine
from app.models import ticket_model
from app.models import ticket_log_model
from app.models.user import user_model
from app.models.user import profile_model
from app.models.user import permission_model
# --------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
