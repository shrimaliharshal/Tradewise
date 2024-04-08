# from kafka import Consumer, KafkaError
import csv
import os
from datetime import datetime
import json
import requests
from confluent_kafka import Producer

# ticker_symbol = 'BTC-USD'
# headers = {
#  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
#  'Content-Type': 'application/json',
#  'Authorization': 'Bearer <token>'
# }



# def fetch_and_send_stock_price():
#  while True:
#    try:
#      url = 'https://query2.finance.yahoo.com/v8/finance/chart/btc-usd'
#      response = requests.get(url, headers=headers)
#      data = json.loads(response.text)
#      price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
#      print(f"Sent {ticker_symbol} price to Kafka: {price}")
#      return data 
#    except Exception as e:
#     print(f"Error fetching/sending stock price: {e}")

# data = fetch_and_send_stock_price()
# print(data)



import yfinance as yf
# from kafka import KafkaProducer
import json
import time

# # Initialize Kafka producer to connect to the Kafka service within Docker
# producer = Producer(bootstrap_servers=['broker:9092'], # Use the service name and port from docker-compose
#                          value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# def fetch_and_send_stock_price():
#     ticker_symbol = 'AAPL'  # Example with Apple stock, modify as needed
#     while True:
#         try:
#             # Fetch data
#             ticker = yf.Ticker(ticker_symbol)
#             hist = ticker.history(period="1d", interval="1m")
#             # Latest price
#             price = hist['Close'].iloc[-1]
#             # Construct message
#             message = {'symbol': ticker_symbol, 'price': float(price)}
#             # Send to Kafka
#             producer.send('stock-trades', value=message)
#             producer.flush()
#             print(f"Sent {ticker_symbol} price to Kafka: {price}")
#             time.sleep(60)  # Fetch every 60 seconds
#         except Exception as e:
#             print(f"Error fetching/sending stock price: {e}")

# fetch_and_send_stock_price()




# Corrected Kafka producer configuration
conf = {
    'bootstrap.servers': "localhost:9092",  # Use the service name and port from docker-compose
}

producer = Producer(**conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def fetch_and_send_stock_price():
    ticker_symbol = 'AAPL'  # Example ticker symbol
    while True:
        try:
            # Dummy price data for illustration; replace with actual fetching logic
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period="1d", interval="1m")  # Fetch data at a 1-minute interval for the last day
            if not hist.empty:
                latest_price = hist['Close'].iloc[-1]  # Get the latest closing price
                
                # Construct the message with the real price
                message = {'symbol': ticker_symbol, 'price': float(latest_price)}
            
            # Send the message to Kafka
            producer.produce('stock-trades', key=str(ticker_symbol), value=json.dumps(message), callback=delivery_report)
            producer.poll(0)  # Serve delivery callback queue
            
            print(f"Sent {ticker_symbol} price to Kafka: {latest_price}")
            time.sleep(60)  # Fetch every 60 seconds
        except Exception as e:
            print(f"Error fetching/sending stock price: {e}")

fetch_and_send_stock_price()