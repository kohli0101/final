"""
Debug script to test first candle fetching
Tests actual data retrieval for stocks that should have qualified
"""

from fyers_apiv3 import fyersModel
from config import FYERS_CONFIG
from datetime import datetime, timedelta
import json

def load_access_token():
    """Load access token from file"""
    try:
        with open('access_token.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def test_stock_conditions(stock_symbol):
    """
    Test if a stock meets entry conditions
    """
    client_id = FYERS_CONFIG.get("CLIENT_ID")
    access_token = FYERS_CONFIG.get("ACCESS_TOKEN")
    
    if not access_token or access_token == "YOUR_ACCESS_TOKEN_HERE":
        access_token = load_access_token()
    
    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token)
    
    symbol = f"NSE:{stock_symbol}-EQ"
    
    print(f"\n{'='*70}")
    print(f"Testing: {stock_symbol}")
    print(f"{'='*70}")
    
    # Step 1: Get previous day data
    print(f"\n📊 Step 1: Getting previous day data...")
    try:
        data = {
            "symbol": symbol,
            "resolution": "D",
            "date_format": "1",
            "range_from": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
            "range_to": datetime.now().strftime("%Y-%m-%d"),
            "cont_flag": "1"
        }
        
        response = fyers.history(data)
        print(f"Response status: {response.get('s')}")
        
        if response['s'] == 'ok' and len(response['candles']) >= 2:
            prev_day = response['candles'][-2]
            prev_day_data = {
                'date': datetime.fromtimestamp(prev_day[0]).strftime('%Y-%m-%d'),
                'open': prev_day[1],
                'high': prev_day[2],
                'low': prev_day[3],
                'close': prev_day[4]
            }
            
            print(f"✅ Previous Day Data:")
            print(f"   Date: {prev_day_data['date']}")
            print(f"   Open: ₹{prev_day_data['open']}")
            print(f"   High: ₹{prev_day_data['high']}")
            print(f"   Low: ₹{prev_day_data['low']}")
            print(f"   Close: ₹{prev_day_data['close']}")
        else:
            print(f"❌ Failed to get previous day data")
            print(f"Response: {json.dumps(response, indent=2)}")
            return
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 2: Get first candle (multiple attempts with different date formats)
    print(f"\n📈 Step 2: Getting first 3-min candle (9:15-9:18)...")
    
    today = datetime.now()
    
    # Try different date formats
    attempts = [
        {
            "name": "Today with time",
            "range_from": f"{today.strftime('%Y-%m-%d')} 09:15:00",
            "range_to": f"{today.strftime('%Y-%m-%d')} 09:18:00"
        },
        {
            "name": "Today date only",
            "range_from": today.strftime("%Y-%m-%d"),
            "range_to": today.strftime("%Y-%m-%d")
        },
        {
            "name": "Last 7 days",
            "range_from": (today - timedelta(days=7)).strftime("%Y-%m-%d"),
            "range_to": today.strftime("%Y-%m-%d")
        }
    ]
    
    first_candle_data = None
    
    for attempt in attempts:
        print(f"\n  Attempt: {attempt['name']}")
        print(f"  From: {attempt['range_from']}")
        print(f"  To: {attempt['range_to']}")
        
        try:
            data = {
                "symbol": symbol,
                "resolution": "3",
                "date_format": "1",
                "range_from": attempt['range_from'],
                "range_to": attempt['range_to'],
                "cont_flag": "1"
            }
            
            response = fyers.history(data)
            print(f"  Status: {response.get('s')}")
            
            if response['s'] == 'ok' and 'candles' in response:
                candles = response['candles']
                print(f"  Got {len(candles)} candles")
                
                if candles:
                    # Show first few candles
                    for i, candle in enumerate(candles[:5]):
                        candle_time = datetime.fromtimestamp(candle[0])
                        print(f"  Candle {i+1}: {candle_time.strftime('%Y-%m-%d %H:%M')} O={candle[1]} H={candle[2]} L={candle[3]} C={candle[4]}")
                        
                        # Check if this is the 9:15 candle
                        if candle_time.hour == 9 and candle_time.minute == 15:
                            first_candle_data = {
                                'time': candle_time.strftime('%Y-%m-%d %H:%M'),
                                'open': candle[1],
                                'high': candle[2],
                                'low': candle[3],
                                'close': candle[4]
                            }
                            print(f"\n  ✅ Found first candle!")
                            break
            else:
                print(f"  ❌ No candles in response")
                if 'message' in response:
                    print(f"  Message: {response['message']}")
        
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        if first_candle_data:
            break
    
    if not first_candle_data:
        print(f"\n❌ Could not find first candle for today")
        print(f"\nNote: This is normal if:")
        print(f"  • Market is closed")
        print(f"  • Today is a holiday")
        print(f"  • Current time is before 9:18 AM")
        return
    
    # Step 3: Check conditions
    print(f"\n✅ First Candle Data:")
    print(f"   Time: {first_candle_data['time']}")
    print(f"   Open: ₹{first_candle_data['open']}")
    print(f"   High: ₹{first_candle_data['high']}")
    print(f"   Low: ₹{first_candle_data['low']}")
    print(f"   Close: ₹{first_candle_data['close']}")
    
    print(f"\n🔍 Checking Entry Conditions:")
    
    # Condition 1: Open == Low
    open_equals_low = abs(first_candle_data['open'] - first_candle_data['low']) < 0.01
    print(f"   1. Open == Low: {open_equals_low}")
    print(f"      Open: ₹{first_candle_data['open']}")
    print(f"      Low: ₹{first_candle_data['low']}")
    print(f"      Difference: ₹{abs(first_candle_data['open'] - first_candle_data['low'])}")
    
    # Condition 2: Open < Previous Day High
    open_below_prev_high = first_candle_data['open'] < prev_day_data['high']
    print(f"   2. Open < Prev Day High: {open_below_prev_high}")
    print(f"      Open: ₹{first_candle_data['open']}")
    print(f"      Prev High: ₹{prev_day_data['high']}")
    
    # Condition 3: Close > Previous Day High
    close_above_prev_high = first_candle_data['close'] > prev_day_data['high']
    print(f"   3. Close > Prev Day High: {close_above_prev_high}")
    print(f"      Close: ₹{first_candle_data['close']}")
    print(f"      Prev High: ₹{prev_day_data['high']}")
    
    # Final result
    all_conditions_met = open_equals_low and open_below_prev_high and close_above_prev_high
    
    print(f"\n{'='*70}")
    if all_conditions_met:
        print(f"✅ {stock_symbol} QUALIFIES!")
        print(f"   All 3 conditions met!")
        print(f"\n   ATM Strike would be: {round(first_candle_data['close'] / 50) * 50}")
    else:
        print(f"❌ {stock_symbol} DOES NOT QUALIFY")
        conditions_failed = []
        if not open_equals_low:
            conditions_failed.append("Open ≠ Low")
        if not open_below_prev_high:
            conditions_failed.append("Open >= Prev High")
        if not close_above_prev_high:
            conditions_failed.append("Close <= Prev High")
        print(f"   Failed conditions: {', '.join(conditions_failed)}")
    print(f"{'='*70}")


def main():
    """Test stocks that should have qualified"""
    
    print("\n" + "🔍"*35)
    print("First Candle Debug Script")
    print("Testing stocks mentioned: HDFCLIFE, NTPC")
    print("🔍"*35)
    
    # Test the stocks you mentioned
    stocks_to_test = ["HDFCLIFE", "NTPC"]
    
    for stock in stocks_to_test:
        try:
            test_stock_conditions(stock)
            print("\n")
        except Exception as e:
            print(f"\n❌ Error testing {stock}: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print("Testing Complete")
    print("="*70)
    print("\n💡 Tips:")
    print("  • If 'Could not find first candle' - market is closed")
    print("  • Test during market hours (9:15 AM - 3:30 PM)")
    print("  • Check if today is a trading day")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
