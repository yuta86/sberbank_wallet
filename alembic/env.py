from __future__ import with_statement

from logging.config import fileConfig

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
import os
# print(os.getcwd())
import sys
sys.path.append(os.getcwd())
# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from config import current_config

DB_URL = current_config.DB_URL
ALEMBIC_DB_URL = current_config.ALEMBIC_DB_URL
engine = create_engine(DB_URL,
                       echo=False,
                       pool_size=1,
                       max_overflow=10)
alembic_engine = create_engine(ALEMBIC_DB_URL,
                       echo=False,
                       pool_size=1,
                       max_overflow=10)
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from models._base import Base
# from utils import alembic_engine as engine

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():


    with alembic_engine.connect() as connection:
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
