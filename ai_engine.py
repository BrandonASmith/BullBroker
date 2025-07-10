import openai
import yfinance as yf
import random
import os
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

CANDIDATE_TICKERS = [
    {"ticker": "MSFT", "type": "blue_chip"},
    {"ticker": "AAPL", "type": "blue_chip"},
    {"ticker": "TSLA", "type": "growth"},
    {"ticker": "NVDA", "type": "growth"},
    {"ticker": "PLTR", "type": "speculative"},
    {"ticker": "SOFI", "type": "speculative"},
    {"ticker": "AMD", "type": "growth"},
    {"ticker": "GOOGL", "type": "blue_chip"},
    {"ticker": "AMZN", "type": "blue_chip"},
    {"ticker": "META", "type": "blue_chip"},
]

def get_best_stock_today():
    valid_choices = []
    for stock in CANDIDATE_TICKERS:
        try:
            data = yf.Ticker(stock["ticker"]).history(period="1mo")
            if not data.empty:
                valid_choices.append(stock)
        except Exception as e:
            print(f"Skipping {stock['ticker']}: {e}")
            continue

    if not valid_choices:
        return {
            "ticker": None,
            "stock_type": None,
            "pick_type": None,
            "rationale": "No valid stocks found after filtering."
        }

    pick = random.choice(valid_choices)
    summary = get_stock_summary(pick["ticker"])

    rationale = generate_stock_pick_rationale(pick["ticker"], pick["type"], summary)

    return {
        "ticker": pick["ticker"],
        "stock_type": pick["type"],
        "pick_type": "Long Hold",
        "rationale": rationale
    }

def get_stock_summary(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return f"{info.get('longBusinessSummary', '')}\nMarket Cap: {info.get('marketCap', 'N/A')}\nPE Ratio: {info.get('trailingPE', 'N/A')}"
    except Exception as e:
        return "No stock summary available."

def generate_stock_pick_rationale(ticker, stock_type, summary):
    prompt = f"""
You are a professional stock analyst. Based on the following summary, generate a clear rationale for why {ticker} is a strong {stock_type} stock pick today. Be concise, include valuation, earnings, trends, and relevant market context.

Summary:
{summary}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating rationale: {e}"
