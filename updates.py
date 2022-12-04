from datetime import date as d
from typing import (
    List,
    TypedDict
)

def date(day: int, month: int, year: int):
    y = int('20' + str(year))
    
    return d(day=day, month=month, year=y)


class UpdateJson(TypedDict):
    date: d
    name: str


json: List[UpdateJson] = [
    {
        "date": date(4, 12, 22),
        "name": "2022.48b"
    }
]
