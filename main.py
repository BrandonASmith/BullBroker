from fastapi import FastAPI
from stock_data import fetch_stock_summary
from ai_engine import generate_stock_pick_rationale

app = FastAPI()

STOCK_POOL = ['NVDA', 'TSLA', 'AAPL', 'MSFT', 'AMD', 'GOOGL', 'META']

@app.get("/daily-pick")
def daily_stock_pick():
    best_pick = None
    best_rationale = ""

    for ticker in STOCK_POOL:
        try:
            summary = fetch_stock_summary(ticker)
            rationale = generate_stock_pick_rationale(str(summary), ticker)
            if not best_pick:
                best_pick = ticker
                best_rationale = rationale
        except Exception as e:
            print(f"Error processing {ticker}: {e}")

    return {
        "ticker": best_pick,
        "rationale": best_rationale
    }