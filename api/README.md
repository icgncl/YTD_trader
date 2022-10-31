# YTD_trader API

  Preconditions:
* Python3
* Pip3

Firstly, create an Python environment and activate it. Then install project dependencies.

```
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

Then go inside /api folder. And run tests by 
```
pytest test_api.py
```

In order to run API in local env:
```
uvicorn app:client --reload
```

> API can be used with GET requests. http://127.0.0.1:8000/stock/price/

> Example body for requests:
```json
{
    "stock": "META",
    "start_date": "2022-10-26",
    "end_date": "2022-10-27",
    "interval": "1m"
}
```
For interval, following ones can be used:
* minute = '1m'
* half_hour = '30m'
* hour = '1h'
* day = '1d'
* week = '1wk'
* month = '1mo'