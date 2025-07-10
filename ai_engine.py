import os
import openai
import yfinance as yf
import json
import datetime

# Load OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")

# -----------------------------
# === STOCK UNIVERSE GROUPS ===
# -----------------------------
blue_chip_stocks = ["AAPL", "MSFT", "GOOGL", "NVDA", "AMZN", "JPM", "UNH", "PG", "V", "XOM"]
growth_stocks = ["TSLA", "SHOP", "U", "CRWD", "NET", "PLTR", "ABNB", "SNOW", "DDOG", "MDB"]
speculative_stocks = ["AI", "BBAI", "DNA", "IDEX", "NVOS", "ASTS", "SOUN", "IONQ", "LIFW", "MVIS"]
etfs = ["QQQ", "SPY", "VTI", "ARKK", "XLK", "SMH", "SOXX", "IWM", "XLF", "XLE"]
value_stocks = ["PEP", "KO", "MCD", "WMT", "HD", "CVX", "TGT", "LMT", "BA", "IBM"]
penny_stocks = ["PLUG", "FCEL", "NKLA", "RIG", "TLRY", "HUSA", "CEI", "BBIG", "WISH", "GROM"]

# Combine into one master list
stock_universe = (
    blue_chip_stocks +
    growth_stocks +
    speculative_stocks +
    etfs +
    value_stocks +
    penny_stocks
)

# -----------------------------
# === DATA COLLECTION LOGIC ===
# -----------------------------
def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        history = stock.history(period="5d")
        summary = {
            "name": info.get("shortName"),
            "sector": info.get("sector"),
            "marketCap": info.get("marketCap"),
            "volume": info.get("volume"),
            "previousClose": info.get("previousClose"),
            "50DayAverage": info.get("fiftyDayAverage"),
            "200DayAverage": info.get("twoHundredDayAverage"),
            "1moHistory": history.tail(5).to_dict()
        }
        return summary
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# -----------------------------
# === MAIN AI DECISION ENGINE ===
# -----------------------------
def generate_stock_pick_rationale():
    today = datetime.date.today().isoformat()
    candidates = []

    for ticker in stock_universe:
        data = fetch_stock_data(ticker)
        if data:
            candidates.append((ticker, data))
        if len(candidates) >= 10:  # limit how many we analyze at once
            break

    if not candidates:
        return {
            "ticker": None,
            "rationale": "No valid pick generated today."
        }

    # Format data for prompt
    formatted_data = "\n".join([
        f"{ticker}: {json.dumps(data)}"
        for ticker, data in candidates
    ])

    prompt = f"""
You are a world-class AI financial analyst trained in market data, investor psychology, and global economic conditions.

You will be shown 10 stock summaries pulled from current data. Choose the **single best stock pick for today**.

Your answer **must include**:
- Ticker (e.g., AAPL)
- Pick Type: "Long Hold" or "Short Sell"
- Stock Type: Blue Chip, Growth, Speculative, ETF, Value, or Penny Stock
- A 2–4 sentence rationale referencing price trends, volume, valuation, or macroeconomic reasoning
- A target price (short or long term) and a recommended holding period if applicable

Here is the data:
{formatted_data}

Return only this JSON:
{{
  "ticker": "...",
  "pick_type": "...",
  "stock_type": "...",
  "rationale": "..."
}}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=500
        )
        response_text = response.choices[0].message.content.strip()
        print("[GPT Output Raw]:", response_text)

        parsed = json.loads(response_text)
        if parsed.get("ticker") and parsed.get("pick_type") and parsed.get("rationale"):
            return parsed
        else:
            raise ValueError("Incomplete GPT response")

    except Exception as e:
        print("[AI ERROR]:", e)
        return {
            "ticker": None,
            "rationale": "No valid pick generated today."
        }

# Optional: test run
if __name__ == "__main__":
    print(generate_stock_pick_rationale())
