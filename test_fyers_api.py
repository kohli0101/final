"""
Test Fyers API Connection and Data Retrieval
This will help debug the "Could not get first candle" issue
"""

from fyers_apiv3 import fyersModel
from config import FYERS_CONFIG, STOCK_LIST
from datetime import datetime, timedelta
import json

def load_access_token():
    """Load access token from file"""
    try:
        with open('access_token.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def test_connection():
    """Test basic API connection"""
    print("\n" + "="*70)
    print("TEST 1: Testing Fyers API Connection")
    print("="*70)
    
    client_id = FYERS_CONFIG.get("CLIENT_ID")
    access_token = FYERS_CONFIG.get("ACCESS_TOKEN")
    
    if not access_token or access_token == "YOUR_ACCESS_TOKEN_HERE":
        access_token = load_access_token()
    
    if not client_id or not access_token:
        print("❌ Missing credentials!")
        return None
    
    try:
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token)
        response = fyers.get_profile()
        
        if response.get('s') == 'ok':
            print("✅ Connection successful!")
            data = response.get('data', {})
            print(f"   Name: {data.get('name', 'N/A')}")
            print(f"   Email: {data.get('email_id', 'N/A')}")
            print(f"   Client ID: {data.get('fy_id', 'N/A')}")
            return fyers
        else:
            print(f"❌ Connection failed: {response}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_quotes(fyers):
    """Test getting current quotes"""
    print("\n" + "="*70)
    print("TEST 2: Testing Market Quotes")
    print("="*70)
    
    test_symbols = ["NSE:SBIN-EQ", "NSE:RELIANCE-EQ", "NSE:TCS-EQ"]
    
    for symbol in test_symbols:
        try:
            print(f"\nGetting quote for {symbol}...")
            data = {"symbols": symbol}
            response = fyers.quotes(data)
            
            if response.get('s') == 'ok':
                quote_data = response['d'][0]['v']
                print(f"✅ Success!")
                print(f"   LTP: ₹{quote_data.get('lp', 'N/A')}")
                print(f"   Volume: {quote_data.get('volume', 'N/A')}")
                print(f"   High: ₹{quote_data.get('high_price', 'N/A')}")
                print(f"   Low: ₹{quote_data.get('low_price', 'N/A')}")
            else:
                print(f"❌ Failed: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_historical_data(fyers):
    """Test getting historical candle data"""
    print("\n" + "="*70)
    print("TEST 3: Testing Historical Data Retrieval")
    print("="*70)
    
    symbol = "NSE:SBIN-EQ"
    
    # Test different date ranges
    test_cases = [
        {
            "name": "Last 5 days (Daily)",
            "resolution": "D",
            "days_back": 5
        },
        {
            "name": "Today's data (3-min)",
            "resolution": "3",
            "days_back": 0
        },
        {
            "name": "Yesterday's data (3-min)",
            "resolution": "3",
            "days_back": 1
        }
    ]
    
    for test in test_cases:
        print(f"\n📊 Test: {test['name']}")
        print(f"   Symbol: {symbol}")
        print(f"   Resolution: {test['resolution']} min")
        
        try:
            # Calculate dates
            if test['days_back'] == 0:
                from_date = datetime.now().strftime("%Y-%m-%d")
                to_date = datetime.now().strftime("%Y-%m-%d")
            else:
                from_date = (datetime.now() - timedelta(days=test['days_back']+5)).strftime("%Y-%m-%d")
                to_date = datetime.now().strftime("%Y-%m-%d")
            
            print(f"   From: {from_date}")
            print(f"   To: {to_date}")
            
            data = {
                "symbol": symbol,
                "resolution": test['resolution'],
                "date_format": "1",
                "range_from": from_date,
                "range_to": to_date,
                "cont_flag": "1"
            }
            
            response = fyers.history(data)
            
            if response.get('s') == 'ok':
                candles = response.get('candles', [])
                print(f"   ✅ Success! Got {len(candles)} candles")
                
                if candles:
                    # Show first candle
                    first = candles[0]
                    print(f"\n   First Candle:")
                    print(f"   Time: {datetime.fromtimestamp(first[0]).strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"   Open: ₹{first[1]}")
                    print(f"   High: ₹{first[2]}")
                    print(f"   Low: ₹{first[3]}")
                    print(f"   Close: ₹{first[4]}")
                    print(f"   Volume: {first[5]}")
                    
                    # Show last candle
                    if len(candles) > 1:
                        last = candles[-1]
                        print(f"\n   Last Candle:")
                        print(f"   Time: {datetime.fromtimestamp(last[0]).strftime('%Y-%m-%d %H:%M:%S')}")
                        print(f"   Open: ₹{last[1]}")
                        print(f"   High: ₹{last[2]}")
                        print(f"   Low: ₹{last[3]}")
                        print(f"   Close: ₹{last[4]}")
                        print(f"   Volume: {last[5]}")
                else:
                    print("   ⚠️ No candles returned (might be market closed or weekend)")
            else:
                print(f"   ❌ Failed: {response}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()

def test_first_candle_logic(fyers):
    """Test the exact logic used in the strategy"""
    print("\n" + "="*70)
    print("TEST 4: Testing First Candle Logic (Strategy Method)")
    print("="*70)
    
    symbol = "NSE:SBIN-EQ"
    
    # Try to get first candle of today
    today = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\nTrying to get first 3-min candle of {today}...")
    print(f"Time range: {today} 09:15:00 to {today} 09:18:00")
    
    try:
        data = {
            "symbol": symbol,
            "resolution": "3",
            "date_format": "1",
            "range_from": f"{today} 09:15:00",
            "range_to": f"{today} 09:18:00",
            "cont_flag": "1"
        }
        
        response = fyers.history(data)
        
        print(f"\nResponse status: {response.get('s')}")
        print(f"Full response: {json.dumps(response, indent=2)}")
        
        if response.get('s') == 'ok':
            candles = response.get('candles', [])
            if candles:
                print(f"\n✅ Got {len(candles)} candle(s)")
                for i, candle in enumerate(candles):
                    print(f"\nCandle {i+1}:")
                    print(f"  Time: {datetime.fromtimestamp(candle[0]).strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"  Open: ₹{candle[1]}")
                    print(f"  High: ₹{candle[2]}")
                    print(f"  Low: ₹{candle[3]}")
                    print(f"  Close: ₹{candle[4]}")
                    print(f"  Volume: {candle[5]}")
            else:
                print("\n⚠️ No candles in response")
                print("This is normal if:")
                print("  - Market is closed")
                print("  - Today is a holiday/weekend")
                print("  - Current time is before 9:18 AM")
        else:
            print(f"\n❌ API returned error: {response.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"\n❌ Exception occurred: {e}")
        import traceback
        traceback.print_exc()

def test_previous_day_data(fyers):
    """Test getting previous day's data"""
    print("\n" + "="*70)
    print("TEST 5: Testing Previous Day Data")
    print("="*70)
    
    symbol = "NSE:SBIN-EQ"
    
    print(f"\nGetting last 5 days of daily data...")
    
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
        
        if response.get('s') == 'ok':
            candles = response.get('candles', [])
            print(f"✅ Got {len(candles)} days of data")
            
            if len(candles) >= 2:
                prev_day = candles[-2]
                today = candles[-1] if len(candles) > 1 else None
                
                print(f"\nPrevious Trading Day:")
                print(f"  Date: {datetime.fromtimestamp(prev_day[0]).strftime('%Y-%m-%d')}")
                print(f"  Open: ₹{prev_day[1]}")
                print(f"  High: ₹{prev_day[2]}")
                print(f"  Low: ₹{prev_day[3]}")
                print(f"  Close: ₹{prev_day[4]}")
                
                if today:
                    print(f"\nToday (so far):")
                    print(f"  Date: {datetime.fromtimestamp(today[0]).strftime('%Y-%m-%d')}")
                    print(f"  Open: ₹{today[1]}")
                    print(f"  High: ₹{today[2]}")
                    print(f"  Low: ₹{today[3]}")
                    print(f"  Close: ₹{today[4]}")
            else:
                print("⚠️ Not enough historical data")
        else:
            print(f"❌ Failed: {response}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("\n" + "🔍"*35)
    print("Fyers API Diagnostic Tool")
    print("🔍"*35)
    
    # Test 1: Connection
    fyers = test_connection()
    
    if not fyers:
        print("\n❌ Cannot proceed without valid connection")
        print("\nPlease:")
        print("1. Run: python3 fyers_auth.py")
        print("2. Make sure access token is valid (expires in 24 hours)")
        print("3. Check config.py has correct CLIENT_ID")
        return
    
    # Test 2: Quotes
    test_quotes(fyers)
    
    # Test 3: Historical data
    test_historical_data(fyers)
    
    # Test 4: First candle logic
    test_first_candle_logic(fyers)
    
    # Test 5: Previous day data
    test_previous_day_data(fyers)
    
    # Summary
    print("\n" + "="*70)
    print("DIAGNOSTIC COMPLETE")
    print("="*70)
    print("\n📝 Notes:")
    print("  • 'Could not get first candle' is NORMAL when market is closed")
    print("  • Strategy will work during market hours (9:15 AM - 3:30 PM)")
    print("  • Historical data should show previous days' data")
    print("  • Run this script again tomorrow during market hours to verify")
    print("\n✅ If Tests 1-2 passed: Your API connection is working!")
    print("✅ If Tests 3-5 show data: Historical data retrieval works!")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
