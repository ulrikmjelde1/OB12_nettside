import requests
import json
from datetime import datetime
#import pandas as pd

#-- Alpha Vantage API config.
API_KEY = 'DZQX84XELWXBXQLI'
BASE_URL = 'https://www.alphavantage.co/query'

CURRENCY_PAIRS = [
    ('USD', 'NOK'),
    ('GBP', 'USD'),
    ('GBP', 'NOK'),
    ('DKK', 'NOK'),
    ('SEK', 'NOK'),
    ('EUR', 'NOK')
]

def fetch_fx_data():
    fx_data = {}  # Initialize fx_data here to ensure it's available throughout the function
    for base, target in CURRENCY_PAIRS:
        params = {
            'function': 'CURRENCY_EXCHANGE_RATE',
            'from_currency': base,
            'to_currency': target,
            'apikey': API_KEY
        }
        
        response = requests.get(BASE_URL, params=params)
        
        # Check if the API request was successful
        if response.status_code == 200:
            data = response.json()
            
            try:
                fx_rate = data['Realtime Currency Exchange Rate']
                rate_info = {
                    'from_currency': fx_rate['1. From_Currency Code'],
                    'to_currency': fx_rate['3. To_Currency Code'],
                    'exchange_rate': fx_rate['5. Exchange Rate'],
                    'last_refreshed': fx_rate['6. Last Refreshed'],
                    'time_zone': fx_rate['7. Time Zone']
                }
                fx_data[f'{base}_{target}'] = rate_info
            except KeyError:
                print(f"Error fetching data for {base}/{target}: Missing keys in response.")
        else:
            print(f"Error fetching data for {base}/{target}: API request failed with status code {response.status_code}")

    # Save the data to a JSON file
    with open('fx_data.json', 'w') as file:
        json.dump(fx_data, file, indent=4)
    
    print("FX data has been updated.")

if __name__ == "__main__":
    fetch_fx_data()
