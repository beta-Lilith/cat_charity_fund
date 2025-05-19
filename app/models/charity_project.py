from sqlalchemy import Column, String, Text

from app.models.base import ProjectDonationBase


NAME_LENGHT = 100

CHARITY_PROJECT_REPR = (
    '{super}'
    'Имя проекта: {name}\n'
    'Описание: {description}\n'
)


class CharityProject(ProjectDonationBase):
    name = Column(String(NAME_LENGHT), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return CHARITY_PROJECT_REPR.format(
            super=super().__repr__(),
            name=self.name,
            description=self.description,
        )
