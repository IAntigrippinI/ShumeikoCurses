from pydantic import BaseModel, Field


class RoomsAddReq(BaseModel):
    title: str
    description: str | None = Field(None, description="Описание")
    price: int
    quantity: int


class RoomsAdd(RoomsAddReq):
    hotel_id: int = Field(description="id отеля")


class Rooms(RoomsAdd):
    id: int


class RoomsPATCH(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: str | None = Field(None)
    quantity: str | None = Field(None)
