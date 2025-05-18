from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_project_exists
from app.core.db import get_async_session
from app.crud import charity_project_crud
from app.crud.utils import donate
from app.schemas import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
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
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    await donate(session, project=new_project)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def delete_charity_project(
    project_id,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)
    deleted_project = await charity_project_crud.delete(project, session)
    return deleted_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def update_charity_project(
    project_id,
    new_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)
    name = new_data.name
    if name:
        await check_name_duplicate(name, session)
    # print(session.identity_map)
    # for obj in session.identity_map:
    #     print(obj)
    updated_project = await charity_project_crud.update(
        project, new_data, session,
    )
    return updated_project
