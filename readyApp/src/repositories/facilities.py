from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomsFacility
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm


class Facilitiesrepository(BaseRepository):
    schema = Facility
    model = FacilitiesOrm


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomsFacility