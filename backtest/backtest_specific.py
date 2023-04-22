import numpy as np
import pandas as pd
import vectorbt as vbt

# Read data from csv
btc_price = pd.read_csv("data_1m.csv")[["timestamp", "close"]]
btc_price["date"] = pd.to_datetime(btc_price["timestamp"], unit="s")
btc_price = btc_price.set_index("date")["close"]

for window in range(1, 300): #optimize range
    # VectorBT part
    rsi = vbt.RSI.run(btc_price, window=100, short_name="rsi")

    # Levels
    entry = 33
    exit = 63.1

    # Calculate
    entries = rsi.rsi_crossed_below(entry)
    exits = rsi.rsi_crossed_above(exit)
    pf = vbt.Portfolio.from_signals(btc_price, entries, exits)

    # Print
    stats = pf.stats()
    # print(stats)

    total_return = stats[5] 
    total_trades = stats[11]

    print(f"window = {100}: return = {total_return} | trades = {total_trades}")