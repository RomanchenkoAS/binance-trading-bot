import json
import requests
import pandas as pd
import datetime

currency_pair = 'btcusd'

URL = f'https://www.bitstamp.net/api/v2/ohlc/{currency_pair}/'

params = {
    'step' : 60,
    'limit' : 10 # 1 .. 1000
}

data = requests.get(URL, params=params).json()

# for line in data['data']['ohlc']:
#     print(line)
    
data = data['data']['ohlc']

df = pd.DataFrame(data)

print(df)

