import sqlite3
import pandas as pd

conn = sqlite3.connect("stocks.db")

query = """
SELECT ticker, Date, Close
FROM prices
WHERE ticker = 'TCS.NS'
ORDER BY Date DESC
LIMIT 5
"""
print(pd.read_sql(query, conn))
conn.close()