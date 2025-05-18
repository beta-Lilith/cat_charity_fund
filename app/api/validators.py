from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject


NAME_NOT_UNIQUE = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект не найден!'


async def check_name_duplicate(
        name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_id_by_name(name, session)
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=NAME_NOT_UNIQUE,
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND
        )
    return project
