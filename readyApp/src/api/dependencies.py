from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, description="Страница", ge=1)]
    per_page: Annotated[
        int | None,
        Query(default=3, description="кол-во объектов на странице", ge=1, lt=100),
    ]


PaginationDep = Annotated[PaginationParams, Depends()]
