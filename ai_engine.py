# ai_engine.py

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_best_stock_today():
    prompt = (
        "Based on current financial trends, news, earnings reports, and market sentiment, "
        "select one stock (in the US market) with the highest potential return today. "
        "Provide: ticker, stock_type (blue_chip, growth, speculative), pick_type (Long Hold, Day Trade, Options, Short Sell), "
        "target price, and a detailed AI-generated rationale.\n\n"
        "Respond in JSON format with keys: ticker, stock_type, pick_type, rationale."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        content = response["choices"][0]["message"]["content"]

        # Try parsing JSON content
        import json
        return json.loads(content)

    except Exception as e:
        print(f"Error in get_best_stock_today: {e}")
        return {"ticker": "", "stock_type": "", "pick_type": "", "rationale": ""}

