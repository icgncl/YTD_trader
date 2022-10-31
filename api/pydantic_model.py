from datetime import date
from pydantic import BaseModel
from datetime import date
from enum import Enum

class Interval(str, Enum):
    minute = '1m'
    half_hour = '30m'
    hour = '1h'
    day = '1d'
    week = '1wk'
    month = '1mo'

class InputData(BaseModel):
    stock: str
    start_date: date
    end_date: date
    interval: Interval

    class Config:
        use_enum_values = True
