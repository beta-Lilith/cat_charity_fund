from datetime import datetime

from sqlalchemy import Column, Boolean, DateTime, Integer

from app.core.db import Base


DEFAULT_INVESTED_AMOUNT = 0


class ProjectDonationBase(Base):
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=DEFAULT_INVESTED_AMOUNT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime)
