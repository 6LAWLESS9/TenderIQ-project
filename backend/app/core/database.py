from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import AsyncMongoClient

from app.core.config import settings
from app.repositories.memory import MemoryStore


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.memory = MemoryStore()
    app.state.mongo = None
    app.state.db = None
    try:
        client = AsyncMongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=1200)
        await client.admin.command("ping")
        app.state.mongo = client
        app.state.db = client[settings.mongodb_database]
        from app.repositories.seed import seed_database
        await seed_database(app.state.db)
    except Exception:
        if app.state.mongo:
            await app.state.mongo.close()
        app.state.mongo = None
        app.state.db = None
    try:
        yield
    finally:
        if app.state.mongo:
            await app.state.mongo.close()
