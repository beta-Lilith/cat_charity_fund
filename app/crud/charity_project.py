from typing import Optional

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


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

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> Optional[list]:
        closed_projects = await session.execute(
            select(
                CharityProject.name,
                (
                    extract('epoch', CharityProject.close_date) -
                    extract('epoch', CharityProject.create_date)
                ).label('duration'),
                CharityProject.description,
            ).where(CharityProject.fully_invested).order_by('duration')
        )
        return closed_projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
