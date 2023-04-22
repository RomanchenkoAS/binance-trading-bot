import pandas as pd
import os


folder_path = 'trades'

trades = pd.DataFrame()

for filename in os.listdir(folder_path):
    print(filename)
    add = pd.read_csv(f"trades/{filename}")
    trades = pd.concat([trades, add], ignore_index=True)
        
# print(trades)

sum = 0
for i, row in trades.iterrows():
    # print(row)
    sum = sum - row['price'] if row['side'] == 'buy' else sum + row['price']
    
print(sum)