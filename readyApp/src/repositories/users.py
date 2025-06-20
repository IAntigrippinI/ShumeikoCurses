from sqlalchemy import select
from pydantic import EmailStr

from src.repositories.mappers.mappers import (
    UserDataMapper,
    UserWithHashPasswordDataMapper,
)
from src.repositories.base import BaseRepository
from src.models.users import UsersOrm


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_pass(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)

        model = result.scalars().one()
        # print(query.compile(compile_kwargs={"literal_binds": True}))

        return UserWithHashPasswordDataMapper.map_to_domain_entity(model)
