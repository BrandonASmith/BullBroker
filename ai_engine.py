import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_stock_pick_rationale(stock_data_summary, stock_ticker):
    prompt = f"""
You are an expert financial strategist and investment advisor.
Using the following stock data and recent trend summary for {stock_ticker}, recommend whether it is best suited for a day trade, an options strategy, or a long-term investment.

Include:
1. The pick type
2. Why this stock is ideal today
3. Consider market sentiment, technicals, macro conditions

Stock data summary:
{stock_data_summary}

Output:
- Pick Type
- Short Summary (100-150 words)
"""

    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)

    return response['choices'][0]['message']['content']
