from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer

from src.database import Base


class HotelsOrm(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))  # max len = 100
    location: Mapped[str]
