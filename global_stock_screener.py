import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide", page_title="Stock Comparison", initial_sidebar_state="expanded")

# Apply dark mode
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: #fafafa;
    }
    .st-bf {
        background-color: #0e1117;
    }
    .st-c6 {
        background-color: #0e1117;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Stock Comparison Dashboard (Finviz-style)")

# Example ticker list to choose from
available_tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "TSLA", "META", "NVDA", "JNJ", "V", "JPM"]

# Multi-select instead of text input
tickers = st.multiselect("Select stock tickers to compare", options=available_tickers, default=["AAPL", "MSFT", "AMZN"])

@st.cache_data
def get_stock_info(ticker):
    try:
        stock = yf.Ticker(ticker.strip())
        info = stock.info
        hist = stock.history(period="2d")  # last 2 days for % change
        if not hist.empty and len(hist) >= 2:
            change = ((hist['Close'][-1] - hist['Close'][-2]) / hist['Close'][-2]) * 100
        else:
            change = None
        return {
            "Name": info.get("shortName"),
            "Sector": info.get("sector"),
            "Market Cap": info.get("marketCap"),
            "P/E": info.get("trailingPE"),
            "EPS": info.get("trailingEps"),
            "Dividend Yield": info.get("dividendYield"),
            "52W High": info.get("fiftyTwoWeekHigh"),
            "52W Low": info.get("fiftyTwoWeekLow"),
            "% Change (1D)": round(change, 2) if change is not None else None,
            "Volume": info.get("volume"),
            "Chart": stock.history(period="6mo")["Close"]
        }
    except Exception as e:
        return {"Error": str(e)}

# Fetch data
data = {ticker: get_stock_info(ticker) for ticker in tickers}

# Display table
st.subheader("🧮 Fundamental Metrics Comparison")
df = pd.DataFrame(data).T.drop(columns=["Chart"])
st.dataframe(df)

# Display charts
st.subheader("📈 Price Charts")
cols = st.columns(len(tickers))
for i, ticker in enumerate(tickers):
    chart = data[ticker].get("Chart")
    if chart is not None:
        with cols[i]:
            st.write(f"**{ticker.strip()}**")
            st.line_chart(chart)
    else:
        st.warning(f"No chart data for {ticker.strip()}")

# PayPal donation
st.markdown("""
---
### ❤️ Support This App
If this helped you compare stocks, consider [donating via PayPal](https://www.paypal.com/donate?hosted_button_id=YOUR_ID).
""")
