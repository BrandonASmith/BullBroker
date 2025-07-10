import os
import random
import openai
from datetime import datetime

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    raise RuntimeError("❌ OPENAI_API_KEY is not set.")

# Tracker list: 500 strong stocks
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
    "HSY", "LUV", "ZBRA", "MPWR", "POOL", "CDNS", "FIVN", "FSLR", "ENPH", "RUN", "NEE", "SEDG", "CSIQ", "BLNK",
    "CHPT", "PLTR", "SNOW", "U", "DDOG", "ZS", "OKTA", "NET", "PATH", "AI", "BILL", "TWLO", "AFRM", "DOCN",
    "UPST", "SOFI", "RIVN", "LCID", "NKLA", "HOOD", "CROX", "SHOP", "SQ", "PYPL", "BABA", "JD", "PDD", "LI",
    "NIO", "TSM", "ASML", "INTU", "WM", "TGT", "KR", "LOW", "BBY", "VFC", "DELL", "HP", "Z", "EBAY", "YELP",
    "GRMN", "CZR", "MGM", "WYNN", "TTWO", "EA", "ATVI", "ROKU", "DKNG", "PENN", "LYV", "BIDU", "ARCC", "MAIN",
    "BX", "KHC", "GIS", "HSBC", "ING", "BP", "TOT", "RY", "TD", "ENB", "BNS", "BMO", "NSRGY", "SNY", "GSK",
    "UL", "BTI", "NGG", "RELX", "WBK", "TEF", "VOD", "RIO", "VALE", "GOLD", "FCX", "NEM", "MOS", "SMG", "ADM",
    "BG", "CTVA", "NTR", "CF", "CARG", "APP", "WING", "TTD", "NVCR", "ON", "SWKS", "QRVO", "HUBS", "FICO",
    "TEAM", "MNDY", "TXG", "BRZE", "SPLK", "ESTC", "MDB", "GLBE", "GTLB", "FIGS", "RVLV", "LEVI", "DKS",
    "CHWY", "PTON", "NU", "MELI", "WBD", "PARA", "DISCA", "MTN", "LTH", "XPO", "FWRD", "R", "TTC", "IR", "WMS",
    "PNR", "AWI", "MAS", "LEG", "WHR", "LII", "AOS", "OC", "BWA", "ALSN"
]

# Utility function: classify pick type
def classify_pick_type():
    options = ["Long-Term", "Day Trade", "Options Play"]
    return random.choice(options)

# Generate the AI rationale
def generate_stock_pick_rationale(ticker):
    today = datetime.now().strftime("%B %d, %Y")

    prompt = (
        f"As of {today}, explain why {ticker} is the best stock pick today for a retail investor. "
        "Factor in market trends, sector performance, recent news, and technical indicators. "
        "Explain it like an expert financial strategist writing to a curious but non-professional trader. "
        "Make it persuasive and insightful in under 150 words."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7,
        )
        output = response.choices[0].message.content.strip()
        return output
    except Exception as e:
        print("❌ GPT API Error:", e)
        return "No rationale received"

# Main handler to use in FastAPI or Streamlit
def get_daily_pick():
    try:
        ticker = random.choice(TRACKER_LIST)
        pick_type = classify_pick_type()
        rationale = generate_stock_pick_rationale(ticker)
        return {
            "ticker": ticker,
            "pick_type": pick_type,
            "rationale": rationale
        }
    except Exception as e:
        print("❌ Error getting pick:", e)
        return {
            "ticker": None,
            "pick_type": "Unclear",
            "rationale": "No valid pick generated today."
        }
