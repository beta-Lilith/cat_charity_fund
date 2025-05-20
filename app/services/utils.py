from datetime import datetime

from app.models import ProjectDonationBase


def investment(
        target: ProjectDonationBase,
        sources: list[ProjectDonationBase],
) -> list[ProjectDonationBase]:
    updated_sources = list()
    for source in sources:
        min_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in (target, source):
            obj.invested_amount += min_amount
            update_status(obj)
        updated_sources.append(source)
        if target.fully_invested:
            break
    return updated_sources


def update_status(obj: ProjectDonationBase) -> None:
    obj.fully_invested = (obj.full_amount == obj.invested_amount)
    if obj.fully_invested:
        obj.close_date = datetime.utcnow()
