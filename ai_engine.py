import os
import openai
import random
import yfinance as yf
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file (optional for local dev)
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("❌ OPENAI_API_KEY is not set.")

# List of tracked stocks (500 high-quality tickers)
TRACKED_TICKERS = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "AVGO", "V", "UNH", "XOM", "JPM", "LLY", "MA", "JNJ", "PG",
    "HD", "ORCL", "COST", "MRK", "CVX", "ABBV", "ADBE", "PEP", "BAC", "NFLX", "TMO", "KO", "WMT", "AMD", "DIS", "QCOM",
    "INTC", "CRM", "MCD", "VZ", "ABT", "ACN", "TXN", "NEE", "LIN", "DHR", "BMY", "NKE", "AMGN", "MDT", "IBM", "LOW",
    "SBUX", "GS", "NOW", "ISRG", "GE", "SPGI", "BLK", "LRCX", "BKNG", "PLD", "CAT", "CHTR", "VRTX", "PANW", "AXP",
    "ADI", "REGN", "TGT", "CI", "MO", "CSCO", "ZTS", "PFE", "CB", "DE", "MMC", "C", "SYK", "ETN", "FISV", "TMUS",
    "ELV", "ADP", "EQIX", "SO", "BDX", "DUK", "GILD", "CL", "ATVI", "PSX", "AON", "AEP", "WM", "HCA", "NSC", "COF",
    "ADSK", "TRV", "EMR", "FDX", "WELL", "ECL", "APD", "ILMN", "D", "ADM", "KDP", "ROST", "HPQ", "WBA", "KHC", "MNST",
    "TSCO", "DAL", "ROKU", "LUV", "OKE", "EXPE", "TTWO", "ETSY", "ALGN", "MTCH", "FSLR", "NET", "ZS", "DDOG", "DOCU",
    "RIVN", "U", "PATH", "PLTR", "SNOW", "MDB", "SHOP", "SQ", "COIN", "ARKK", "SMCI", "ENPH", "SEDG", "F", "GM", "UBER"
]

def get_live_stock_data(ticker: str) -> dict:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")

        if hist.empty:
            raise ValueError("No price data found")

        last_quote = hist.iloc[-1]
        previous_quote = hist.iloc[-2]

        return {
            "price": round(last_quote["Close"], 2),
            "change": round(last_quote["Close"] - previous_quote["Close"], 2),
            "percent": round(((last_quote["Close"] - previous_quote["Close"]) / previous_quote["Close"]) * 100, 2),
            "history": hist
        }
    except Exception as e:
        print(f"❌ Error fetching stock data for {ticker}: {e}")
        return {}

def determine_pick_type(change: float, percent: float) -> str:
    if percent > 5:
        return "Momentum"
    elif percent < -5:
        return "Contrarian"
    elif change > 0:
        return "Growth"
    elif change < 0:
        return "Value"
    else:
        return "Neutral"

def generate_stock_pick_rationale(ticker: str, pick_type: str) -> str:
    today = datetime.now().strftime("%B %d, %Y")

    prompt = (
        f"As of {today}, explain why {ticker} is a strong {pick_type} investment pick today. "
        "Factor in market trends, sector performance, recent news, and technical indicators. "
        "Explain it like an expert financial strategist writing to a curious but non-professional trader. "
        "Make it persuasive and insightful in under 150 words."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ GPT Error:", e)
        return "No rationale received"

def get_daily_pick() -> dict:
    ticker = random.choice(TRACKED_TICKERS)
    stock_data = get_live_stock_data(ticker)

    if not stock_data:
        return {"ticker": None, "pick_type": None, "price": None, "rationale": "No data available."}

    pick_type = determine_pick_type(stock_data["change"], stock_data["percent"])
    rationale = generate_stock_pick_rationale(ticker, pick_type)

    return {
        "ticker": ticker,
        "pick_type": pick_type,
        "price": stock_data["price"],
        "change": stock_data["change"],
        "percent": stock_data["percent"],
        "rationale": rationale,
        "history": stock_data["history"]
    }
