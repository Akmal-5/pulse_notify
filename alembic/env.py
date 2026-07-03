import asyncio
import os
from dotenv import load_dotenv
from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
 
load_dotenv()
 
from app.core.config import Base
from app.models.user import CreateUsers
from app.models.userteste import UserTeste
from app.models.target import Target
from app.models.checklog import CheckLog

config = context.config
 

if config.config_file_name is not None:
    fileConfig(config.config_file_name)
 

target_metadata = Base.metadata

 
 
def run_migrations_offline() -> None:

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
 
    with context.begin_transaction():
        context.run_migrations()
 
 
def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()
 
 
async def run_migrations_online() -> None:

    connectable = create_async_engine(
        os.getenv("DATABASE_URL"),
        poolclass=pool.NullPool,
    )
 
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
 
    await connectable.dispose()
 
 
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())