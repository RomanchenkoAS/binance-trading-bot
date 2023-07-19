import pandas as pd
import vectorbt as vbt

# Preferences
# metric = "positions.win_rate" # total_return | positions.win_rate
# metric = ("max_drawdown", ) # Must be a tuple
data_file = "data_1m.csv"

# Read data from csv
btc_price = pd.read_csv(data_file)[["timestamp", "close"]]
btc_price["date"] = pd.to_datetime(btc_price["timestamp"], unit="s")
btc_price = btc_price.set_index("date")["close"]

# VectorBT part
rsi = vbt.RSI.run(btc_price, window=100, short_name="rsi")

# Make a grid
entry_points = 32.76
exit_points = 62.83

entries = rsi.rsi_crossed_below(entry_points)
exits = rsi.rsi_crossed_above(exit_points)
pf = vbt.Portfolio.from_signals(btc_price, entries, exits)

print(pf.stats())

pf.plot().show()
