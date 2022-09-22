from datetime import date as d
from typing import (
    List,
    TypedDict
)

def date(day: int, month: int, year: int):
    return d(day=day, month=month, year=year)


class UpdateJson(TypedDict):
    date: d,
    changelog: str,
    date_str: str


json: List[UpdateJson] = [
    {
        "date": date(22, 9, 2022),
        "changelog": """
            1. Добавлен ИИ для ассистента,
            2. Добавлена команда Обновления
            3. Мини баг фиксы и оптимизации
                    """,
        "date_str": "22 сентября 2022"
    }
]
