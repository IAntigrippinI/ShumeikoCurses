from fastapi import Request
from typing import Annotated
from fastapi import Depends, Query, HTTPException
from pydantic import BaseModel
from src.services.auth import AuthService
from src.utils.db_manager import DBManager
from src.database import async_session_maker


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, description="Страница", ge=1)]
    per_page: Annotated[
        int | None,
        Query(default=3, description="кол-во объектов на странице", ge=1, lt=100),
    ]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    access_token = request.cookies.get(
        "access_token", None
    )  # поиск по словарю делается с исп .get(key, if not key)
    if not access_token:
        raise HTTPException(status_code=401, detail="Пользователь не аутентифицирован")
    return access_token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    if token:
        data = AuthService().decode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[None, Depends(get_db)]
