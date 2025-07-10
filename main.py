from fastapi import FastAPI
from stock_data import fetch_stock_summary
from ai_engine import generate_stock_pick_rationale

app = FastAPI()

STOCK_POOL = ['AAPL']  # Limit to 1 ticker for speed

@app.get("/daily-pick")
def daily_stock_pick():
    try:
        ticker = 'AAPL'
        print(f"📊 Trying: {ticker}")
        summary = fetch_stock_summary(ticker)
        print(f"📄 Summary: {summary}")

        rationale = generate_stock_pick_rationale(str(summary), ticker)
        print(f"💬 GPT Output:\n{rationale}")

        return {
            "ticker": ticker,
            "rationale": rationale or "No rationale received"
        }

    except Exception as e:
        print(f"❌ Error: {e}")
        return {"ticker": None, "rationale": "Backend error."}
