from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility
from src.models.facilities import FacilitiesOrm


class Facilitiesrepository(BaseRepository):
    schema = Facility
    model = FacilitiesOrm
