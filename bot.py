# Requirements: python-decouple python-binance pandas pandas-ta 
# API : testnet.binance.vision 

from decouple import config
from binance.client import Client

print(config("API_KEY"))
print(config("SECRET_KEY"))

# testnet = True means all the trading is virtual 
client = Client(config("API_KEY"), config("SECRET_KEY"), testnet = True)





