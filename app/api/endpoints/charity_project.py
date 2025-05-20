from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_project_before_delete,
    check_project_before_update,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud, donation_crud
from app.services.utils import investment
from app.schemas import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate,
)


router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charity_project_crud.get_all(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(
        project,
        session,
        save_to_db=False,
    )
    opened_donations = await donation_crud.get_opened_obj(session)
    await charity_project_crud.save_to_db(
        new_project,
        *investment(target=new_project, sources=opened_donations),
        session=session,
    )
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_before_delete(project_id, session)
    deleted_project = await charity_project_crud.delete(project, session)
    return deleted_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    new_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_before_update(project_id, new_data, session)
    updated_project = await charity_project_crud.update(
        project, new_data, session,
    )
    return updated_project
