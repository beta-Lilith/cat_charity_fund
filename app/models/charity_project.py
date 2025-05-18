from sqlalchemy import Column, String, Text

from app.models.base import ProjectDonationBase


NAME_LENGHT = 100


class CharityProject(ProjectDonationBase):
    name = Column(String(NAME_LENGHT), unique=True, nullable=False)
    description = Column(Text, nullable=False)
