from fastapi import FastAPI, HTTPException, status
from pydantic_model import InputData
import yfinance as yf
from datetime import date


client = FastAPI()

@client.post("/get_daily_data/")
def get_stock_prices(data: InputData):
    if data.start_date > data.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date",
        )
    if data.end_date > date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be before today",
        )
    if data.is_hourly:
        interval = "1h"
    else:
        interval = "1d"
    stock = yf.Ticker(data.stock)
    hist = stock.history(start=data.start_date, end=data.end_date, interval=interval).reset_index().to_dict(orient="records")
    return hist