from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import CharityProjectDB, DonationDB
from . import charity_project_crud, donation_crud


async def donate(
        session: AsyncSession,
        project: CharityProjectDB = None,
        donation: DonationDB = None,
):
    if project:
        all_donations = await donation_crud.get_all(session)
        await invest_amount(project, all_donations)
    if donation:
        all_projects = await charity_project_crud.get_all(session)
        await invest_amount(donation, all_projects)
    await session.commit()
    await session.refresh(project or donation)


async def invest_amount(new_obj, db_objs):
    for db_obj in db_objs:
        if db_obj.fully_invested:
            continue
        min_amount = min(
            new_obj.full_amount - new_obj.invested_amount,
            db_obj.full_amount - db_obj.invested_amount
        )
        new_obj.invested_amount += min_amount
        db_obj.invested_amount += min_amount
        await update_obj_status(new_obj)
        await update_obj_status(db_obj)
        if new_obj.fully_invested:
            break


async def update_obj_status(obj):
    obj.fully_invested = (obj.full_amount == obj.invested_amount)
    if obj.fully_invested:
        obj.close_date = datetime.utcnow()
