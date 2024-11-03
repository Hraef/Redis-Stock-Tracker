# Stock Data Monitoring System

A Python-based application for gathering and storing stock data using Redis. This project retrieves real-time intraday stock data from the Marketstack API and stores it in Redis, enabling easy access and data persistence.

## Overview

This project:
- Polls stock data for specific symbols (e.g., AAPL, MSFT).
- Stores retrieved data in Redis
- Uses logging for monitoring requests and updates.

## Technologies Used

- **Python**: Core language for implementing data polling and processing.
- **Redis**: Database for storing and retrieving stock data.
- **Marketstack API**: Source for real-time stock market data.

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/stock-data-monitor.git
   cd stock-data-monitor


2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Configure API Key**:
   - Create a `.env` file in the root directory.
   - Add your Marketstack API key:
     ```plaintext
     APIKEY=your_marketstack_api_key
     ```

4. **Start Redis**:
   - Ensure Redis is running locally. I used docker to run redis in this project
     ```bash
     docker run --name redis -d -p 6379:6379 redis
     ```
    - to verify the container is up and running run
    ```bash
    docker ps
    ```

## Running the Project

Run the script to start polling and storing stock data:
```bash
python main.py
```

## Code Structure

- **fetch_stock_data()**: Retrieves stock data from the Marketstack API.
- **redis_set()**, **redis_get()**, **redis_update()**: Functions for storing, retrieving, and updating data in Redis.
- **poll_and_store_stock_data()**: Main loop for polling the API, checking Redis, and updating data as needed.
