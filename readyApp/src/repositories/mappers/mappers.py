from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.schemas.facilities import Facility, RoomsFacility
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersOrm
from src.schemas.bookings import Booking
from src.schemas.rooms import RoomWithRels, Rooms
from src.schemas.users import User, UserWithHashPassword
from src.models.hotels import HotelsOrm
from src.repositories.mappers.base import DataMapper
from src.schemas.hotels import Hotel


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Rooms


class RoomWithRelsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithRels


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class UserWithHashPasswordDataMapper(DataMapper):
    db_model = UsersOrm
    schema = UserWithHashPassword


class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepositoryDataMapper(DataMapper):
    db_model = RoomsFacilitiesOrm
    schema = RoomsFacility
