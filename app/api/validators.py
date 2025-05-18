from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas import CharityProjectUpdate


NAME_NOT_UNIQUE = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект не найден!'
PROJECT_INVESTED_ERR = (
    'Нельзя удалить проект, в который уже были инвестированы средства!'
)
PROJECT_AMOUNT_ERR = 'Нельзя установить требуемую сумму меньше уже вложенной!'
PROJECT_CLOSED = 'Закрытый проект нельзя редактировать!'


async def check_name_duplicate(
        name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_id_by_name(name, session)
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
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


async def check_project_before_delete(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await check_project_exists(project_id, session)
    if project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_INVESTED_ERR,
        )
    return project


async def check_project_before_update(
        project_id: int,
        new_data: CharityProjectUpdate,
        session: AsyncSession,
) -> CharityProject:
    project = await check_project_exists(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_CLOSED,
        )
    name = new_data.name
    if name:
        await check_name_duplicate(name, session)
    full_amount = new_data.full_amount
    if full_amount and full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_AMOUNT_ERR,
        )
    return project
