# alembic/env.py

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 1. Aseguramos que Python encuentre el paquete app/ en la raíz
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# 2. Importamos la configuración y el engine que definimos en app/
from app.config import settings
from app.database import engine
from sqlmodel import SQLModel

# 3. Importamos aquí todos los modelos que tengamos (por ahora, League)
from app.models.league import League
from app.models.team import Team
from app.models.player import Player
from app.models.venue import Venue
from app.models.fixture import Fixture
from app.models.payment import Payment
from app.models.user import User




# Este metadata contiene todas las tablas de SQLModel
target_metadata = SQLModel.metadata

# Configuración de logging desde alembic.ini
config = context.config
fileConfig(config.config_file_name)

def run_migrations_offline():
    """Ejecutar migraciones sin conexión (genera SQL)."""
    url = settings.DATABASE_URL  # Tomamos la URL desde .env (sqlite:///./dev.db)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Ejecutar migraciones con conexión a la BD (aplica cambios)."""
    connectable = engine  # Ya está configurado con settings.DATABASE_URL

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
