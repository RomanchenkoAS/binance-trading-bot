# Requirements: python-decouple python-binance pandas pandas-ta
# API : testnet.binance.vision

from decouple import config
from binance.client import Client
import pandas as pd
import pandas_ta as ta
import time
import json

# testnet = True means all the trading is virtual
client = Client(config("API_KEY"), config("SECRET_KEY"), testnet=True)

# Balance check
# balance = client.get_asset_balance(asset="BTC")
# print(balance)


def fetch_klines(asset):

    klines = client.get_historical_klines(
        asset, Client.KLINE_INTERVAL_1MINUTE, "1 hour ago UTC")

    klines = [[x[0], float(x[4])] for x in klines]

    klines = pd.DataFrame(klines, columns=["time", "price"])
    klines["time"] = pd.to_datetime(klines["time"], unit="ms")

    return klines


def get_rsi(asset):

    klines = fetch_klines(asset)
    klines["rsi"] = ta.rsi(close=klines["price"], length=14)

    return klines["rsi"].iloc[-1]


# for i in range(0, 10):
#     rsi = get_rsi("BTCUSDT")
#     print(rsi)
#     time.sleep(5)

def create_account():
    
    pass

    account = {
        "is_buying":True,
        "assets":{},
    }
    
    with open("bot_account.json", "w") as f:
        f.write( json.dumps(account))
        
create_account()