# Binance trading bot ⚡️
This is an indicator-based binance trading bot & script to scrape / backtest historical data.

## Objectives 🎯

- Scrape historical candlestick data from Binance exchange
- Backtest a specific strategy against historical data and show a heatmap for a range of strategy coefficients
- Create a bot that trades on Binance testnet using a chosen strategy and records its actions to a CSV and log file
- Analyze trades and show a dataframe and returns of the trading strategy

## Goals (TODO) ✔️

- [x] Launch bot at a remote VM
- [ ] Implement and test additional strategies
- [ ] Implement the bot on the live Binance exchange and track its performance
- [ ] Use ML to optimize live strategy coefficients and parameters
- [ ] Build a front-end interface to visualize bot performance and trading activity

## Technologies used 🛠

 - Python 
 - Plotly
 - Pandas
 - Numpy
 - VectorBT
 - Binance Client
 - [Bitstamp](https://www.bitstamp.net/api/) - for scraping 

## Description 🤔

#### Scraping

To scrape data I am using **Bitstamp API** (web link). It is fairly simple: choose dates and generate according timestamps, make a request, recieve Open-High-Low-Close data (candlesticks), strip surplus from recieved data and write to csv using **pandas**.
- API: https://www.bitstamp.net/api/
- URL: https://www.bitstamp.net/api/v2/ohlc/{currency_pair}/

Some info about process is shown to the user to make sure all the numbers are correct:

<p align="center">
<img src="https://user-images.githubusercontent.com/119735427/235074146-41d7eddb-07b8-4ff3-9027-3199f773320b.png" alt="alt-text">
</p>

As a little extra: scraping.py builds a candlestick plot from recieved data with **plotly**:
<p align="center">
<img src="https://user-images.githubusercontent.com/119735427/235073869-ed1cbb39-5fc5-4921-9b18-7071671f18e1.png" alt="alt-text">
</p>


#### Backtest

- backtest.py : test chosen strategy against a grid of coefficients
- backtest_single.py : test a single pair of coefficients and get in-depth data
- backtest_optimize.py : with a single pair of coefficients optimize "window" size at which RSI is calculated 

Now we can apply any chosen strategy to this historical data. To do this, I am using **VectorBT library**. It is really convenient to use, because it requires no class - based strategy, just a simple declaration of chosen indicator and border points.
In this case I am using relative-strength indicator (aka RSI) to find my entry & exit points. General idea is: we must buy the commodity whenever it is oversold, and sell it once it becomes overbought. RSI moves in range from 1 to 100, and it is generally advised to buy at RSI=30 and then sell at RSI=70.
Let us apply RSI strategy with these levels to 1 month worth of candlesticks data :

<p align="center">
<img src="https://user-images.githubusercontent.com/119735427/235079062-e8056a1f-03d1-4d96-988b-e9af23a3f261.png" alt="alt-text">
</p>

As we can see 30-70 RSI strategy returned 5.3% profit whereas benchmark returned only 3.7%. That is alright, but not good enough, it is time to play with borders a little. VectorBT allows to run multiple tests at once with a range of coefficients, so we set range for entry=(1..50) and exit=(50..99), and create a linear space grid (using numpy) to check all of those combinations and recieve total return of each pair. 

<p align="center">
<img src="https://user-images.githubusercontent.com/119735427/235080396-0f32d85d-68c5-4102-8777-d2626d82d192.png" alt="alt-text">
</p>

This heatmap shows a large portions of entry&exit pairs with return = 0, that means no trades were made with these coefficients.
Yellow squares point out the most successful pairs, so we narrow down the range and increase fragmentation to find the most efficient combination.
With range entry=(30..50) & exit=(58..72):

<p align="center">
<img src="https://user-images.githubusercontent.com/119735427/235081891-5291af99-f4bb-43a3-be6f-bed0cbfc0ebf.png" alt="alt-text">
</p>

Now, almost 15% for a month is an outstanding strategy, let's check these entry&exit points statistic:

<p align="center">
<img src="https://user-images.githubusercontent.com/119735427/235082661-e99625f9-042e-4a71-9f4d-0801a5b72718.png" alt="alt-text">
</p>

Alongside dry text statistic we can build a plot for this strategy:

<p align="center">
<img src="https://user-images.githubusercontent.com/119735427/235082911-49429047-6ae6-4944-99f8-e4336f957851.png" alt="alt-text">
</p>

This looks real nice, next step is **forward-testing** this strategy.

#### Forward-testing (a.k.a. trading bot)


