import os
import openai
import random
import yfinance as yf
from datetime import datetime, timedelta

openai.api_key = os.getenv("OPENAI_API_KEY")

# Top 500 stock tickers (sample for now, replace with your list if needed)
top_stock_tickers = [
    "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "BRK-B", "JPM", "V",
    "UNH", "AVGO", "JNJ", "WMT", "MA", "XOM", "LLY", "PG", "ORCL", "HD", "COST",
    "MRK", "CVX", "PEP", "ABBV", "ADBE", "BAC", "KO", "NFLX", "ACN", "TMO", "AMD",
    "ABT", "CRM", "INTC", "DHR", "MCD", "NKE", "VZ", "TXN", "WFC", "LIN", "NEE",
    "QCOM", "UPS", "PM", "LOW", "MS", "BMY", "AMAT", "SBUX", "INTU", "GS", "IBM",
    "RTX", "PLD", "CAT", "HON", "BLK", "GE", "AMGN", "DE", "ISRG", "ADI", "MDT"
    # Add more tickers to reach 500 as needed
]

def get_stock_summary(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="5d")
        if hist.empty:
            return None

        close = hist["Close"].iloc[-1]
        previous_close = hist["Close"].iloc[-2]
        percent_change = ((close - previous_close) / previous_close) * 100

        return {
            "ticker": ticker,
            "company": info.get("shortName", ""),
            "sector": info.get("sector", ""),
            "marketCap": info.get("marketCap", 0),
            "summary": info.get("longBusinessSummary", ""),
            "price": round(close, 2),
            "change": round(percent_change, 2),
        }
    except Exception:
        return None

def choose_top_candidate():
    random.shuffle(top_stock_tickers)
    for ticker in top_stock_tickers:
        summary = get_stock_summary(ticker)
        if summary:
            return summary
    return None

def generate_stock_pick_rationale(summary):
    if not summary:
        return {"ticker": None, "rationale": "No valid pick generated today."}

    prompt = f"""
You are a financial strategist and expert stock analyst. Given the following stock data, generate an investment rationale.

Stock: {summary["ticker"]} ({summary["company"]})
Sector: {summary["sector"]}
Market Cap: {summary["marketCap"]}
Current Price: ${summary["price"]}
1-Day % Change: {summary["change"]}%
Business Summary: {summary["summary"]}

Your task:
- Recommend this stock only if it is truly the BEST pick today.
- Specify the investment type: "Long Hold" (for strong long-term plays) or "Short Sell" (if the stock will likely decline soon).
- Provide a target price (higher for long, lower for short).
- Classify the stock (e.g., growth, value, speculative, blue chip).
- Give a compelling reason using insights from recent trends, momentum, and overall market conditions.

Respond in this JSON format ONLY:
{{
  "ticker": "AAPL",
  "pick_type": "Long Hold",
  "target_price": 230.00,
  "stock_class": "blue chip",
  "rationale": "Apple continues to outperform expectations with strong hardware and service sales. With AI integration expected in iOS 19 and global iPhone upgrades accelerating, AAPL has momentum. Based on current patterns, it may rise to $230 in the next quarter."
}}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        content = response.choices[0].message["content"]

        # Safe parsing of JSON output
        import json
        parsed = json.loads(content)
        if "ticker" in parsed and "rationale" in parsed:
            return parsed
        else:
            return {"ticker": None, "rationale": "AI returned malformed result."}

    except Exception as e:
        return {"ticker": None, "rationale": f"OpenAI Error: {str(e)}"}

def get_best_stock_pick():
    summary = choose_top_candidate()
    return generate_stock_pick_rationale(summary)
