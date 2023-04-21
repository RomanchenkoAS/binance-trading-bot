import numpy as np
import pandas as pd
import vectorbt as vbt

# Preferences
num = 10
metric = "positions.win_rate" # total_return | positions.win_rate
metric = ("max_drawdown", ) # Must be a tuple

# Read data from csv
btc_price = pd.read_csv("data_1d.csv")[["timestamp", "close"]]
btc_price["date"] = pd.to_datetime(btc_price["timestamp"], unit="s")
btc_price = btc_price.set_index("date")["close"]

# VectorBT part
rsi = vbt.RSI.run(btc_price, window=14, short_name="rsi")

# Make a grid
entry_points = np.linspace(1, 45, num=num)
exit_points = np.linspace(55, 99, num=num)

grid = np.array(np.meshgrid(entry_points, exit_points)).T.reshape(-1, 2)
entries = rsi.rsi_crossed_below(list(grid[:, [0]]))
exits = rsi.rsi_crossed_above(list(grid[:, [1]]))
pf = vbt.Portfolio.from_signals(btc_price, entries, exits)

pf_perf = pf.deep_getattr(metric)

pf_perf_matrix = pf_perf.vbt.unstack_to_df(
    index_levels="rsi_crossed_above",
    column_levels="rsi_crossed_below")

print(pf_perf_matrix)

pf_perf_matrix.vbt.heatmap(
    xaxis_title="entry",
    yaxis_title="exit").show()
