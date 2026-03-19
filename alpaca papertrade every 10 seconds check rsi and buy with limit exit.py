import alpaca_trade_api as tradeapi
import pandas_ta as ta
import pandas as pd
import time

# 1. Setup credentials (using Paper Trading keys)
API_KEY = 'PKVGCUDJQ2CWIF7J2LTP6SALT3'
SECRET_KEY = 'GnMRFELScut8t19stbee5ZJERzdJvgyegJjDVDpvGKgp'
BASE_URL = 'https://paper-api.alpaca.markets'

# 1a. Connect to the API
api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

SYMBOL = "SPY"
MAX_QTY = 5

while True:
    # 1. Check current position (Don't buy if over 5 shares)
    try:
        position = api.get_position(SYMBOL)
        current_qty = int(position.qty)
    except:
        current_qty = 0

    if current_qty < MAX_QTY:
        # 2. Get the last 15 minutes of 1-min data
        bars = api.get_bars(SYMBOL, tradeapi.TimeFrame.Minute, limit=20).df
        
        # 3. Calculate RSI
        rsi = ta.rsi(bars['close'], length=14)
        current_rsi = rsi.iloc[-1]
        print(f"Current RSI: {current_rsi:.2f} | Shares held: {current_qty}")

        # 4. Logic: If RSI < 30, Buy 1 share
        if current_rsi < 30:
            print("RSI below 30! Placing Buy Order...")
            buy_order = api.submit_order(
                symbol=SYMBOL, qty=1, side='buy', type='market', time_in_force='gtc'
            )
            
            # 5. Wait for fill and place Limit Sell (+0.25)
            time.sleep(5) # Give the market a moment to fill
            fill_price = float(api.get_order(buy_order.id).filled_avg_price)
            
            api.submit_order(
                symbol=SYMBOL,
                qty=1,
                side='sell',
                type='limit',
                limit_price=fill_price + 0.25,
                time_in_force='gtc'
            )
            print(f"Bought at {fill_price}, Limit Sell set at {fill_price + 0.25}")

            # 6. Don't buy more than 1 every 5 minutes
            print("Waiting 5 minutes before next check...")
            time.sleep(10) 
            
    else:
        print(f"Max shares ({MAX_QTY}) reached. Skipping buy.")

    time.sleep(10) # Check the RSI every minute
    