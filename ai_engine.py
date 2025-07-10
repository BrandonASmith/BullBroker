import os
import openai
import random

# Get API key safely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY is not set.")

openai.api_key = OPENAI_API_KEY

# Sample high-quality tickers — you can extend or fetch dynamically
TICKER_LIST = [
    "AAPL", "MSFT", "NVDA", "TSLA", "AMD", "AMZN", "GOOGL", "META", "NFLX",
    "SMCI", "PLTR", "AVGO", "SHOP", "U", "ENPH", "SOFI", "RIVN", "CROX",
    "NIO", "F", "XOM", "LULU", "BX", "DKNG", "T", "INTC", "BABA"
]

# Map keywords to pick types
def infer_pick_type(text: str) -> str:
    text_lower = text.lower()
    if "day trade" in text_lower:
        return "Day Trade"
    elif "option" in text_lower or "call" in text_lower or "put" in text_lower:
        return "Options"
    elif "long-term" in text_lower or "hold" in text_lower:
        return "Long-Term"
    return "Unclear"

# Main function to call GPT and return a stock pick
def generate_stock_pick_rationale():
    ticker = random.choice(TICKER_LIST)

    prompt = f"""
You are BullBroker, an AI-powered financial advisor and expert stock strategist.
Today’s goal is to pick ONE U.S. stock to recommend based on the most recent news, macro trends, company performance, and investor sentiment.

Stock to evaluate today: {ticker}

For this stock, provide:
1. The investment strategy type (day trade, options play, or long-term hold).
2. A concise rationale (2-4 sentences) explaining why this stock is your pick today.

Return the result in this exact format:
---
Ticker: {ticker}
Pick Type: <Type>
Rationale: <Your explanation>
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        full_response = response["choices"][0]["message"]["content"].strip()
        print(f"💬 GPT Output:\n{full_response}")

        lines = full_response.splitlines()
        pick_type = "Unclear"
        rationale = "No rationale received."

        for line in lines:
            if line.lower().startswith("pick type:"):
                pick_type = line.split(":", 1)[1].strip()
            elif line.lower().startswith("rationale:"):
                rationale = line.split(":", 1)[1].strip()

        return {
            "ticker": ticker,
            "pick_type": pick_type,
            "rationale": rationale
        }

    except Exception as e:
        print(f"❌ GPT Error: {e}")
        return {
            "ticker": None,
            "pick_type": "Error",
            "rationale": "Failed to generate rationale."
        }
