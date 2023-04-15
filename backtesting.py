import numpy as np
import pandas as pd
from datetime import datetime
import vectorbt as vbt

num = 50
metric = 'total_return'

btc_price = pd.read_csv('btcusdt.csv')[['datetime', 'close']]

# Make data into approriate for vectorBt format
btc_price = btc_price.set_index("datetime")['close']

parameters = {
    'window': 14,
    'entry': 45,  # 49.9
    'exit': 55  # 50.1
}

# Create evenly distributed array of entry/exit points for optimization
entry_points = np.linspace(55, 30, num=num)
exit_points = np.linspace(45, 70, num=num)

# print(entry_points)
# print(exit_points)

# Define strategy: RSI = relative strength index
rsi = vbt.RSI.run(btc_price, window=14, short_name="rsi")

entries = rsi.rsi_crossed_below(list(entry_points))
exits = rsi.rsi_crossed_above(list(exit_points))

# Make a VectorBT calculation
pf = vbt.Portfolio.from_signals(btc_price, entries, exits)

# Calculate performance for entry/exit pairs
pf_perf = pf.deep_getattr(metric)

pf_perf_matrix = pf_perf.vbt.unstack_to_df(
    index_levels="rsi_crossed_above", column_levels="rsi_crossed_below")

pf_perf_matrix.vbt.heatmap(
    xaxis_title="entry",
    yaxis_title="exit").show()

print(pf_perf)

print(pf.stats())

pf.plot().show()
print(btc_price)
