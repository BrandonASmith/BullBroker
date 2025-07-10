import os
import openai
import yfinance as yf
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

# Categorized Ticker Universe for BullBroker
categorized_tickers = {
    'speculative': ['PLTR', 'RIVN', 'DNA', 'IONQ', 'SOUN', 'BBAI', 'ASTR', 'NKLA', 'CANO', 'FFIE', 'JOBY', 'ACHR', 'EVGO', 'QS', 'CVNA', 'UPST', 'BEEM', 'XPEV', 'LI', 'GDRX', 'LMND', 'RUN', 'HOOD', 'NU', 'PATH', 'OPEN', 'RENT', 'ENVX', 'WBD', 'VYGR'],
    'growth': ['TSLA', 'NVDA', 'AMD', 'CELH', 'MELI', 'SHOP', 'TTD', 'ZS', 'DDOG', 'CRWD', 'SNOW', 'NET', 'DOCN', 'FVRR', 'ASAN', 'U', 'BILL', 'GLBE', 'ROKU', 'COIN', 'ESTC', 'ENPH', 'MDB', 'SMCI', 'TWLO', 'S', 'LULU', 'ABNB', 'MOD', 'ON'],
    'blue_chip': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'JNJ', 'V', 'MA', 'WMT', 'KO', 'PEP', 'PG', 'UNH', 'HD', 'CVX', 'XOM', 'MCD', 'NKE', 'JPM', 'DIS', 'LLY', 'AVGO', 'ADBE', 'MRK', 'ABBV', 'BAC', 'TMO', 'TXN', 'LIN', 'DHR'],
    'etfs': ['SPY', 'QQQ', 'VTI', 'VOO', 'ARKK', 'SOXX', 'XLF', 'XLK', 'VGT', 'SMH', 'IWM', 'XLE', 'XLV', 'DIA', 'TAN', 'ICLN', 'XLY', 'XLC', 'VHT', 'VNQ'],
    'value': ['KO', 'PFE', 'CVX', 'XOM', 'IBM', 'WBA', 'MMM', 'T', 'VZ', 'C', 'BAC', 'GM', 'F', 'KHC', 'MO', 'INTC', 'CSCO', 'CVS', 'BMY', 'WFC', 'PGR', 'USB', 'BK', 'MET', 'PRU', 'NTRS', 'ALL', 'AFL', 'SYY', 'O'],
    'penny_stocks': ['HUSA', 'IMPP', 'BRQS', 'COSM', 'GNS', 'CEI', 'INPX', 'BBIG', 'SNDL', 'TRKA', 'IDEX', 'HCDI', 'AITX', 'PROG', 'ABVC', 'VTGN', 'PHUN', 'OPK', 'CLNN', 'NBY'],
}

top_stock_tickers = ['AAPL', 'ABBV', 'ABNB', 'ABVC', 'ACHR', 'ADBE', 'AFL', 'AITX', 'ALL', 'AMD', 'AMZN', 'ARKK', 'ASAN', 'ASTR', 'AVGO', 'BAC', 'BBAI', 'BBIG', 'BEEM', 'BILL', 'BK', 'BMY', 'BRQS', 'C', 'CANO', 'CEI', 'CELH', 'CLNN', 'COIN', 'COSM', 'CRWD', 'CSCO', 'CVNA', 'CVS', 'CVX', 'DDOG', 'DHR', 'DIA', 'DIS', 'DNA', 'DOCN', 'ENPH', 'ENVX', 'ESTC', 'EVGO', 'F', 'FFIE', 'FVRR', 'GDRX', 'GLBE', 'GM', 'GNS', 'GOOGL', 'HCDI', 'HD', 'HOOD', 'HUSA', 'IBM', 'ICLN', 'IDEX', 'IMPP', 'INPX', 'INTC', 'IONQ', 'IWM', 'JNJ', 'JOBY', 'JPM', 'KHC', 'KO', 'LI', 'LIN', 'LLY', 'LMND', 'LULU', 'MA', 'MCD', 'MDB', 'MELI', 'MET', 'META', 'MMM', 'MO', 'MOD', 'MRK', 'MSFT', 'NBY', 'NET', 'NKE', 'NKLA', 'NTRS', 'NU', 'NVDA', 'O', 'ON', 'OPEN', 'OPK', 'PATH', 'PEP', 'PFE', 'PG', 'PGR', 'PHUN', 'PLTR', 'PROG', 'PRU', 'QQQ', 'QS', 'RENT', 'RIVN', 'ROKU', 'RUN', 'S', 'SHOP', 'SMCI', 'SMH', 'SNDL', 'SNOW', 'SOUN', 'SOXX', 'SPY', 'SYY', 'T', 'TAN', 'TMO', 'TRKA', 'TSLA', 'TTD', 'TWLO', 'TXN', 'U', 'UNH', 'UPST', 'USB', 'V', 'VGT', 'VHT', 'VNQ', 'VOO', 'VTGN', 'VTI', 'VYGR', 'VZ', 'WBA', 'WBD', 'WFC', 'WMT', 'XLC', 'XLE', 'XLF', 'XLK', 'XLV', 'XLY', 'XOM', 'XPEV', 'ZS']

# Flatten all tickers into a single list for core engine use
top_stock_tickers = list(set(sum(categorized_tickers.values(), [])))

def get_stock_summary(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")
        if hist.empty or len(hist) < 60:
            return None

        current_price = hist["Close"].iloc[-1]
        prev_day_price = hist["Close"].iloc[-2]
        one_month_price = hist["Close"].iloc[-22]

        day_change = ((current_price - prev_day_price) / prev_day_price) * 100
        month_change = ((current_price - one_month_price) / one_month_price) * 100
        sma_50 = hist["Close"].rolling(window=50).mean().iloc[-1]
        sma_200 = hist["Close"].rolling(window=200).mean().iloc[-1]
        rsi = 100 - (100 / (1 + hist["Close"].pct_change().dropna().rolling(14).mean().iloc[-1]))

        info = stock.info

        return {
            "ticker": ticker,
            "company": info.get("shortName", ""),
            "sector": info.get("sector", ""),
            "summary": info.get("longBusinessSummary", ""),
            "price": round(current_price, 2),
            "change_day": round(day_change, 2),
            "change_month": round(month_change, 2),
            "rsi": round(rsi, 2),
            "sma_50": round(sma_50, 2),
            "sma_200": round(sma_200, 2)
        }
    except Exception as e:
        print(f"❌ Error for {ticker}: {e}")
        return None

def choose_top_candidate():
    import random
    random.shuffle(top_stock_tickers)
    for ticker in top_stock_tickers:
        summary = get_stock_summary(ticker)
        if summary:
            return summary
    return None

def generate_stock_pick_rationale(summary):
    if not summary:
        return {"ticker": None, "rationale": "No valid pick generated today."}

    today = datetime.now().strftime("%B %d, %Y")

    prompt = f"""
You are BullBroker, a financial AI that selects ONE stock to recommend today based on the following real market data.

Today's date: {today}

Stock: {summary['ticker']} ({summary['company']})
Sector: {summary['sector']}
Price: ${summary['price']}
1-Day % Change: {summary['change_day']}%
1-Month % Change: {summary['change_month']}%
RSI: {summary['rsi']}
50-day SMA: {summary['sma_50']}
200-day SMA: {summary['sma_200']}
Business Summary: {summary['summary']}

Rules:
- If RSI > 50, price above 50SMA and 200SMA, and recent gains → "Long Hold"
- If RSI < 45, price below both SMAs and recent losses → "Short Sell"
- Otherwise pick best case scenario for either side, not neutral
- You MUST choose only one: "Long Hold" or "Short Sell"
- Assign a classification: growth, speculative, blue chip, value, defensive, etc.
- Include a realistic target price (up or down)
- Your reply must be valid JSON with no explanation

Format:
{{
  "ticker": "{summary['ticker']}",
  "pick_type": "Long Hold",
  "stock_class": "blue chip",
  "target_price": 250.00,
  "rationale": "This stock is riding upward momentum, trading above both 50 and 200 day SMAs, with RSI at 63. Analysts project continued strength given earnings and tech growth sector tailwinds."
}}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=400,
        )
        content = response.choices[0].message["content"]
        import json
        return json.loads(content)
    except Exception as e:
        return {"ticker": None, "rationale": f"OpenAI Error: {str(e)}"}

def get_best_stock_pick():
    summary = choose_top_candidate()
    return generate_stock_pick_rationale(summary)
