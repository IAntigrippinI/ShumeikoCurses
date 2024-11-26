from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class FacilitiesOrm(Base):
    __tablename__ = "facilities"
    __table_args__ = {'extend_existing': True} 
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))


class RoomsFacilitiesOrm(Base):
    __tablename__ = "rooms_facilities"
    __table_args__ = {'extend_existing': True} 

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))
