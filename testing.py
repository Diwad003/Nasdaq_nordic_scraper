import yfinance as yf

# Fetch data for CLA-B.ST
stock = yf.Ticker("CLA-B.ST")

# Get historical dividend data
dividends = stock.dividends

# Print the dividend data
print(dividends)
