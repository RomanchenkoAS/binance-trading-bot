# Requirements: python-decouple python-binance pandas pandas-ta
# API : testnet.binance.vision

from decouple import config
from binance.client import Client
import pandas as pd
import pandas_ta as ta
import time
import json
import os
import sys
from datetime import datetime

# testnet = True means all the trading is virtual
client = Client(config("API_KEY"), config("SECRET_KEY"), testnet=True)
asset = "BTCUSDT"

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


def create_account():

    account = {
        "is_buying": True,
        "assets": {},
    }

    with open("bot_account.json", "w") as f:
        f.write(json.dumps(account))


def log(msg):
    message = f"{msg}"
    print("[LOG] ", message)
    
    # Create a directory for logs if not exist
    if not os.path.isdir("logs"):
        os.mkdir("logs")
    
    now = datetime.now()
    
    with open("logs/log.txt", "w") as f:
        f.write(str(now))
        f.write(message)

if __name__ == "__main__":

    rsi = get_rsi(asset)
    old_rsi = rsi # to check crossover event

    entry = 30
    exit = 70

    while True:
        
        try:
            if not os.path.exists("bot_account.json"):\
                create_account()
                
            with open("bot_account.json") as f:
                account = json.load(f)
                
            print("account: ", account)
            
            old_rsi = rsi
            rsi = get_rsi(asset)
            
            log("wow much trading")
            
            if account["is_buying"]:
                
                if rsi < entry and old_rsi > entry:
                    pass 
                    # trade
            
            else:
                
                if rsi > exit and old_rsi < exit:
                    pass
                    # trade
            
            print(rsi)
            
            time.sleep(5)
            
        except Exception as _ex:
            print("[ERR] Error: ", _ex)
            sys.exit()