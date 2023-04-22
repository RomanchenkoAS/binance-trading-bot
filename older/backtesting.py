import numpy as np
import pandas as pd
from datetime import datetime
import vectorbt as vbt

num = 10
metric = "total_return" # total_return | positions.win_rate

# Read csv file
btc_price = pd.read_csv("data_2m.csv")[["timestamp", "close"]]
btc_price["date"] = pd.to_datetime( btc_price["timestamp"], unit = "s")

# Make data into approriate for vectorBt format
btc_price = btc_price.set_index("date")["close"]

parameters = {
    "window": 14,
    "entry": 45,  # 49.9
    "exit": 55  # 50.1
}

# Define strategy: RSI = relative strength index
rsi = vbt.RSI.run(btc_price, window=14, short_name="rsi")

# Create evenly distributed array of entry/exit points for optimization
entry_points = np.linspace(1, 45, num=num)
exit_points = np.linspace(55, 99, num=num)

# Make a nice numpy grid by combinating all the possibilities in those two lists
grid = np.array(np.meshgrid(entry_points, exit_points)).T.reshape(-1,2)
# print(grid)

# print(entry_points) 
# print(exit_points)

entries = rsi.rsi_crossed_below(list(grid[ : ,[0]]))
exits = rsi.rsi_crossed_above(list(grid[ : ,[1]]))

# Make a VectorBT calculation
pf = vbt.Portfolio.from_signals(btc_price, entries, exits)

# Calculate performance for entry/exit pairs
pf_perf = pf.deep_getattr(metric)

pf_perf_matrix = pf_perf.vbt.unstack_to_df(
    index_levels="rsi_crossed_above", column_levels="rsi_crossed_below")#, symmetric=True)

pf_perf_matrix.vbt.heatmap(
    xaxis_title="entry",
    yaxis_title="exit").show()

# print(pf_perf)

# print(pf.stats())

# pf.plot().show()
# print(btc_price)
