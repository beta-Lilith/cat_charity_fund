from datetime import datetime

from sqlalchemy import Column, Boolean, DateTime, Integer, CheckConstraint

from app.core.db import Base


DEFAULT_INVESTED_AMOUNT = 0

PROJECT_DONATION_REPR = (
    'Таблица: {tablename}\n'
    'Общая сумма: {full_amount}\n'
    'Инвестировано: {invested_amount}\n'
    'Объект закрыт: {fully_invested}\n'
    'Дата открытия: {create_date}\n'
    'Дата закрытия: {close_date}\n'
)


class ProjectDonationBase(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('invested_amount <= full_amount',
                        name='invested_amount_le_full_amount'),
        CheckConstraint('invested_amount >= 0',
                        name='invested_amount_ge_0'),
        CheckConstraint('full_amount >= 0',
                        name='full_amount_ge_0'),
    )
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=DEFAULT_INVESTED_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime)

    def __repr__(self):
        return PROJECT_DONATION_REPR.format(
            tablename=self.__class__.__tablename__,
            full_amount=self.full_amount,
            invested_amount=self.invested_amount,
            fully_invested=self.fully_invested,
            create_date=self.create_date,
            close_date=self.close_date,
        )
