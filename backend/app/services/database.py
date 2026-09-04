import os

from pymongo import MongoClient

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "test_analyzer")

mongo_client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=3000)
database = mongo_client[MONGODB_DATABASE]

async def init_db() -> None:
    mongo_client.admin.command("ping")

async def shutdown_db() -> None:
    mongo_client.close()
