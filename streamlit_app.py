import streamlit as st
import requests

# CONFIG
API_URL = "https://yourrenderurl.com/daily-pick"  # <- Replace with your real Render URL

st.set_page_config(page_title="BullBroker", layout="centered")

st.title("📈 BullBroker: Daily Stock Pick")
st.subheader("Your AI-Powered Investment Strategist")

with st.spinner("Fetching today's stock pick..."):
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        ticker = data.get("ticker", "N/A")
        rationale = data.get("rationale", "No rationale available.")

        # Try to parse pick type from AI response
        lines = rationale.splitlines()
        pick_type_line = next((l for l in lines if "Pick Type" in l), "")
        pick_type = pick_type_line.split(":")[-1].strip() if ":" in pick_type_line else "Unclear"

        st.markdown(f"### 🏷️ Ticker: `{ticker}`")
        st.markdown(f"**💡 Pick Type:** `{pick_type}`")
        st.markdown("### 🧠 AI Rationale")
        st.write(rationale)

    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
