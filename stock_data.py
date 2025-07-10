import yfinance as yf

def fetch_stock_summary(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")
    info = stock.info

    summary = {
        "name": info.get("shortName"),
        "sector": info.get("sector"),
        "marketCap": info.get("marketCap"),
        "volume": info.get("volume"),
        "previousClose": info.get("previousClose"),
        "50DayAverage": info.get("fiftyDayAverage"),
        "200DayAverage": info.get("twoHundredDayAverage"),
        "1moHistory": hist.tail(5).to_dict()
    }

    return summary