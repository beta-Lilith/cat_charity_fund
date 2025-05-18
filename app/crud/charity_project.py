from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas import CharityProjectUpdate


class CRUDCharityProject(CRUDBase):

    async def get_id_by_name(
            self,
            name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == name)
        )
        return db_id.scalars().first()

    async def update(
            self,
            project: CharityProject,
            new_data: CharityProjectUpdate,
            session: AsyncSession
    ):
        db_data = jsonable_encoder(project)
        new_data = new_data.dict(exclude_unset=True)
        for field in db_data:
            if field in new_data:
                setattr(project, field, new_data[field])
        # session.add(project)
        await session.commit()
        await session.refresh(project)
        return project

    async def delete(
            self,
            project: CharityProject,
            session: AsyncSession
    ):
        await session.delete(project)
        await session.commit()
        return project


charity_project_crud = CRUDCharityProject(CharityProject)
