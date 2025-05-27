from datetime import date

from datetime import date

from sqlalchemy import select, func
from src.models.rooms import RoomsOrm
from src.models.bookings import BookingsOrm

def rooms_ids_for_booking( date_from: date, date_to: date, hotel_id: int | None = None):
    rooms_booked = (
            select(BookingsOrm.room_id, func.count("*").label("busy_rooms"))
            .select_from(BookingsOrm)
            .filter(BookingsOrm.date_from <= date_to, BookingsOrm.date_to >= date_from)
            .group_by(BookingsOrm.room_id)
            .cte(name="rooms_booked")
        )

    free_rooms_tbl = (
            select(
                RoomsOrm.id.label("room_id"),
                RoomsOrm.hotel_id,
                (RoomsOrm.quantity - func.coalesce(rooms_booked.c.busy_rooms, 0)).label(
                    "free_rooms"
                ),
                RoomsOrm.quantity,
                rooms_booked.c.busy_rooms,
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_booked, RoomsOrm.id == rooms_booked.c.room_id)
            .cte(name="free_rooms_tbl")
        )

    rooms_ids_for_hotel = (
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
        )
    
    if hotel_id:
        rooms_ids_for_hotel=rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotel = rooms_ids_for_hotel.subquery(name="rooms_ids_for_hotel") 

    rooms_ids_to_get = (
            select(free_rooms_tbl.c.room_id)
            .select_from(free_rooms_tbl)
            .filter(
                free_rooms_tbl.c.free_rooms > 0,
                free_rooms_tbl.c.room_id.in_(rooms_ids_for_hotel),
            )
        )

    # print(rooms_ids_to_get.compile(compile_kwargs={"literal_binds": True}))
    return rooms_ids_to_get


"""with rooms_ids(
    select id from rooms where hotel_id=1
    ) # получаем только нужный нам отель
 rooms_booked as (
	select room_id, count(*) as busy_rooms
	from bookings 
	where date_from <='2024-11-18' and date_to >='2024-11-17'
	group by room_id
	),  # получаем количество занятых комнат
free_rooms_tbl as (
	select rooms.id as room_id, rooms.hotel_id, rooms.quantity-coalesce(rooms_booked.busy_rooms, 0) as free_rooms, rooms.quantity, rooms_booked.busy_rooms 
	from rooms 
	left join rooms_booked on
	rooms.id=rooms_booked.room_id
) # получаем количество оставшихся мест в комнатах
select * from free_rooms_tbl
where free_rooms > 0 and room_id in (select id from rooms where hotel_id = 1); # забираем только свободные номера #подзапрос для получение комнат конкретного отеля"""
