# main.py (Streamlit frontend)

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objs as go

st.set_page_config(page_title="BullBroker: Daily Stock Pick", layout="centered")
st.title("📈 BullBroker: Daily Stock Pick")
st.subheader("Your AI-Powered Investment Strategist")

if st.button("📊 Get Today's Pick"):
    try:
        response = requests.get("https://bullbroker.onrender.com/daily-pick", timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data["ticker"]:
                st.success(f"🏷️ Ticker: {data['ticker']}")
                st.markdown(f"💡 **Pick Type**: {data.get('pick_type', 'Unclear')}")
                st.markdown(f"📊 **Stock Type**: {data.get('stock_type', 'Unclear')}")
                st.markdown(f"🎯 **Target Price**: {data.get('target_price', 'N/A')}")

                # Show rationale
                st.markdown("### 🧠 AI Rationale")
                st.write(data.get("rationale", "No rationale received"))

                # Live price chart
                ticker = data['ticker']
                price_response = requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1mo&interval=1d")
                price_data = price_response.json()

                try:
                    timestamps = price_data['chart']['result'][0]['timestamp']
                    closes = price_data['chart']['result'][0]['indicators']['quote'][0]['close']
                    df = pd.DataFrame({"Date": pd.to_datetime(timestamps, unit='s'), "Close": closes})
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], mode="lines", name=ticker))
                    fig.update_layout(title=f"{ticker} 1-Month Price Chart", xaxis_title="Date", yaxis_title="Close Price")
                    st.plotly_chart(fig)
                except Exception as e:
                    st.warning("Chart data not available.")
            else:
                st.error("❌ No valid stock ticker returned. Please try again later.")
        else:
            st.error(f"❌ Failed to fetch data: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Failed to fetch data: {e}")
