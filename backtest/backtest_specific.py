import numpy as np
import pandas as pd
import vectorbt as vbt

# Preferences
# num = 10
# metric = "positions.win_rate" # total_return | positions.win_rate
# metric = ("max_drawdown", ) # Must be a tuple
# metric = "total_return"

# Read data from csv
btc_price = pd.read_csv("data_1m.csv")[["timestamp", "close"]]
btc_price["date"] = pd.to_datetime(btc_price["timestamp"], unit="s")
btc_price = btc_price.set_index("date")["close"]

# VectorBT part
rsi = vbt.RSI.run(btc_price, window=100, short_name="rsi")

# Levels
entry = 32.8
exit = 63.1

entries = rsi.rsi_crossed_below(entry)
exits = rsi.rsi_crossed_above(exit)
pf = vbt.Portfolio.from_signals(btc_price, entries, exits)

print(pf.stats())