import alpaca_trade_api as tradeapi

# 1. Setup credentials (using Paper Trading keys)
API_KEY = 'YOUR_API_KEY'                            # get afer openining paper trade account, in home screen on the right side
SECRET_KEY = 'YOUR_SECRET_KEY'                      # get afer openining paper trade account, in home screen on the right side
BASE_URL = 'https://paper-api.alpaca.markets'

# 2. Connect to the API
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

# 3. Submit a Market Order for 1 share of SPY
api.submit_order(
    symbol='SPY',
    qty=1,
    side='buy',
    type='market',
    time_in_force='gtc' # 'Good 'Til Canceled'
)

print("Order submitted successfully!")
