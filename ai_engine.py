import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

if not openai.api_key:
    raise RuntimeError("❌ OPENAI_API_KEY is not set.")

def generate_stock_pick_rationale(stock_data_summary, stock_ticker):
    prompt = f"""
You are an expert financial strategist and investment advisor.
Using the following stock data and recent trend summary for {stock_ticker}, recommend whether it is best suited for a day trade, an options strategy, or a long-term investment.

Include:
1. The pick type (e.g. "Pick Type: Long-Term Investment")
2. A concise rationale (100–150 words)

Stock data summary:
{stock_data_summary}

Respond in this format only:
Pick Type: [type]
[rationale paragraph]
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        output = response['choices'][0]['message']['content']
        print(f"✅ GPT-4 OUTPUT for {stock_ticker}:\n{output[:300]}")
        return output
    except Exception as e:
        print(f"❌ OpenAI request failed: {e}")
        return None
