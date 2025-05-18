from datetime import datetime
from typing import Dict, Optional, Union

from pydantic import BaseModel, Extra, Field, PositiveInt, root_validator


NAME_MIN_LENGTH = 1
NAME_MAX_LENGTH = 100
DESCRIPTION_MIN_LENGTH = 1

FIELD_CANT_BE_NULL = 'Поле {field} не может быть пустым!'


class CharityProjectBase(BaseModel):
    name: str = Field(
        ..., min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH,
    )
    description: str = Field(
        ..., min_length=DESCRIPTION_MIN_LENGTH,
    )
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(
        None, min_length=NAME_MIN_LENGTH, max_length=NAME_MAX_LENGTH,
    )
    description: Optional[str] = Field(
        None, min_length=DESCRIPTION_MIN_LENGTH,
    )
    full_amount: Optional[PositiveInt]

    @root_validator(pre=True)
    def field_cant_be_null(
        cls, values: Dict[str, Union[str, int]],
    ) -> Optional[Dict[str, Union[str, int]]]:
        for field, value in values.items():
            if value is None:
                raise ValueError(FIELD_CANT_BE_NULL.format(field=field))
        return values
