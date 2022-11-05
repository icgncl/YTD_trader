import datetime
from functools import lru_cache

import numpy as np
import yfinance as yf
from dash import Dash, Input, Output, dcc, html
import logging

logging.basicConfig(
    format='%(asctime)s|%(levelname)s|%(message)s',
    level=logging.INFO,
    datefmt="%Y-%m-%dT%H:%M:%S%z"
)
logger = logging.getLogger()


TIMEZONE = datetime.timezone.utc
HISTORY_DAYS = 7
FORECAST_INPUT_START_OFFSET = 3

# taken from https://gist.github.com/ihoromi4/b681a9088f348942b01711f251e5f964

def seed_everything(seed: int):
    import os
    import random
    import numpy as np
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)


seed_everything(42)

# Stock price history
@lru_cache(maxsize=10)
def fetch_stock_price(stock_id, start, end, interval="1h"):
    logger.info(f"Fetching historical stock price data for {stock_id} between {start} and {end}")
    return (
        yf.Ticker(stock_id)
        .history(start=start, end=end, interval=interval)
        .tz_convert(TIMEZONE)
    )


# Forecast
def forecast(stock_id, df):
    start_time = df.index[-1].to_pydatetime()
    n_forecast = 12
    x = [start_time + datetime.timedelta(hours=i) for i in range(1, 1 + n_forecast)]
    y = (
        df.Close.values.mean() + df.Close.values.std() * np.random.rand(n_forecast)
    ).tolist()
    return dict(x=x, y=y)


# App
app = Dash("Cassandra")

app.layout = html.Div(
    [
        dcc.Dropdown(
            id="stock-dropdown",
            options=[
                {"label": "Meta", "value": "META"},
                {"label": "Tesla", "value": "TSLA"},
                {"label": "Apple", "value": "AAPL"},
            ],
            value="META",
        ),
        dcc.Graph(id="stock-price-graph"),
    ],
    style={"width": "500"},
)


@app.callback(Output("stock-price-graph", "figure"), [Input("stock-dropdown", "value")])
def update_graph(stock_id):
    # stock price history
    end = datetime.datetime.now(tz=TIMEZONE)
    start = end - datetime.timedelta(days=HISTORY_DAYS)
    df = fetch_stock_price(stock_id, start.date().isoformat(), end.date().isoformat())
    # forecast
    input_df = df[end - datetime.timedelta(days=FORECAST_INPUT_START_OFFSET) :]
    forecast_data = forecast(stock_id, input_df)
    # representation
    history_data = {"x": df.index.tolist(), "y": df.Close.tolist(), "name": "History"}
    forecast_data["name"] = "Forecast"
    forecast_data["x"].insert(0, history_data["x"][-1])
    forecast_data["y"].insert(0, history_data["y"][-1])
    return dict(
        data=[history_data, forecast_data],
        layout=dict(
            margin={"l": 40, "r": 0, "t": 20, "b": 30},
            legend=dict(font=dict(size=14)),
        ),
    )


app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

if __name__ == "__main__":
    app.run_server(debug=True)
