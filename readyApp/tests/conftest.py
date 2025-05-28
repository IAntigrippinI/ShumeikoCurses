# ruff: noqa: E402 # чтобы ruff не ругался на импорты из проекта, вызванные после мока
from typing import AsyncGenerator
from unittest import mock


def empty_cache(*args, **kwargs):
    def wrapper(func):
        print("Use empty cache", func.__name__)
        return func

    return wrapper


mock.patch(
    "fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f
).start()  # моки нужно вызывать раньше, чем импорты из других файлов проекта
# mock.patch("fastapi_cache.decorator.cache", empty_cache).start()
# mock.patch("src.api.facilities.func", empty_cache).start()
from httpx import AsyncClient, ASGITransport
from dotenv import load_dotenv
from pydantic import TypeAdapter

from src.api.dependencies import get_db
from src.main import app
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomsAdd
from src.utils.db_manager import DBManager

load_dotenv(".env-test")
import pytest
import json
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import *  # noqa - пишем noqa, чтобы ruff не считал это ошибкой. Можно добавть : F402, чтобы указать какую именно ошибку нужно игнорировать


async def get_db_null_pool() -> AsyncGenerator[DBManager]:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager]:
    """
    scope=function: на каждый запуск функции прогоняется фикстура
    scope=module: запускается один раз при щапуске теста из этого файла (модуля)
    scope=session: запускается один раз на весь тест

    """
    async for db in get_db_null_pool():
        yield db


@pytest.fixture(scope="module")
async def db_module() -> AsyncGenerator[DBManager]:
    """
    scope=function: на каждый запуск функции прогоняется фикстура
    scope=module: запускается один раз при щапуске теста из этого файла (модуля)
    scope=session: запускается один раз на весь тест

    """
    async for db_module in get_db_null_pool():
        yield db_module


app.dependency_overrides[get_db] = (
    get_db_null_pool  # Переопределение каких-то зависимостей для тестов. В данной случае нужен session maker null pull для отработки тестов
)


# Второй способ в database.py
@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(
    check_test_mode,
):  # эта функция выполнится после выполнения check_test_mode
    print("Я ФИКСТУРА")
    print(engine_null_pool.url)
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def fill_database(setup_database):
    with open("tests/mock_hotels.json", encoding="utf-8") as f:
        json_data = json.load(f)
        hotels = TypeAdapter(list[HotelAdd]).validate_python(json_data)
        # or hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    with open("tests/mock_rooms.json", encoding="utf-8") as f:
        json_data = json.load(f)
        rooms = TypeAdapter(list[RoomsAdd]).validate_python(json_data)
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(data=hotels)
        await db_.rooms.add_bulk(data=rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient]:
    async with app.router.lifespan_context(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test1234"
        ) as ac:
            yield ac


@pytest.fixture(scope="session", autouse=True)
async def test_register_user(setup_database, ac):
    print("Register user")
    response = await ac.post(
        "/auth/register", json={"email": "kot@maul.ru", "password": "1234"}
    )

    print(response.content)


@pytest.fixture(scope="session")
async def autheticated_ac(ac, test_register_user):
    print("login USER")
    response = await ac.post(
        "/auth/login", json={"email": "kot@maul.ru", "password": "1234"}
    )
    token = response.cookies.get("access_token", None)
    ac_token = ac.cookies.get("access_token", None)
    assert token
    assert isinstance(token, str)
    assert ac_token
    assert ac_token == token
    yield ac
