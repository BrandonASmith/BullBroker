import os
import openai
import random

# Get API key safely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("❌ OPENAI_API_KEY is not set.")

openai.api_key = OPENAI_API_KEY

# Sample high-quality tickers — you can extend or fetch dynamically
TRACKER_LIST = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "AVGO", "BRK.B", "LLY",
    "UNH", "V", "JPM", "XOM", "JNJ", "WMT", "MA", "PG", "HD", "COST", "MRK", "CVX", "ABBV", "PEP", "ADBE",
    "CRM", "BAC", "NFLX", "KO", "TMO", "AMD", "DIS", "ABT", "PFE", "MCD", "NKE", "LIN", "INTC", "ORCL",
    "WFC", "ACN", "DHR", "MS", "TXN", "AMAT", "NEE", "QCOM", "PM", "GE", "BMY", "UPS", "CAT", "IBM", "RTX",
    "SPGI", "GS", "BLK", "ISRG", "MDT", "SYK", "HON", "ELV", "CI", "NOW", "REGN", "MU", "VRTX", "PLD",
    "LMT", "ADI", "ADP", "T", "DE", "ZTS", "MMC", "SCHW", "CB", "ETN", "EQIX", "F", "MO", "USB", "CSCO",
    "AXP", "BDX", "C", "DUK", "NSC", "SO", "FDX", "APD", "EOG", "GM", "CL", "ADSK", "ROST", "TJX", "SBUX",
    "SLB", "GILD", "D", "EMR", "PSA", "MCO", "NOC", "VLO", "TRV", "TT", "AON", "PCAR", "LRCX", "HCA", "AEP",
    "PH", "IDXX", "EXC", "KMB", "HUM", "ROK", "MTD", "KMI", "DVN", "PAYX", "FTNT", "WELL", "ED", "AIG", "AME",
    "IQV", "MAR", "SPG", "DAL", "CTAS", "KLAC", "LHX", "FIS", "DLR", "AFL", "VTR", "HES", "AZO", "HAL", "O",
    "FAST", "PWR", "PEG", "ADM", "YUM", "ODFL", "RMD", "MKC", "CEG", "HPQ", "STZ", "ALGN", "RCL", "TSCO",
    "EQR", "CHD", "AWK", "WBA", "EIX", "BALL", "DRI", "NUE", "NDAQ", "KEYS", "CTSH", "SRE", "MTCH", "EXPE",
    "ULTA", "MNST", "COF", "ATO", "VRSK", "AVB", "FE", "XYL", "TER", "CF", "TYL", "INVH", "IFF", "SBAC",
    "HSY", "LUV", "ZBRA", "MPWR", "POOL", "CDNS", "FSLR", "ENPH", "RUN", "NEE", "SEDG", "CSIQ", "BLNK", "CHPT",
    "PLTR", "SNOW", "U", "DDOG", "ZS", "OKTA", "NET", "PATH", "AI", "BILL", "TWLO", "AFRM", "DOCN", "UPST",
    "SOFI", "RIVN", "LCID", "NKLA", "HOOD", "CROX", "SHOP", "SQ", "PYPL", "BABA", "JD", "PDD", "LI", "NIO",
    "TSM", "ASML", "INTU", "WM", "TGT", "KR", "LOW", "BBY", "VFC", "DELL", "HP", "Z", "EBAY", "YELP", "GRMN",
    "CZR", "MGM", "WYNN", "TTWO", "EA", "ATVI", "ROKU", "DKNG", "PENN", "LYV", "BIDU", "ARCC", "MAIN", "BX",
    "KHC", "GIS", "HSBC", "ING", "BP", "TOT", "RY", "TD", "ENB", "BNS", "BMO", "NSRGY", "SNY", "GSK", "UL",
    "BTI", "NGG", "RELX", "WBK", "TEF", "VOD", "RIO", "VALE", "GOLD", "FCX", "NEM", "MOS", "SMG", "ADM",
    "BG", "CTVA", "NTR", "CF", "CARG", "APP", "WING", "TTD", "NVCR", "ON", "SWKS", "QRVO", "HUBS", "FICO",
    "TEAM", "MNDY", "TXG", "BRZE", "SPLK", "ESTC", "MDB", "GLBE", "FIVN", "GTLB", "ZS", "ROKU", "FIGS",
    "RVLV", "LEVI", "DKS", "CHWY", "PTON", "NU", "MELI", "WBD", "PARA", "DISCA", "MTN", "LTH", "XPO", "FWRD",
    "R", "TTC", "IR", "WMS", "PNR", "AWI", "MAS", "LEG", "WHR", "LII", "AOS", "OC", "BWA", "ALSN"
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
