import uvicorn

from fastapi import FastAPI

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import (
    router as router_hotels,
)  # для глобальных импортов от папки src

from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_book
from src.config import settings

app = FastAPI()
app.include_router(router=router_auth)
app.include_router(router=router_hotels)
app.include_router(router=router_rooms)
app.include_router(router=router_book)
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
