import sqlite3
import pandas as pd

conn = sqlite3.connect("stocks.db")

# Overall summary
query1 = """
SELECT COUNT(DISTINCT ticker) AS stocks,
       COUNT(*) AS total_rows,
       MIN(Date) AS first_date,
       MAX(Date) AS last_date
FROM prices
"""
print(pd.read_sql(query1, conn))

# The 10 stocks with the least history
query2 = """
SELECT ticker, COUNT(*) AS days, MIN(Date) AS first_date
FROM prices
GROUP BY ticker
ORDER BY days ASC
LIMIT 10
"""
print(pd.read_sql(query2, conn))

conn.close()