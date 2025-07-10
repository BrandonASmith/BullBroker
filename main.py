# ai_engine.py

import yfinance as yf
import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

# Grouped list of quality tickers
TRACKED_STOCKS = {
    "blue_chip": ["AAPL", "MSFT", "JNJ", "V", "PG"],
    "growth": ["NVDA", "TSLA", "AMZN", "META", "GOOGL"],
    "speculative": ["PLTR", "SOFI", "RIVN", "IONQ", "ARKK"],
    "etf": ["SPY", "QQQ", "VTI", "DIA", "ARKK"],
    "value": ["WMT", "CVX", "PFE", "INTC", "KO"],
    "penny": ["GFAI", "COSM", "MMAT", "HCDI", "IDEX"]
}

def fetch_stock_summary(ticker):
    try:
        info = yf.Ticker(ticker).info
        return {
            "ticker": ticker,
            "summary": {
                "currentPrice": info.get("currentPrice"),
                "marketCap": info.get("marketCap"),
                "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
                "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
                "sector": info.ge
