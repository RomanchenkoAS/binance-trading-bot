import requests
import pandas as pd
import sys 
from datetime import datetime, timedelta

currency_pair = "btcusd"
url = f"https://www.bitstamp.net/api/v2/ohlc/{currency_pair}/"

# Before
start = datetime.now() - timedelta(30)
# Now
end = datetime.now()

dates = pd.date_range(start, end, freq="6H")
dates = [int(x.value/10**9) for x in list(dates)]

print([x.strftime("%m/%d/%Y, %H:%M:%S") for x in dates])

master_data = []

for first, last in zip(dates, dates[1:]):
    print(first, last)

    params = {
        "step": 60,  # seconds
        "limit": 1000,  # 1..1000
        "start": first,
        "end": last,
    }

    data = requests.get(url, params=params)

    data = data.json()["data"]["ohlc"]

    master_data += data

# Clear up the dataframe
df = pd.DataFrame(master_data)
df = df.drop_duplicates()

df["timestamp"] = df["timestamp"].astype(int)
df = df.sort_values(by="timestamp")

# Filter resulting dates to cut off extra ones
df = df[df["timestamp"] >= dates[0]]
df = df[df["timestamp"] < dates[-1]]

print(df)

# Write results to csv
df.to_csv("tutorial.csv", index=False)
