import os
import databases
import sqlalchemy
from sqlalchemy import MetaData

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/test_analyzer")

database = databases.Database(DATABASE_URL)
metadata = MetaData()

async def init_db() -> None:
    if not database.is_connected:
        await database.connect()

async def shutdown_db() -> None:
    if database.is_connected:
        await database.disconnect()
