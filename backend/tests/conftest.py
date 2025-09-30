import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient

os.environ["APP_SECRET"] = "test_secret_key_test_secret_key"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"

from app.main import app  # noqa: E402  pylint: disable=wrong-import-position
from app.core.security import get_password_hash  # noqa: E402
from app.db import base  # noqa: F401  # ensure models imported
from app.db.session import Base, async_session, engine  # noqa: E402
from app.models.user import User  # noqa: E402


@pytest_asyncio.fixture(autouse=True)
async def prepare_database() -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        admin = User(
            email="admin@example.com",
            name="Admin",
            role="owner",
            password_hash=get_password_hash("Admin123!"),
        )
        session.add(admin)
        await session.commit()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
