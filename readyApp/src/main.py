from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
# from fastapi_cache.backends.inmemory import InMemoryBackend для теста вместо редиса

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.dependencies import get_db  # noqa
from src.api.hotels import (
    router as router_hotels,
)  # для глобальных импортов от папки src

from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images
from src.config import settings
from src.init import redis_manager


# async def send_emails_bookings_with_today_checkin(): # пример использования бэкграунд функций python
#     async for db in get_db():
#         bookings = await db.bookings.get_booking_with_today_checkin()
#         print(f"{bookings=}")


# async def run_send_email_regularly():
#     while True:
#         await send_emails_bookings_with_today_checkin()
#         await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старnе
    # asyncio.create_task(run_send_email_regularly()) # пример использования бэкграунд функций python
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    # При перезагрузке/выключении приложения
    if settings.MODE != "TEST":
        print("RESTART REDIS")
        await redis_manager.close()


#
if settings.MODE == "TEST":
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
# FastAPICache.init(InMemoryBackend(), prefix='fastapi-cache')


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_auth)
app.include_router(router=router_hotels)
app.include_router(router=router_rooms)
app.include_router(router=router_facilities)
app.include_router(router=router_bookings)
app.include_router(router=router_images)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
