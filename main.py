# ai_engine.py

import yfinance as yf
import openai
import os
import streamlit as st
import json
from ai_engine import get_best_stock_today

st.set_page_config(page_title="BullBroker: Daily Stock Pick", layout="centered")

st.title("📈 BullBroker: Daily Stock Pick")
st.subheader("Your AI-Powered Investment Strategist")

if st.button("📊 Get Today's Pick"):
    with st.spinner("Analyzing the market..."):
        pick = get_best_stock_today()

    if pick["ticker"]:
        st.success(f"**Ticker:** {pick['ticker']}")
        st.markdown(f"**Type:** {pick['stock_type'].capitalize()}  \n**Strategy:** {pick['pick_type']}")
        st.markdown("---")
        st.markdown(f"**Rationale:**\n\n{pick['rationale']}")
    else:
        st.error("❌ No valid pick generated today.")
