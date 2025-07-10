import os
import random
import openai
import yfinance as yf
from datetime import datetime, timedelta

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("❌ OPENAI_API_KEY is not set.")

# Define categorized ticker groups
blue_chip_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "UNH", "JNJ", "PG", "V", "MA", "HD", "MRK"]
growth_stocks = ["TSLA", "SHOP", "SQ", "UBER", "ABNB", "CRWD", "ZS", "NET", "DDOG", "SNOW", "MDB", "PLTR"]
speculative_stocks = ["AMPX", "BIG", "WISH", "NKLA", "BBIG", "SOUN", "AI", "BBAI", "NIO", "RIVN"]
value_stocks = ["KO", "PEP", "WMT", "CVX", "XOM", "PFE", "INTC", "CSCO", "MDLZ", "ORCL"]
etf_stocks = ["SPY", "QQQ", "VTI", "ARKK", "DIA", "IWM", "XLF", "XLV", "XLK", "XLE", "SCHD", "SCHB"]
penny_stocks = ["TRKA", "HUSA", "MULN", "COSM", "BRDS", "GFAI", "SINT", "AVGR", "VINE"]

# Combine all tickers
top_stock_tickers = list(set(
    blue_chip_stocks + growth_stocks + speculative_stocks + value_stocks + etf_stocks + penny_stocks
))

# Classify ticker
def classify_ticker(ticker):
    if ticker in blue_chip_stocks:
        return "blue chip"
    elif ticker in growth_stocks:
        return "growth"
    elif ticker in speculative_stocks:
        return "speculative"
    elif ticker in value_stocks:
        return "value"
    elif ticker in etf_stocks:
        return "ETF"
    elif ticker in penny_stocks:
        return "penny"
    return "unclassified"

# Determine pick type
def determine_pick_type(data):
    recent = data.get("change_month", 0)
    long_term = data.get("change_year", 0)

    if long_term > 25 and recent > 5:
        return "Long Hold"
    elif recent < -5 and long_term < 0:
        return "Short Sell"
    elif long_term > 10:
        return "Long Hold"
    elif recent < -10:
        return "Short Sell"
    return "Long Hold"

# Pull stock info
def get_stock_summary(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Price history
        today = datetime.now()
        history = stock.history(period="1y")
        if history.empty or "Close" not in history:
            return None

        current_price = history["Close"][-1]
        month_ago = today - timedelta(days=30)
        year_ago = today - timedelta(days=365)

        past_month = history.loc[history.index >= month_ago]
        past_year = history.loc[history.index >= year_ago]

        change_month = ((past_month["Close"][-1] - past_month["Close"][0]) / past_month["Close"][0]) * 100 if len(past_month) > 1 else 0
        change_year = ((past_year["Close"][-1] - past_year["Close"][0]) / past_year["Close"][0]) * 100 if len(past_year) > 1 else 0

        return {
            "ticker": ticker,
            "name": info.get("shortName", ""),
            "sector": info.get("sector", ""),
            "marketCap": info.get("marketCap", 0),
            "currentPrice": current_price,
            "change_month": round(change_month, 2),
            "change_year": round(change_year, 2),
            "classification": classify_ticker(ticker)
        }
    except Exception:
        return None

# Select best stock
def choose_top_candidate():
    valid = []
    random.shuffle(top_stock_tickers)

    for ticker in top_stock_tickers:
        summary = get_stock_summary(ticker)
        if summary:
            valid.append(summary)
        if len(valid) >= 5:
            break

    if valid:
        sorted_valid = sorted(valid, key=lambda x: x["change_month"], reverse=True)
        return sorted_valid[0]
    return None

# Create rationale
def generate_stock_pick_rationale(summary):
    ticker = summary["ticker"]
    classification = summary["classification"]
    pick_type = determine_pick_type(summary)

    prompt = (
        f"You are a financial analyst. Based on current market trends, "
        f"news, macroeconomic factors, and recent stock movement, explain why {ticker} "
        f"is the top stock pick today. Clearly state the investment classification ({classification}), "
        f"the recommended action type ({pick_type}), and a reasonable price target. "
        f"Use data-driven analysis with a confident tone."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert financial strategist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message["content"].strip(), pick_type

# Main export
def get_today_stock_pick():
    summary = choose_top_candidate()

    if summary:
        try:
            rationale, pick_type = generate_stock_pick_rationale(summary)
        except Exception as e:
            rationale = "AI failed to generate a rationale."
            pick_type = determine_pick_type(summary)
    else:
        return {
            "ticker": None,
            "pick_type": None,
            "classification": None,
            "rationale": "No valid pick generated today."
        }

    return {
        "ticker": summary["ticker"],
        "classification": summary["classification"],
        "pick_type": pick_type,
        "current_price": summary["currentPrice"],
        "change_month": summary["change_month"],
        "change_year": summary["change_year"],
        "rationale": rationale
    }
