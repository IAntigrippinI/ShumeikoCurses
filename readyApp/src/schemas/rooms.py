from pydantic import BaseModel, Field


class RoomsAddRequest(BaseModel):
    title: str
    description: str | None = Field(None, description="Описание")
    price: int
    quantity: int
    facilities_ids: list[int] | None = None

class RoomsAdd(BaseModel):
    hotel_id: int = Field(description="id отеля")
    title: str
    description: str | None = None
    price: int
    quantity: int


class Rooms(RoomsAdd):
    id: int


class RoomsPatchRequest(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    facilities_ids: list[int] | None = None


class RoomsPatch(BaseModel):
    hotel_id: int | None = Field(None, description="id отеля")
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
