import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("Sotcks Price Forecasting App")

# Function to obtain the stocks historical data
def get_historical_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)
    data.index = data.index.date
    # The dataset has some keys, the code below drops those keys and also selects the Ajusted Close Price
    return data['Adj Close'].rename_axis(None, axis=1)


# List to save the stocks tickers
if "tickers_list" not in st.session_state:
    st.session_state.tickers_list = []

with st.sidebar:
    st.title("Stocks Selection")

    # Input para adicionar tickers
    explanation = """
    <p><b>Instructions for Stock Ticker Input:</b></p>
    <ul>
    <li>For US-listed stocks, simply enter the ticker symbol (e.g., AAPL, GOOG)</li>
    <li>For stocks listed on non-US exchanges, include the country code after a dot (e.g., ITUB4.SA for Brazil, X.TO for Canada, etc.)</li>
    </ul>
    """

    st.write(explanation, unsafe_allow_html=True)
    new_ticker = st.text_input("Type the Stock Ticker:")
    # Explanation using Markdown syntax

    if st.button("Add Stock"):
        if new_ticker not in st.session_state.tickers_list:
            st.session_state.tickers_list.append(new_ticker)      



    # Multiselect com os tickers
    portifolio = st.multiselect("Portifolio: ", st.session_state.tickers_list)
    
    # Button to clear the wallet and selected tickers
    if st.button("Clear Portfolio"):
        st.session_state.tickers_list = []  # Clear the tickers list
        portifolio = []  # Clear the selected tickers

    

    # Date selection
    st.title("Interval:")
    start_date = st.date_input("Start Date", format="YYYY/MM/DD")
    end_date = st.date_input("End Date", format="YYYY/MM/DD")

#  Main boddy
if st.button("Generate Portifolio"):
    if st.session_state.tickers_list:
    # Obter os dados históricos
        df = get_historical_data(st.session_state.tickers_list, start_date, end_date)
        if df is not None:
            # st.line_chart(df)
            st.table(df)
            fig = go.Figure()

            # Iterate over tickers in the session state
            for ticker in st.session_state.tickers_list:
                if ticker in df.columns:
                    fig.add_trace(go.Scatter(
                        x=df.index, 
                        y=df[ticker],  # Use ticker column for y values
                        name=ticker
                    ))

            fig.update_layout(
                title='Historical Prices',
                xaxis_title='Date',
                yaxis_title='Price'
            )

            st.plotly_chart(fig, use_container_width=True)
                                           
            st.line_chart(df, y=df.columns)
        else:
            st.error("Enter at least one ticker!")

      
        