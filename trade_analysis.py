import pandas as pd
import os

folder_path = 'trades'

df = pd.DataFrame()

files = sorted(os.listdir(folder_path), reverse=False)

for filename in files:
    if os.path.isfile(f"{folder_path}/{filename}"):
        add = pd.read_csv(f"trades/{filename}")
        df = pd.concat([df, add], ignore_index=True)

trades = []

for index in range(0, len(df), 2):
    buy_trade = df.iloc[index]
    try:
        sell_trade = df.iloc[index + 1]
    except IndexError:
        # Last opened trade is not yet closed
        continue
    
    trade = {
        "sym": buy_trade['symbol'],
        "buy_price": buy_trade['price'],
        "sell_price": sell_trade['price'],
        "profit": sell_trade['price'] - buy_trade['price'],
        "profit%": 100 * (sell_trade['price'] - buy_trade['price']) / buy_trade['price']
    }

    trades.append(trade)

trades = pd.DataFrame(trades)

print(trades)


total_profit = trades["profit"].sum(axis=0)

print(f"Total profit earned = {total_profit:.2f}USDT")
