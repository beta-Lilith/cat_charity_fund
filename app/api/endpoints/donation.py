from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud import charity_project_crud, donation_crud
from app.services.utils import investment
from app.models import User
from app.schemas import DonationCreate, DonationDB, DonationShortDB


router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    all_donations = await donation_crud.get_all(session)
    return all_donations


@router.post(
    '/',
    response_model=DonationShortDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(
        donation, session, user, save_to_db=False,
    )
    opened_projects = await charity_project_crud.get_opened_obj(session)
    session.add_all(investment(target=new_donation, sources=opened_projects))
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationShortDB],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    donations = await donation_crud.get_by_user(session, user)
    return donations
