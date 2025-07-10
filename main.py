
import streamlit as st
import requests

st.set_page_config(page_title="BullBroker", layout="centered")

st.markdown("### 📈 **BullBroker: Daily Stock Pick**")
st.markdown("#### Your AI-Powered Investment Strategist")

if st.button("📊 Get Today's Pick"):
    try:
        response = requests.get("https://bullbroker.onrender.com/daily-pick", timeout=15)
        data = response.json()

        if data.get("ticker"):
            st.success(f"**Ticker:** {data['ticker']}")
            st.info(f"**Pick Type:** {data.get('pick_type', 'Unclear')}")
            st.info(f"**Stock Category:** {data.get('stock_type', 'Unknown')}")
            st.write("📌 **Rationale:**")
            st.write(data["rationale"])
        else:
            st.error("❌ No valid stock ticker returned. Please try again later.")
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")

        st.error(f"❌ Failed to fetch data: {e}")
