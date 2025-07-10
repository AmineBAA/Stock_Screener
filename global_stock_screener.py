import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 Stock Comparison Dashboard (Finviz-style)")

# Input
tickers = st.text_input("Enter stock tickers (comma-separated)", "AAPL, MSFT, AMZN").upper().split(',')

@st.cache_data
def get_stock_info(ticker):
    try:
        stock = yf.Ticker(ticker.strip())
        info = stock.info
        hist = stock.history(period="6mo")
        return {
            "Name": info.get("shortName"),
            "Sector": info.get("sector"),
            "Market Cap": info.get("marketCap"),
            "P/E": info.get("trailingPE"),
            "EPS": info.get("trailingEps"),
            "Dividend Yield": info.get("dividendYield"),
            "52W High": info.get("fiftyTwoWeekHigh"),
            "52W Low": info.get("fiftyTwoWeekLow"),
            "Chart": hist["Close"] if not hist.empty else None
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
