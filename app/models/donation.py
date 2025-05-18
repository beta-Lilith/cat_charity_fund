from sqlalchemy import Column, Text

from app.models.base import ProjectDonationBase


class Donation(ProjectDonationBase):
    comment = Column(Text)
