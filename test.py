import yfinance as yf
import pandas as pd

# List of stock tickers
tickers = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN"]

# Time period for historical data
period = "1mo"  # Options: "1d", "5d", "1mo", "6mo", "1y", "5y"

# Fetch stock data
stock_data = {}
for ticker in tickers:
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)

    # Get additional stock info
    stock_info = stock.info
    stock_data[ticker] = {
        "Market Cap": stock_info.get("marketCap", "N/A"),
        "P/E Ratio": stock_info.get("trailingPE", "N/A"),
        "52-Week High": stock_info.get("fiftyTwoWeekHigh", "N/A"),
        "52-Week Low": stock_info.get("fiftyTwoWeekLow", "N/A"),
        "Dividend Yield": stock_info.get("dividendYield", "N/A"),
        "Volume": hist["Volume"].iloc[-1] if not hist.empty else "N/A",
        "Last Close Price": hist["Close"].iloc[-1] if not hist.empty else "N/A"
    }

# Convert to DataFrame for better visualization
df = pd.DataFrame(stock_data).T  # Transpose for readability
print("\n✅ Yahoo Finance Data Retrieval Successful!\n")
print(df)
