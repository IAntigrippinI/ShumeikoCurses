from httpx import AsyncClient, ASGITransport
from dotenv import load_dotenv
from pydantic import TypeAdapter

from src.main import app
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomsAdd
from src.utils.db_manager import DBManager

load_dotenv(".env-test")
import pytest
import json
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.models import *


@pytest.fixture(scope='function')
async def db() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode): # эта функция выполнится после выполнения check_test_mode
    print("Я ФИКСТУРА")
    print(engine_null_pool.url)
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session', autouse=True)
async def fill_database(setup_database):
    with open("tests/mock_hotels.json", encoding='utf-8') as f:
        json_data = json.load(f)
        hotels = TypeAdapter(list[HotelAdd]).validate_python(json_data)
        # or hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    with open("tests/mock_rooms.json", encoding='utf-8') as f:
        json_data = json.load(f)
        rooms = TypeAdapter(list[RoomsAdd]).validate_python(json_data)
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(data=hotels)
        await db_.rooms.add_bulk(data=rooms)
        await db_.commit()


@pytest.fixture(scope='session')
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test1234") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def test_register_user(setup_database, ac):
    print("Register user")
    responce = await ac.post(
            "/auth/register",
            json={
                "email": "kot@maul.ru",
                "password": "1234"
            }
        )

    print(responce.content)


