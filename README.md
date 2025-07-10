# BullBroker

An AI-powered backend that recommends one high-conviction stock pick each day — for day trading, options, or long-term investment.

## 🚀 Features
- Pulls real-time stock data (Yahoo Finance)
- Uses OpenAI GPT-4 to analyze and select the best stock daily
- Returns:
  - Stock ticker
  - Type of investment
  - AI-generated rationale

## 🧠 Requirements

- Python 3.8+
- OpenAI API key

## 🔧 Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/BullBroker.git
   cd BullBroker
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file:
   ```bash
   cp .env.example .env
   # Then paste your OpenAI API key in .env
   ```

5. Run the app:
   ```bash
   uvicorn main:app --reload
   ```

6. Visit in browser:
   [http://localhost:8000/daily-pick](http://localhost:8000/daily-pick)

## 🔒 Notes
- Do NOT commit your `.env` file — it contains your secret API key.

## 📦 Coming Soon
- Frontend UI with Streamlit or iOS integration
- Smarter ticker selection
- Charting + risk level
