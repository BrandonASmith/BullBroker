import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

if not openai.api_key:
    raise RuntimeError("❌ OPENAI_API_KEY is not set.")

def generate_stock_pick_rationale(stock_data_summary, stock_ticker):
    prompt = f"""
You are an expert investment strategist.

Analyze the following stock data and choose whether {stock_ticker} is best for:
- A Day Trade
- An Options Trade
- A Long-Term Investment

Respond in this **exact format**:

Pick Type: [Day Trade | Options Trade | Long-Term Investment]

[Your 100-150 word rationale.]

Stock Summary:
{stock_data_summary}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        content = response["choices"][0]["message"]["content"]
        print(f"\n✅ GPT-4 RESPONSE for {stock_ticker}:\n{content}\n")
        return content
    except Exception as e:
        print(f"❌ GPT Error: {e}")
        return "No rationale received"
