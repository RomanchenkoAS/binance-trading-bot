import json
import requests
import pandas as pd
import datetime
import plotly.graph_objects as go

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

df['datetime'] = df['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(int(x)))

print(df)

# Configure plot
fig = go.Figure(data=[go.Candlestick(x=df['datetime'], open=df['open'],
                high=df['high'], low=df['low'], close=df['close'])])

fig.update_layout(xaxis_rangeslider_visible=False)  # Remove slider
fig.update_layout(template='plotly_dark') # Add some style
fig.update_layout(yaxis_title='BTCUSDT pair', xaxis_title='Date-time') # Name axes

# Display plot
fig.show()

