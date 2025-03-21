import requests
from load import ALPHA_VANTAGE_API_KEY

def fetch_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    print(f"Fetching data from: {url}")  # Debugging
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "Time Series (Daily)" in data:
            return data["Time Series (Daily)"]
        else:
            print("Invalid API response:", data)  # Debugging
            return None
    else:
        print("Failed to fetch stock data.")
        return None

if __name__ == "__main__":
    symbol = "AAPL"  # Test with Apple stock
    stock_data = fetch_stock_data(symbol)
    print(stock_data)
