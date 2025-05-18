from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session

from app.crud import donation_crud
from app.crud.utils import donate
from app.schemas import DonationCreate, DonationDB, DonationShortDB


router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
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
):
    new_donation = await donation_crud.create(donation, session)
    await donate(session, donation=new_donation)
    return new_donation


@router.get('/my')
async def get_user_donations():
    pass
