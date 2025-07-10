import streamlit as st
import requests
import yfinance as yf

API_URL = "https://bullbroker.onrender.com/daily-pick"

st.set_page_config(page_title="BullBroker", layout="centered")
st.title("📈 BullBroker: Daily Stock Pick")
st.subheader("Your AI-Powered Investment Strategist")

if st.button("📊 Get Today's Pick"):
    with st.spinner("Contacting the AI strategist..."):
        try:
            response = requests.get(API_URL, timeout=15)
            response.raise_for_status()
            data = response.json()

            ticker = data.get("ticker", "N/A")
            rationale = data.get("rationale", "No rationale available.")

            # Extract Pick Type
            lines = rationale.splitlines()
            pick_type_line = next((l for l in lines if "Pick Type" in l), "")
            pick_type = pick_type_line.split(":")[-1].strip() if ":" in pick_type_line else "Unclear"

            # Display info
            st.markdown(f"### 🏷️ Ticker: `{ticker}`")
            st.markdown(f"**💡 Pick Type:** `{pick_type}`")

            # 💹 Live stock data
            stock = yf.Ticker(ticker)
            todays_data = stock.history(period="1d")
            current_price = todays_data["Close"].iloc[-1]
            previous_close = stock.info.get("previousClose", current_price)
            change = current_price - previous_close
            percent_change = (change / previous_close) * 100

            st.markdown(f"### 💵 Live Price: ${current_price:.2f}")
            st.markdown(f"**📉 Change:** {change:+.2f} ({percent_change:+.2f}%)")

            st.markdown("### 🧠 AI Rationale")
            st.write(rationale)

        except Exception as e:
            st.error(f"Failed to fetch data: {e}")
else:
    st.info("Click the button above to get today’s pick.")
