import json
import requests
import pandas as pd
import datetime
import plotly.graph_objects as go

currency_pair = 'btcusd'
URL = f'https://www.bitstamp.net/api/v2/ohlc/{currency_pair}/'

start = "2021-01-01"
end = "2021-01-02"

# Create a time range
dates = pd.date_range(start, end, freq='12H')

# Transform ns -> s and into int, make a list
dates = [int(x.value/10**9) for x in list(dates)]

master_data = []

# Request data by time periods
for first, last in zip(dates, dates[1:]):
    print(f"{pd.to_datetime(first, unit='s')} ({first}) --> {pd.to_datetime(last, unit='s')} ({last})")
    params = {
        'step' : 60, # seconds
        'limit' : 1000, # 1 .. 1000
        'start' : first,
        'end' : last,
    }

    data = requests.get(URL, params=params).json()
        
    data = data['data']['ohlc']
    
    master_data += data

# Set all the resulting data as dataframe
df = pd.DataFrame(master_data)

# Remove duplicate data
df = df.drop_duplicates()

# Make sure timestamps are integer type
df['timestamp'] = df['timestamp'].astype(int)

# Sort by time
df.sort_values(by='timestamp')

# Filter rows from a specific datetime
df = df [ df['timestamp'] >= dates[0] ]
df = df [ df['timestamp'] < dates[-1] ]

# Create a datetime column
df['datetime'] = df['timestamp'].apply(lambda x: pd.to_datetime(x, unit='s'))

# Set index from 0
df.reset_index(inplace=True)
df.set_index('index', inplace=True)

print(df)

df.to_csv('data.csv', index=False)

# Configure plot
fig = go.Figure(data=[go.Candlestick(x=df['datetime'], open=df['open'],
                high=df['high'], low=df['low'], close=df['close'])])

fig.update_layout(xaxis_rangeslider_visible=False)  # Remove slider
fig.update_layout(template='plotly_dark') # Add some style
fig.update_layout(yaxis_title='BTCUSDT pair', xaxis_title='Date-time') # Name axes

# Display plot
fig.show()




