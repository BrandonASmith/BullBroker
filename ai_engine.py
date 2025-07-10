# ai_engine.py
import openai
import os
import yfinance as yf
import random
from datetime import datetime, timedelta

openai.api_key = os.getenv("OPENAI_API_KEY")

# Updated stock tracker list
stock_tracker = {
    "blue_chip": ["AAPL", "MSFT", "GOOGL", "JNJ", "JPM", "PG", "V", "NVDA", "UNH", "MA"],
    "growth": ["TSLA", "SHOP", "SQ", "ROKU", "ETSY", "SE", "U", "COIN", "NET", "DDOG"],
    "speculative": ["DNA", "ASTR", "BBIG", "MNMD", "IDEX", "FCEL", "NNDM", "SNDL", "BBAI", "AI"],
    "etf": ["SPY", "QQQ", "VTI", "ARKK", "XLF", "XLE", "XLV", "IWM", "EEM", "DIA"],
    "value": ["WMT", "KO", "PEP", "MCD", "T", "VZ", "PFE", "MRK", "INTC", "CSCO"],
    "penny": ["HCMC", "ZOM", "SNDL", "ENZC", "AITX", "CTRM", "CEI", "INND", "ILUS", "PHIL"]
}

all_tickers = sum(stock_tracker.values(), [])

def fetch_summary(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        info = stock.info

        return {
            "name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "marketCap": info.get("marketCap", 0),
            "volume": info.get("volume", 0),
            "previousClose": info.get("previousClose", 0),
            "50DayAverage": info.get("fiftyDayAverage", 0),
            "200DayAverage": info.get("twoHundredDayAverage", 0),
            "1moHistory": hist.tail(5).to_dict()
        }
    except Exception as e:
        return {"error": str(e)}

def classify_stock_type(ticker):
    for category, tickers in stock_tracker.items():
        if ticker in tickers:
            return category
    return "unknown"

def determine_pick_type(summary):
    try:
        previous = summary["previousClose"]
        average_50 = summary["50DayAverage"]
        average_200 = summary["200DayAverage"]
        market_cap = summary["marketCap"]

        if previous > average_50 and average_50 > average_200 and market_cap > 10_000_000_000:
            return "Long Hold"
        elif previous < average_50 and average_50 < average_200:
            return "Short Sell"
        else:
            return "Long Hold" if random.random() > 0.5 else "Short Sell"
    except:
        return "Unclear"

def generate_stock_pick_rationale(ticker, summary):
    stock_type = classify_stock_type(ticker)
    pick_type = determine_pick_type(summary)

    prompt = (
        f"You are an AI financial analyst. Analyze {ticker}, a {stock_type} stock."
        f" Classify the pick type as either Long Hold or Short Sell."
        f" Provide a clear rationale based on the latest data and news. Include a recommended target price and explain your reasoning."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional stock market analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    ai_text = response["choices"][0]["message"]["content"]
    return {
        "ticker": ticker,
        "stock_type": stock_type,
        "pick_type": pick_type,
        "rationale": ai_text
    }

def generate_daily_pick():
    attempts = 0
    while attempts < 5:
        ticker = random.choice(all_tickers)
        summary = fetch_summary(ticker)

        if "error" in summary or summary["previousClose"] == 0:
            attempts += 1
            continue

        try:
            return generate_stock_pick_rationale(ticker, summary)
        except Exception:
            attempts += 1

    return {"ticker": None, "rationale": "No valid pick generated today."}

# Optional: test run
if __name__ == "__main__":
    print(generate_stock_pick_rationale())
