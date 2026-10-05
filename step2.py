import sqlite3
import yfinance as yf

tickers = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ITC.NS"]

def get_prices(ticker):
    df = yf.Ticker(ticker).history(start="2015-01-01")
    df = df.reset_index()                                 # moves Date from the index into a normal column
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")       # clean date text
    df["ticker"] = ticker                                 # label each row with its stock
    return df[["ticker", "Date", "Open", "High", "Low", "Close", "Volume"]]

conn = sqlite3.connect("stocks.db")                       # creates the file if it doesn't exist
conn.execute("DROP TABLE IF EXISTS prices")               # start fresh each run

for t in tickers:
    df = get_prices(t)
    df.to_sql("prices", conn, if_exists="append", index=False)
    print(t, len(df), "rows saved")

conn.close()