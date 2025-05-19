from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import ProjectDonationBase


DONATION_REPR = (
    '{super}'
    'Комментарий: {comment}\n'
    'Создал user_id: {user_id}\n'
)


class Donation(ProjectDonationBase):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return DONATION_REPR.format(
            super=super().__repr__(),
            comment=self.comment,
            user_id=self.user_id,
        )
