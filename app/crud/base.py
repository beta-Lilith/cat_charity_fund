from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.services.utils import update_status


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_all(
            self,
            session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def get_opened_obj(
        self,
        session: AsyncSession,
    ):
        opened_obj = await session.execute(
            select(self.model).where(
                self.model.fully_invested == False  # noqa
            )
        )
        return opened_obj.scalars().all()

    async def save_to_db(
            self,
            *args,
            session: AsyncSession,
    ):
        session.add_all(args)
        await session.commit()
        for arg in args:
            await session.refresh(arg)

    async def create(
            self,
            new_obj,
            session: AsyncSession,
            user: Optional[User] = None,
            save_to_db: bool = True,
    ):
        data = new_obj.dict()
        if user:
            data['user_id'] = user.id
        obj = self.model(**data)
        if save_to_db:
            await self.save_to_db(obj, session=session)
        else:
            session.add(obj)
            await session.flush()
        return obj

    async def update(
            self,
            obj,
            new_data,
            session: AsyncSession,
    ):
        db_data = jsonable_encoder(obj)
        new_data = new_data.dict(exclude_unset=True)
        for field in db_data:
            if field in new_data:
                setattr(obj, field, new_data[field])
        update_status(obj)
        await self.save_to_db(obj, session=session)
        return obj

    async def delete(
            self,
            obj,
            session: AsyncSession,
    ):
        await session.delete(obj)
        await session.commit()
        return obj
