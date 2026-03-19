import alpaca_trade_api as tradeapi
import time

# 1. Setup credentials
API_KEY = 'YOUR_API_KEY'
SECRET_KEY = 'YOUR_SECRET_KEY'
BASE_URL = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

# 2. Step One: Buy 1 share at Market Price
print("Submitting market buy order for 1 share of SPY...")
buy_order = api.submit_order(
    symbol='SPY',
    qty=1,
    side='buy',
    type='market',
    time_in_force='gtc'
)

# 3. Wait a moment for the order to fill so we can get the price
time.sleep(2) 
filled_order = api.get_order(buy_order.id)

if filled_order.status == 'filled':
    # Get the price we actually paid
    entry_price = float(filled_order.filled_avg_price)
    take_profit_price = entry_price + 1.00
    
    print(f"Bought at ${entry_price}. Setting limit sell at ${take_profit_price}")

    # 4. Step Two: Place the Limit Order $1.00 higher
    api.submit_order(
        symbol='SPY',
        qty=1,
        side='sell',
        type='limit',
        limit_price=take_profit_price,
        time_in_force='gtc'
    )
    print("Limit order placed!")
else:
    print(f"Order status is {filled_order.status}. Limit order not placed.")
