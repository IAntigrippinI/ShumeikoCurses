from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import (
    router as router_hotels,
)  # для глобальных импортов от папки src

from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.config import settings
from src.init import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    #При старе
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    #При перезагрузке/выключении приложения
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router=router_auth)
app.include_router(router=router_hotels)
app.include_router(router=router_rooms)
app.include_router(router=router_facilities)
app.include_router(router=router_bookings)

if __name__ == "__main__":

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
