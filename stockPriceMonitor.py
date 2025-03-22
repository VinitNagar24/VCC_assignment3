import requests
from flask import Flask, render_template
import time

# Initialize the Flask application
app = Flask(__name__, template_folder='templates')

# Your API Key from MarketStack
API_KEY = 'b5b9c6601c328067d62246879e8ba29c'

# Function to fetch real-time prices for stocks (e.g., Apple and Google)
def fetch_prices():
    url = f"http://api.marketstack.com/v1/eod"
    
    params = {
        'access_key': API_KEY,
        'symbols': 'AAPL,GOOGL',  # Test with valid stock symbols (Apple, Google)
        'limit': 1  # Fetch the most recent data
    }
    
    try:
        # Get the response from MarketStack API
        response = requests.get(url, params=params).json()

        if 'data' in response and len(response['data']) > 0:
            # Extract the most recent data from the API response
            data = response['data'][0]

            # Extract values for Apple and Google
            apple_price = data['close']  # Close price for Apple (AAPL)
            google_price = data['close']  # Close price for Google (GOOGL)

            return apple_price, google_price
        else:
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching prices: {e}")
        return None, None

# Route for the main page
@app.route('/')
def index():
    apple_price, google_price = fetch_prices()
    
    if apple_price and google_price:
        return render_template('index.html', apple_price=apple_price, google_price=google_price)
    else:
        return "Failed to fetch stock prices", 500

if __name__ == "__main__":
    app.run(debug=True)

