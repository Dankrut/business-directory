from httpx import AsyncClient, ASGITransport
import pytest
import sys
from pathlib import Path
from typing import AsyncGenerator

# Добавляем путь для импорта seed
sys.path.append(str(Path(__file__).parent.parent))

from src.api.dependencies import get_db, verify_api_key
from src.models import *  # noqa
from src.config import settings
from src.database import Base
from src.main import app
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool
from src.seed import seed


# Устанавливаем режим тестирования
@pytest.fixture(scope="session", autouse=True)
def test_check_mode():
    assert settings.MODE == "TEST"


# Переопределяем зависимости
async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


async def mock_verify_api_key():
    return "test-api-key"


app.dependency_overrides[get_db] = get_db_null_pool
app.dependency_overrides[verify_api_key] = mock_verify_api_key


# Создаем БД и заполняем тестовыми данными
@pytest.fixture(scope="session", autouse=True)
def setup_db(test_check_mode):
    """Создает таблицы и заполняет тестовыми данными"""

    # Создаем таблицы (синхронно)
    from sqlalchemy import create_engine

    sync_url = settings.DB_URL.replace("+asyncpg", "")
    engine = create_engine(sync_url)

    # Удаляем и создаем таблицы
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Заполняем данными через seed
    seed()  # ← Вызываем ваш seed

    print("✅ Тестовые данные загружены")


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={"X-API-Key": "test-api-key"},
    ) as ac:
        yield ac
