import os
from dotenv import load_dotenv
import requests
import pandas as pd

load_dotenv()

API_KEY = os.getenv('ALPACA_API_KEY')
SECRET_KEY = os.getenv('ALPACA_SECRET_KEY')
BASE_URL = "https://paper-api.alpaca.markets"
DATA_URL = "https://data.alpaca.markets/v2"

HEADERS = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY
}

def get_historical_data(symbol, start, end, timeframe="1Min"):
    url = f"{DATA_URL}/stocks/{symbol}/bars"
    params = {
        "start": start,
        "end": end,
        "timeframe": timeframe,
        "adjustment": "raw",  # or "split" if you want split-adjusted data
        "limit": 10000        # max you can pull at once
    }
    
    response = requests.get(url, headers=HEADERS, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Data download error: {response.text}")
    
    data = response.json()["bars"]
    df = pd.DataFrame(data)
    df['t'] = pd.to_datetime(df['t'])
    df.set_index('t', inplace=True)
    return df

if __name__ == "__main__":
    # Example usage
    symbol = "AAPL"
    start = "2024-04-01T09:30:00-04:00"
    end = "2024-04-01T16:00:00-04:00"

    df = get_historical_data(symbol, start, end)
    print(df.head())