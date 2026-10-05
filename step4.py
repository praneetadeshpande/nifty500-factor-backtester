import sqlite3
import time
import pandas as pd
import yfinance as yf

# 1. Read the list of companies
constituents = pd.read_csv("nifty500.csv")
print(constituents.columns.tolist())          # shows the column names, so we can check "Symbol" exists
tickers = [s + ".NS" for s in constituents["Symbol"]]
tickers.append("^CRSLDX")                     # the Nifty 500 index itself, our benchmark later

# 2. The same recipe as before
def get_prices(ticker):
    df = yf.Ticker(ticker).history(start="2015-01-01")
    df = df.reset_index()
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    df["ticker"] = ticker
    return df[["ticker", "Date", "Open", "High", "Low", "Close", "Volume"]]

# 3. Open the database and see which stocks are already saved
conn = sqlite3.connect("stocks.db")
try:
    done = set(pd.read_sql("SELECT DISTINCT ticker FROM prices", conn)["ticker"])
except Exception:
    done = set()                              # table doesn't exist yet

# 4. Loop through every ticker
failed = []
for i, t in enumerate(tickers, start=1):
    if t in done:
        continue                              # skip stocks we already have
    try:
        df = get_prices(t)
        if df.empty:
            failed.append(t)
            continue
        df.to_sql("prices", conn, if_exists="append", index=False)
        print(i, "of", len(tickers), t, len(df), "rows")
    except Exception:
        failed.append(t)
    time.sleep(0.5)                           # small pause so Yahoo doesn't block us

conn.close()
print("Finished. Failed tickers:", failed)