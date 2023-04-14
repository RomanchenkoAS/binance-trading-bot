import json
import requests
import pandas as pd
import datetime

currency_pair = 'btcusd'

URL = f'https://www.bitstamp.net/api/v2/ohlc/${currency_pair}/'