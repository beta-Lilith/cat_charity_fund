from typing import Optional

from sqlalchemy import select
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


charity_project_crud = CRUDCharityProject(CharityProject)
