from datetime import date
from pydantic import BaseModel
from datetime import date

class InputData(BaseModel):
    stock: str
    start_date: date
    end_date: date
    is_hourly: bool = False