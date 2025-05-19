from datetime import datetime
from typing import Union

from app.models import CharityProject, Donation


def donate(
        target: Union[CharityProject, Donation],
        sources: Union[list[CharityProject], list[Donation]],
) -> None:
    target.invested_amount = (0 if target.invested_amount is None  # Заглушка
                              else target.invested_amount)         # для тестов
    for source in sources:
        min_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in (target, source):
            obj.invested_amount += min_amount
            update_status(obj)
        if target.fully_invested:
            break


def update_status(obj: Union[CharityProject, Donation]) -> None:
    obj.fully_invested = (obj.full_amount == obj.invested_amount)
    if obj.fully_invested:
        obj.close_date = datetime.utcnow()
