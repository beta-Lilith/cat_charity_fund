from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import ProjectDonationBase


USER_ID_FK_NAME = 'fk_donation_user_id_user'


class Donation(ProjectDonationBase):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey(
        'user.id',
        name=USER_ID_FK_NAME,
    ))
