import yfinance as yf

df = yf.Ticker("TCS.NS").history(start="2015-01-01")
print(df.head())
print(len(df), "rows")