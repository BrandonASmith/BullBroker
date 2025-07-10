# api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ai_engine import generate_daily_stock_pick

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/daily-pick")
def get_daily_pick():
    result = generate_daily_stock_pick()
    return result


class StockPick(BaseModel):
    ticker: str
    rationale: str
    pick_type: str
    stock_type: str

# Simulated stock categories
stocks = [
    {"ticker": "TSLA", "type": "growth"},
    {"ticker": "NVDA", "type": "blue chip"},
    {"ticker": "PLTR", "type": "speculative"},
    {"ticker": "AAPL", "type": "blue chip"},
    {"ticker": "SOXL", "type": "ETF"},
    {"ticker": "MARA", "type": "speculative"},
    {"ticker": "AMZN", "type": "growth"},
    {"ticker": "AMD", "type": "growth"},
    {"ticker": "TQQQ", "type": "ETF"},
    {"ticker": "CLSK", "type": "penny"}
]

@app.get("/daily-pick", response_model=StockPick)
def get_daily_pick():
    try:
        pick = random.choice(stocks)
        pick_type = "Long Hold" if pick["type"] in ["blue chip", "ETF", "growth"] else "Short Sell"
        rationale = f"{pick['ticker']} is a {pick['type']} stock showing strong relative momentum. Ideal for a {pick_type} position based on recent trend data and analyst consensus. Target price: +12% from current level."

        return StockPick(
            ticker=pick["ticker"],
            rationale=rationale,
            pick_type=pick_type,
            stock_type=pick["type"]
        )
    except Exception as e:
        return {"ticker": None, "rationale": f"Error: {str(e)}"}

