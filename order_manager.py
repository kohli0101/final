"""
Standalone Order Placement Program for Fyers
Places LIMIT orders at current LTP
"""

import sys
import os
from fyers_apiv3 import fyersModel
from datetime import datetime
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config import FYERS_CONFIG
except ImportError:
    print("Error: config.py not found.")
    FYERS_CONFIG = {}

def get_current_price(fyers, symbol):
    """Get current LTP for a symbol"""
    try:
        data = {"symbols": symbol}
        response = fyers.quotes(data=data)
        if response['s'] == 'ok' and 'd' in response and len(response['d']) > 0:
            return response['d'][0]['v']['lp']
        return None
    except Exception as e:
        print(f"Error getting price for {symbol}: {e}")
        return None

def place_limit_order_at_ltp(fyers, symbol, qty, side):
    """
    Place a limit order at the current LTP
    
    Args:
        fyers: FyersModel instance
        symbol: Symbol in Fyers format (e.g., "NSE:SBIN-EQ")
        qty: Quantity to trade
        side: 1 for Buy, -1 for Sell
    """
    ltp = get_current_price(fyers, symbol)
    if not ltp:
        return {"s": "error", "message": f"Could not get LTP for {symbol}"}
    
    data = {
        "symbol": symbol,
        "qty": int(qty),
        "type": 1,        # 1: Limit Order, 2: Market Order
        "side": 1 if side > 0 else -1, # 1: Buy, -1: Sell
        "productType": "INTRADAY", # INTRADAY, MARGIN, CNC
        "limitPrice": float(ltp),
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
        "orderTag": "ManualOrder"
    }
    
    try:
        response = fyers.place_order(data=data)
        return response
    except Exception as e:
        print(f"Error placing order: {e}")
        return {"s": "error", "message": str(e)}

def main():
    # Example usage
    client_id = FYERS_CONFIG.get("CLIENT_ID")
    access_token = FYERS_CONFIG.get("ACCESS_TOKEN")
    
    if not client_id or not access_token:
        print("Error: Missing credentials in config.py")
        return

    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token)
    
    print("\n--- Standalone Order Placement ---")
    symbol = input("Enter symbol (e.g., NSE:SBIN-EQ): ").strip()
    qty = input("Enter quantity: ").strip()
    side_input = input("Enter side (B for Buy, S for Sell): ").strip().upper()
    
    if not symbol or not qty or side_input not in ['B', 'S']:
        print("Invalid input.")
        return
    
    side = 1 if side_input == 'B' else -1
    
    print(f"\nPlacing {'Buy' if side == 1 else 'Sell'} order for {qty} shares of {symbol} at LTP (Limit)...")
    response = place_limit_order_at_ltp(fyers, symbol, qty, side)
    
    print("\nResponse:")
    print(response)

if __name__ == "__main__":
    main()
