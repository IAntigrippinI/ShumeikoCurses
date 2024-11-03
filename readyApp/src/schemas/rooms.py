from pydantic import BaseModel, Field


class RoomsAddRequest(BaseModel):
    title: str
    description: str | None = Field(None, description="Описание")
    price: int
    quantity: int


class RoomsAdd(RoomsAddRequest):
    hotel_id: int = Field(description="id отеля")


class Rooms(RoomsAdd):
    id: int


class RoomsPatchRequest(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)


class RoomsPatch(BaseModel):
    hotel_id: int | None = Field(None, description="id отеля")
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
