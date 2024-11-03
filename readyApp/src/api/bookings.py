from fastapi import APIRouter
from src.api.dependencies import DBDep


router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
def add_booking():
    pass
