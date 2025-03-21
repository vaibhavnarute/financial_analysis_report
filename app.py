import os
import yfinance as yf
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from alpha_vantage.timeseries import TimeSeries
from flask import Flask, request, jsonify
from fastapi import FastAPI
import uvicorn

from flask import jsonify
import pandas as pd


# Load environment variables
load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Flask App
flask_app = Flask(__name__)
fastapi_app = FastAPI()

# Fetch stock data
def fetch_stock_data(symbol):
    """Fetch stock data from Yahoo Finance."""
    try:
        symbol = symbol.strip()  # Remove unwanted spaces
        stock = yf.Ticker(symbol)
        data = stock.history(period='1mo')  # Fetch last month's data

        if data.empty:
            return {"error": "No data found. Check ticker symbol."}, 404

        # Convert index (datetime) to string for JSON serialization
        data.index = data.index.astype(str)
        return data.to_dict()
    
    except Exception as e:
        return {"error": f"Error fetching data: {str(e)}"}, 500

# Fetch Alpha Vantage data
def fetch_alpha_vantage_data(symbol):
    ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
    data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')
    return data

# Fetch financial news
def fetch_financial_news():
    url = "https://www.financialnews.com/latest"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = [item.text for item in soup.find_all('h2')][:5]
    return headlines

# Flask routes
@flask_app.route('/stock', methods=['GET'])
def get_stock():
    """API endpoint to fetch stock data."""
    symbol = request.args.get('symbol', '').upper()
    
    if not symbol:
        return jsonify({"error": "Stock symbol is required"}), 400
    
    data = fetch_stock_data(symbol)
    return jsonify(data)


@flask_app.route('/news', methods=['GET'])
def get_news():
    news = fetch_financial_news()
    return jsonify({'latest_news': news})

# Streamlit UI
st.title('Financial Analysis Dashboard')
stock_symbol = st.text_input("Enter Stock Symbol:")
if stock_symbol:
    stock_data = fetch_stock_data(stock_symbol)
    st.write(stock_data)
    fig = px.line(stock_data, x=stock_data.index, y='Close', title=f'{stock_symbol} Closing Prices')
    st.plotly_chart(fig)
    if st.button("Get Financial News"):
        news = fetch_financial_news()
        st.write(news)

if __name__ == '__main__':
    flask_app.run(port=5000)