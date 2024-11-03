import requests
import redis
import json
import time
import logging
from dotenv import load_dotenv
import os

# Retrieve apikey from .env
load_dotenv()
APIKEY = os.getenv("APIKEY")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Redis connection
redis_db = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Marketstack API details
API_KEY = APIKEY 
API_URL = 'http://api.marketstack.com/v1/intraday'
STOCK_SYMBOLS = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'NVDA']
POLL_INTERVAL = 20

# Catches data from MarketStack API
def fetch_stock_data():
    all_data = []
    for stock in STOCK_SYMBOLS:
        params = {'access_key': API_KEY, 'symbols': stock}
        response = requests.get(API_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and data['data']:
                all_data.append(data['data'][0])
        else:
            logging.error(f"Failed to retrieve data for {stock}. Status code: {response.status_code}")
    
    return all_data

# Redis Operations
  ## Store data in Redis
def redis_set(key, value):
    redis_db.set(key, json.dumps(value))
    logging.info(f"Stored data for '{key}' in Redis.")

  ## Retrieve data stored in Redis
def redis_get(key):
    value = redis_db.get(key)
    return json.loads(value) if value else None

  ##Updates stored data in Redis
def redis_update(key, value):
    redis_set(key, value) 
    logging.info(f"Updated data for '{key}' in Redis.")

# API polling and implements Redis SET/GET/UPDATE as needed
def poll_and_store_stock_data():
    while True:
        stock_data_list = fetch_stock_data()
        
        for data in stock_data_list:
            if isinstance(data, dict) and 'symbol' in data:
                stock_symbol = data['symbol']
                stock_data = {
                    "date": data.get('date'),
                    "open": data.get('open'),
                    "last": data.get('last'),
                    "high": data.get('high')
                }
                # Checks if data exists in Redis already. 
                existing_data = redis_get(stock_symbol)
                print(existing_data)
                if existing_data:
                    if existing_data == stock_data:
                        logging.info(f"No update needed for '{stock_symbol}'")
                        continue
                    else:
                      redis_update(stock_symbol, stock_data)
                else:
                    # If data is not stored it will create a new entry
                    redis_set(stock_symbol, stock_data)

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    poll_and_store_stock_data()