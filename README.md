#Overview#
This system integrates real-time stock price data fetching, streaming, prediction, and visualization into a seamless workflow using Python, Kafka, Docker, and Streamlit. The project is structured around four main Python scripts and a Docker setup to ensure ease of deployment and scalability.

#System Architecture#
Data Fetching: streaming_kafka.py fetches real-time stock data using external APIs and sends it to Kafka for streaming.
Data Streaming: Kafka acts as a central hub for data streaming, ensuring that data flows efficiently between components.
Data Prediction: prediction.py subscribes to the Kafka topic to fetch data and applies predictive models to forecast stock prices.
Interactive Dashboards: dashboard.py utilizes Streamlit to create web interfaces that display real-time insights and predictions.
Data Visualization: indicator_test.py accesses both real-time and predicted data to generate graphical representations.
Each component is encapsulated in Docker containers, orchestrated with Docker Compose to streamline deployment and scaling.

#Installation#
Prerequisites
Python 3.8+
Docker and Docker Compose
Apache Kafka

#Troubleshooting#
Kafka Connection Issues: Ensure Kafka and Zookeeper services are running and accessible.
Data Fetching Errors: Check API limits and connectivity.
Streamlit Interface Not Loading: Verify that Streamlit is properly installed in the Docker container and ports are mapped correctly.
