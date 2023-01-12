from typing import Optional, List

from pydantic import Field, Extra, BaseModel


class Config(BaseModel):
    room_id_list: List[str]

    class Config:
        extra = Extra.ignore
        allow_population_by_field_name = True
