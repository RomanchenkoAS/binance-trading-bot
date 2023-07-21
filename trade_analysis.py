import os
import sys
from datetime import datetime
import pandas as pd

folder_path = "trades"

df = pd.DataFrame()

files = sorted(os.listdir(folder_path), reverse=False)

for filename in files:
    if os.path.isfile(f"{folder_path}/{filename}"):
        add = pd.read_csv(f"trades/{filename}")
        # Get filename without extension
        date = os.path.splitext(filename)[0]
        add["date"] = date
        df = pd.concat([df, add], ignore_index=True)

# To see full history use "full" key on launch
if len(sys.argv) > 1 and sys.argv[1] == "full":
    # Set the options to display unlimited rows and columns
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)

trades = []

for index in range(0, len(df), 2):
    buy_trade = df.iloc[index]
    try:
        sell_trade = df.iloc[index + 1]
    except IndexError:
        # Last opened trade is not yet closed
        continue

    trade = {
        "sym": buy_trade["symbol"],
        "date": buy_trade["date"],
        "buy_price": buy_trade["price"],
        "sell_price": sell_trade["price"],
        "profit": sell_trade["price"] - buy_trade["price"],
        "profit%": 100
        * (sell_trade["price"] - buy_trade["price"])
        / buy_trade["price"],
    }

    trades.append(trade)

trades = pd.DataFrame(trades)
trades["buy_price"] = trades["buy_price"].astype(float).round(3)
trades["sell_price"] = trades["sell_price"].astype(float).round(3)
trades["profit"] = trades["profit"].astype(float).round(3)
trades["profit%"] = trades["profit%"].astype(float).round(3)
print(trades)

# Show totals
total_profit = trades["profit"].sum(axis=0)
total_profit_p = trades["profit%"].sum(axis=0)
total_profit_str = f"+{total_profit:.2f}%" if total_profit >= 0 else f"{total_profit:.2f}%"
total_profit_p_str = f"+{total_profit_p:.2f}%" if total_profit_p >= 0 else f"{total_profit_p:.2f}%"
totals = f"Total profit earned = {total_profit_str}USDT ({total_profit_p_str})"
print(totals)

# Show daily
date_start = trades["date"].iloc[0]
date_over = trades["date"].iloc[-1]
date_start = datetime.strptime(date_start, "%Y-%m-%d")
date_over = datetime.strptime(date_over, "%Y-%m-%d")
delta = date_over - date_start
totals = f"Data recordered for {delta.days} days, totaling daily return +{total_profit_p / delta.days :.2f}%" 
if total_profit_p < 0:
    totals.replace("+", "-")
print(totals)
