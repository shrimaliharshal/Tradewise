import pandas as pd
import numpy as np
import plotly.graph_objs as go
import streamlit as st
import json
from confluent_kafka import Consumer, KafkaError

def consume_prices():
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'mygroup',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(**conf)
    consumer.subscribe(['stock-trades'])
    data = pd.DataFrame(columns=['Date', 'Close'])
    
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # Handle end of partition
                    continue
                else:
                    print(msg.error())
                    break
            stock_data = json.loads(msg.value().decode('utf-8'))
            new_row = {'Date': pd.to_datetime(stock_data['date']), 'Close': stock_data['closing_price']}
            data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
            if len(data) >= 10:  # Check if we have at least 30 data points
                yield data
    finally:
        consumer.close()


# Simulate data fetching
def fetch_data():
    # Simulate daily closing prices
    np.random.seed(0)
    prices = np.random.normal(100, 0.5, 60).cumsum()  # 60 days worth of data
    dates = pd.date_range(start='1/1/2020', periods=60)
    df = pd.DataFrame(data={'Date': dates, 'Close': prices})
    return df

# Calculate indicators
def calculate_indicators(df):
    # Calculate Moving Averages, MACD, RSI
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    df['SMA_5'] = df['Close'].rolling(window=5).mean()
    df['SMA_20'] = df['Close'].rolling(window=20).mean()

    return df
def plot_data(df):
    # Separate figures for each indicator
    fig_close_price = go.Figure()
    fig_close_price.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close Price'))
    fig_close_price.update_layout(title='Close Price', xaxis_title='Date', yaxis_title='Value')

    fig_sma = go.Figure()
    fig_sma.add_trace(go.Scatter(x=df['Date'], y=df['SMA_5'], mode='lines', name='5-day SMA'))
    fig_sma.add_trace(go.Scatter(x=df['Date'], y=df['SMA_20'], mode='lines', name='20-day SMA'))
    fig_sma.update_layout(title='Simple Moving Averages', xaxis_title='Date', yaxis_title='Value')

    fig_macd = go.Figure()
    fig_macd.add_trace(go.Scatter(x=df['Date'], y=df['MACD'], mode='lines', name='MACD'))
    fig_macd.add_trace(go.Scatter(x=df['Date'], y=df['Signal'], mode='lines', name='Signal Line'))
    fig_macd.update_layout(title='MACD', xaxis_title='Date', yaxis_title='Value')

    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], mode='lines', name='RSI'))
    fig_rsi.update_layout(title='RSI', xaxis_title='Date', yaxis_title='Value')

    return fig_close_price, fig_sma, fig_macd, fig_rsi

def main():
    st.title('Real-Time Stock Indicator Visualization')
    
    # Placeholders for each chart
    placeholder_close_price = st.empty()
    placeholder_sma = st.empty()
    placeholder_macd = st.empty()
    placeholder_rsi = st.empty()

    for data in consume_prices():
        df = calculate_indicators(data)  # Calculate indicators
        fig_close_price, fig_sma, fig_macd, fig_rsi = plot_data(df)  # Plot the data

        # Update the placeholders with new figures
        placeholder_close_price.plotly_chart(fig_close_price, use_container_width=True)
        placeholder_sma.plotly_chart(fig_sma, use_container_width=True)
        placeholder_macd.plotly_chart(fig_macd, use_container_width=True)
        placeholder_rsi.plotly_chart(fig_rsi, use_container_width=True)

if __name__ == "__main__":
    main()
