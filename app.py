import streamlit as st
from firebaseSetup import initialize_auth, sign_up, login, logout, check_email
from indicators_test import consume_prices, calculate_indicators, plot_data
from prediction import predict_stock_prices
from streaming_kafka import fetch_and_send_stock_price, fetch_and_stream_historical_prices

def main():
    st.sidebar.title("Login/Sign-Up")
    # Initialize Firebase Auth
    auth = initialize_auth()

    # Session state to track user session
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if st.session_state['authenticated']:
        # After successful login
        choice = st.sidebar.radio("Go to", ["Home", "Stock Indicators", "Stock Predictions", "Logout"])

        if choice == "Home":
            st.subheader("Home Page")
            st.write("Welcome to the Stock Analysis Dashboard!")

        elif choice == "Stock Indicators":
            # Call Kafka consume function and display results
            st.subheader("Real-Time Stock Indicator Visualization")
            if st.button("Start Streaming"):
                for data in consume_prices():
                    df = calculate_indicators(data)
                    fig_close_price, fig_sma, fig_macd, fig_rsi = plot_data(df)
                    st.plotly_chart(fig_close_price)
                    st.plotly_chart(fig_sma)
                    st.plotly_chart(fig_macd)
                    st.plotly_chart(fig_rsi)

        elif choice == "Stock Predictions":
            # Display prediction results
            st.subheader("Stock Predictions")
            ticker = st.text_input("Enter Stock Ticker", "AAPL")
            if st.button("Predict"):
                predictions, training_data = predict_stock_prices(ticker)
                st.write(predictions)

        elif choice == "Logout":
            logout()
            st.session_state['authenticated'] = False
            st.experimental_rerun()

    else:
        # Login and Sign-Up
        form_type = st.sidebar.selectbox("Login/Sign-Up", ["Login", "Sign-Up"])
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        if form_type == "Login":
            if st.sidebar.button("Login"):
                st.session_state['authenticated'] = login(username, password)

        elif form_type == "Sign-Up":
            if st.sidebar.button("Sign Up"):
                sign_up(username, password)
                st.sidebar.write("Please login now.")

if __name__ == "__main__":
    main()
