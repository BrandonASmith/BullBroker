from fastapi import FastAPI
from stock_data import fetch_stock_summary
from ai_engine import generate_stock_pick_rationale

app = FastAPI()

STOCK_POOL = ['NVDA', 'TSLA', 'AAPL', 'MSFT', 'AMD', 'GOOGL', 'META']

@app.get("/daily-pick")
def daily_stock_pick():
    for ticker in STOCK_POOL:
        try:
            print(f"📊 Trying {ticker}")
            summary = fetch_stock_summary(ticker)
            if not summary:
                continue

            rationale = generate_stock_pick_rationale(str(summary), ticker)
            if rationale:
                return {
                    "ticker": ticker,
                    "rationale": rationale
                }

        except Exception as e:
            print(f"❌ Error on {ticker}: {e}")

    return {"ticker": None, "rationale": "No valid pick generated today."}
