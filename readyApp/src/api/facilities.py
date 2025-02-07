import json

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.init import redis_manager
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    # facilities_from_cache = await redis_manager.get('facilities')
    # if not facilities_from_cache:
    #     facilities =  await db.facilities.get_all()
    #     facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
    #     facilities_json = json.dumps(facilities_schemas)
    #     await redis_manager.set("facilities", facilities_json, expire=10)        
    #     return facilities
    # else:
    #     facilities_dicts = json.loads(facilities_from_cache)
    #     return facilities_dicts
    print('Иду в бд')
    return await db.facilities.get_all()
    

@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd):
    add_facility = await db.facilities.add(facility_data)
    await db.commit()
    return add_facility
