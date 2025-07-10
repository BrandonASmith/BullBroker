import streamlit as st
import requests
import yfinance as yf
import plotly.graph_objects as go

API_URL = "https://bullbroker.onrender.com/daily-pick"

st.set_page_config(page_title="BullBroker", layout="centered")
st.title("📈 BullBroker: Daily Stock Pick")
st.subheader("Your AI-Powered Investment Strategist")

if st.button("📊 Get Today's Pick"):
    with st.spinner("Analyzing the market..."):
        try:
            # Request backend
            response = requests.get(API_URL, timeout=15)
            response.raise_for_status()
            data = response.json()

            ticker = data.get("ticker")
            rationale = data.get("rationale", "").strip()

            # Validate ticker
            if not ticker or not isinstance(ticker, str):
                st.error("❌ No valid stock ticker returned. Please try again later.")
            else:
                st.markdown(f"### 🏷️ Ticker: `{ticker.upper()}`")

                # Pick Type extraction
                lines = rationale.splitlines()
                pick_type_line = next((l for l in lines if "Pick Type:" in l), "")
                pick_type = pick_type_line.split(":")[-1].strip() if ":" in pick_type_line else "Unclear"
                st.markdown(f"**💡 Pick Type:** `{pick_type}`")

                # Live price
                stock = yf.Ticker(ticker)
                hist = stock.history(period="1d")
                if not hist.empty:
                    current_price = hist["Close"].iloc[-1]
                    previous_close = stock.info.get("previousClose", current_price)
                    change = current_price - previous_close
                    percent_change = (change / previous_close) * 100

                    st.markdown(f"### 💵 Live Price: ${current_price:.2f}")
                    st.markdown(f"📉 Change: {change:+.2f} ({percent_change:+.2f}%)")
                else:
                    st.warning("Could not fetch live price data.")

                # Chart
                chart_data = stock.history(period="1mo")
                if not chart_data.empty:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=chart_data.index,
                        y=chart_data["Close"],
                        mode="lines",
                        name="Close Price"
                    ))
                    fig.update_layout(
                        title=f"{ticker.upper()} 1-Month Performance",
                        xaxis_title="Date",
                        yaxis_title="Price (USD)",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)

                # Rationale
                st.markdown("### 🧠 AI Rationale")
                if rationale and rationale != "No rationale received":
                    st.write(rationale)
                else:
                    st.warning("No AI explanation was returned.")

        except Exception as e:
            st.error(f"Failed to fetch data: {e}")
else:
    st.info("Click the button above to generate today's AI-powered stock pick.")
