"""
NSE FnO Trading Strategy using Fyers API v3
WITH PROPER LOT SIZE HANDLING AND ACCURATE P&L CALCULATION
"""

from fyers_apiv3 import fyersModel
import pandas as pd
from datetime import datetime, timedelta
import time
import math
import os
import requests
import concurrent.futures

class FnOTradingStrategy:
    def __init__(self, client_id, access_token, stock_list, rate_limiter=None):
        """
        Initialize the trading strategy
        
        Args:
            client_id: Fyers client ID
            access_token: Fyers access token
            stock_list: List of FnO stock symbols (e.g., ['SBIN', 'RELIANCE', 'TCS'])
            rate_limiter: Optional rate limiter instance
        """
        self.fyers = fyersModel.FyersModel(client_id=client_id, token=access_token)
        self.stock_list = stock_list
        self.qualified_stocks = {}  # Stores stocks that meet criteria (CE or PE)
        
        # Virtual trading mode
        from config import TRADING_CONFIG
        self.virtual_trading = TRADING_CONFIG.get("VIRTUAL_TRADING", True)
        
        # Rate limiter
        from rate_limiter import get_rate_limiter, get_batch_manager
        self.rate_limiter = rate_limiter or get_rate_limiter()
        self.batch_manager = get_batch_manager()
        
        # Load lot sizes from Fyers master CSV
        self.lot_size_map = {}
        self.load_lot_sizes()
        
        # Pre-fetch cache
        self.prev_day_cache = {}
        
        # Activity logs
        self.activity_logs = []
        self.max_logs = 50

    def log_activity(self, message):
        """Add a log entry with timestamp"""
        log_entry = {
            'time': datetime.now().strftime('%H:%M:%S'),
            'message': message
        }
        self.activity_logs.insert(0, log_entry)
        if len(self.activity_logs) > self.max_logs:
            self.activity_logs = self.activity_logs[:self.max_logs]
        print(f"[{log_entry['time']}] {message}")
        
    def get_current_quote(self, symbol):
        """
        Get full quote for a symbol
        
        Args:
            symbol: Symbol in Fyers format
            
        Returns:
            dict: Full quote data or None
        """
        try:
            cache_key = f"quote_{symbol}"
            data = {"symbols": symbol}
            
            response = self.batch_manager.get_with_cache(
                cache_key,
                self.fyers.quotes,
                data
            )
            
            if response['s'] == 'ok' and 'd' in response and len(response['d']) > 0:
                return response['d'][0]['v']
            return None
        except Exception as e:
            print(f"Error getting quote for {symbol}: {e}")
            return None

    def get_funds(self):
        """Fetch available funds from Fyers"""
        try:
            response = self.rate_limiter.make_call(self.fyers.funds)
            if response['s'] == 'ok':
                # Return total balance / available margin
                fund_limit = next((item for item in response['fund_limit'] if item['title'] == 'Total Balance'), None)
                if fund_limit:
                    return fund_limit['equityAmount']
            return 0
        except Exception as e:
            print(f"Error getting funds: {e}")
            return 0

    def get_orders_book(self):
        """Fetch daily order book from Fyers"""
        try:
            response = self.rate_limiter.make_call(self.fyers.orderbook)
            if response['s'] == 'ok':
                return response['orderBook']
            return []
        except Exception as e:
            print(f"Error getting orderbook: {e}")
            return []

    def load_lot_sizes(self):
        """
        Download and load lot sizes from Fyers master CSV
        """
        local_file = "nse_fo.csv"
        url = "https://public.fyers.in/sym_details/NSE_FO.csv"
        
        try:
            # Download if not exists or if more than 24 hours old
            should_download = False
            if not os.path.exists(local_file):
                should_download = True
            else:
                file_age = time.time() - os.path.getmtime(local_file)
                if file_age > 86400:  # 24 hours
                    should_download = True
            
            if should_download:
                print(f"Downloading Fyers master symbol file from {url}...")
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    with open(local_file, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded {local_file}")
                else:
                    print(f"Failed to download Fyers master file: Status {response.status_code}")
            
            if os.path.exists(local_file):
                # Fyers NSE_FO.csv structure:
                # Column 3 is lot_size, Column 9 is fyers_symbol
                df = pd.read_csv(local_file, header=None, low_memory=False)
                # Filter rows where index 9 (symbol) and index 3 (lot size) are present
                self.lot_size_map = dict(zip(df[9], df[3]))
                print(f"Loaded {len(self.lot_size_map)} lot sizes from {local_file}")
            else:
                print("Could not load lot sizes: nse_fo.csv not found.")
        except Exception as e:
            print(f"Error loading lot sizes: {e}")
            self.lot_size_map = {}

    def get_lot_size(self, symbol, fallback_lot_size=1):
        """
        Get lot size for a symbol from the master map
        """
        lot_size = self.lot_size_map.get(symbol)
        if lot_size is not None:
            return int(lot_size)
        return fallback_lot_size

    def get_current_price(self, symbol):
        """
        Get current LTP (Last Traded Price)
        """
        quote = self.get_current_quote(symbol)
        if quote:
            return quote.get('lp')  # Last price
        return None
    
    def get_symbol_format(self, stock):
        """Convert stock symbol to Fyers format"""
        return f"NSE:{stock}-EQ"
    
    def get_previous_day_data(self, symbol):
        """
        Get previous day's high and close
        
        Args:
            symbol: Stock symbol in Fyers format
            
        Returns:
            dict with 'high', 'low' and 'close' or None
        """
        try:
            # Get last 2 days of daily data
            data = {
                "symbol": symbol,
                "resolution": "D",
                "date_format": "1",
                "range_from": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
                "range_to": datetime.now().strftime("%Y-%m-%d"),
                "cont_flag": "1"
            }
            
            # Use rate-limited API call
            response = self.rate_limiter.make_call(self.fyers.history, data)
            
            if response['s'] == 'ok' and len(response['candles']) >= 2:
                # Get second last day's data (previous trading day)
                prev_day = response['candles'][-2]
                return {
                    'high': prev_day[2],  # High
                    'low': prev_day[3],   # Low
                    'close': prev_day[4]  # Close
                }
            return None
        except Exception as e:
            print(f"Error getting previous day data for {symbol}: {e}")
            return None

    def pre_fetch_prev_day_data(self):
        """Pre-fetch previous day OHLC for all stocks in the list to speed up scan"""
        print(f"Pre-fetching previous day data for {len(self.stock_list)} stocks...")
        symbols = [self.get_symbol_format(stock) for stock in self.stock_list]
        
        # Use ThreadPool to fetch history in parallel (since we need 'resolution': 'D')
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_stock = {executor.submit(self.get_previous_day_data, sym): sym for sym in symbols}
            for future in concurrent.futures.as_completed(future_to_stock):
                sym = future_to_stock[future]
                try:
                    data = future.result()
                    if data:
                        self.prev_day_cache[sym] = data
                except Exception as e:
                    print(f"Error pre-fetching {sym}: {e}")
        
        print(f"Pre-fetched data for {len(self.prev_day_cache)} / {len(symbols)} stocks.")
    
    def get_first_candle(self, symbol):
        """
        Get first 3-minute candle of the day (9:15-9:18)
        Enhanced with multiple fallback strategies
        
        Args:
            symbol: Stock symbol in Fyers format
            
        Returns:
            dict with 'open', 'high', 'low', 'close' or None
        """
        try:
            today = datetime.now()
            
            # Strategy 1: Try exact time range (9:15-9:18)
            data = {
                "symbol": symbol,
                "resolution": "3",
                "date_format": "1",
                "range_from": f"{today.strftime('%Y-%m-%d')} 09:15:00",
                "range_to": f"{today.strftime('%Y-%m-%d')} 09:30:00",  # Extended to 9:30 to ensure we get the candle
                "cont_flag": "1"
            }
            
            response = self.rate_limiter.make_call(self.fyers.history, data)
            
            if response['s'] == 'ok' and 'candles' in response and len(response['candles']) > 0:
                # Look for the first candle (should be at 9:15)
                for candle in response['candles']:
                    candle_time = datetime.fromtimestamp(candle[0])
                    
                    # Check if this is the 9:15 candle (first 3-min candle)
                    if candle_time.hour == 9 and candle_time.minute in [15, 18]:  # 9:15 or 9:18
                        return {
                            'open': candle[1],
                            'high': candle[2],
                            'low': candle[3],
                            'close': candle[4],
                            'time': candle_time
                        }
                
                # If we didn't find exact 9:15, return first candle anyway
                if response['candles']:
                    first_candle = response['candles'][0]
                    candle_time = datetime.fromtimestamp(first_candle[0])
                    
                    # Only accept if it's morning candle (between 9:15 and 9:30)
                    if candle_time.hour == 9 and 15 <= candle_time.minute < 30:
                        return {
                            'open': first_candle[1],
                            'high': first_candle[2],
                            'low': first_candle[3],
                            'close': first_candle[4],
                            'time': candle_time
                        }
            
            # Strategy 2: Try with just today's date (let API return all candles)
            data2 = {
                "symbol": symbol,
                "resolution": "3",
                "date_format": "1",
                "range_from": today.strftime("%Y-%m-%d"),
                "range_to": today.strftime("%Y-%m-%d"),
                "cont_flag": "1"
            }
            
            response2 = self.rate_limiter.make_call(self.fyers.history, data2)
            
            if response2['s'] == 'ok' and 'candles' in response2 and len(response2['candles']) > 0:
                # Get the first candle of the day
                first_candle = response2['candles'][0]
                candle_time = datetime.fromtimestamp(first_candle[0])
                
                # Verify it's the morning candle
                if candle_time.hour == 9 and candle_time.minute >= 15:
                    return {
                        'open': first_candle[1],
                        'high': first_candle[2],
                        'low': first_candle[3],
                        'close': first_candle[4],
                        'time': candle_time
                    }
            
            return None
            
        except Exception as e:
            print(f"Error getting first candle for {symbol}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def check_entry_conditions(self, symbol, first_candle, prev_day, side='CE'):
        """
        Check if stock meets entry conditions:
        CE: 
            1. First candle Open == Low
            2. Open < Previous Day High
            3. Close > Previous Day High
        PE:
            1. First 3 minute open == High
            2. Open > prev. Day low
            3. Close < previous day Low
        """
        if not first_candle or not prev_day:
            return False
        
        if side == 'CE':
            # Condition 1: Open == Low (with small tolerance)
            cond1 = abs(first_candle['open'] - first_candle['low']) < 0.01
            # Condition 2: Open < Previous Day High
            cond2 = first_candle['open'] < prev_day['high']
            # Condition 3: Close > Previous Day High
            cond3 = first_candle['close'] > prev_day['high']
            
            conditions_met = cond1 and cond2 and cond3
            if conditions_met:
                print(f"\n✓ {symbol} meets CE conditions:")
        else:
            # PE Condition 1: First 3 minute open == High
            cond1 = abs(first_candle['open'] - first_candle['high']) < 0.01
            # PE Condition 2: Open > prev. Day low
            prev_low = prev_day.get('low')
            if prev_low is None:
                return False
            cond2 = first_candle['open'] > prev_low
            # PE Condition 3: Close < previous day Low
            cond3 = first_candle['close'] < prev_low
            
            conditions_met = cond1 and cond2 and cond3
            if conditions_met:
                print(f"\n✓ {symbol} meets PE conditions:")

        if conditions_met:
            print(f"  First Candle: O={first_candle['open']}, H={first_candle['high']}, L={first_candle['low']}, C={first_candle['close']}")
            print(f"  Prev Day: H={prev_day['high']}, L={prev_day.get('low', 'N/A')}, C={prev_day['close']}")
        
        return conditions_met
    
    def get_atm_strike(self, spot_price, strike_difference=50):
        """
        Calculate ATM (At The Money) strike price
        """
        # Round to nearest strike
        atm_strike = round(spot_price / strike_difference) * strike_difference
        return int(atm_strike)
    
    def get_ce_option_symbol(self, stock, strike, expiry_date=None):
        """
        Get CE option symbol in Fyers format
        """
        if expiry_date is None:
            expiry_date = self.get_nearest_expiry(stock)
        
        return f"NSE:{stock}{expiry_date}{strike}CE"

    def get_pe_option_symbol(self, stock, strike, expiry_date=None):
        """
        Get PE option symbol in Fyers format
        """
        if expiry_date is None:
            expiry_date = self.get_nearest_expiry(stock)
        
        return f"NSE:{stock}{expiry_date}{strike}PE"
    
    def get_nearest_expiry(self, stock):
        """
        Get nearest expiry date for the stock
        """
        now = datetime.now()
        # Simplified: return current month expiry
        month_name = now.strftime("%b").upper()
        year = now.strftime("%y")
        
        return f"{year}{month_name}"
    
    def get_multiple_prices(self, symbols):
        """
        Get prices for multiple symbols efficiently using batch API
        """
        return self.batch_manager.batch_get_quotes(self.fyers, symbols)
    
    def scan_stocks_at_918(self):
        """
        Scan all stocks at 9:18 AM to check entry conditions
        Should be called at 9:18:10 AM
        """
        print(f"\n{'='*60}")
        print(f"Starting scan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Scanning {len(self.stock_list)} stocks...")
        print(f"{'='*60}")
        
        scan_results = {
            'total': len(self.stock_list),
            'qualified_ce': 0,
            'qualified_pe': 0,
            'no_prev_day': 0,
            'no_first_candle': 0,
            'failed_conditions': 0
        }

        # Step 1: Pre-fetch all first candles in parallel
        print(f"Fetching first candles for all stocks in parallel...")
        stock_data = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            future_to_stock = {
                executor.submit(self.get_first_candle, self.get_symbol_format(s)): s 
                for s in self.stock_list
            }
            for future in concurrent.futures.as_completed(future_to_stock):
                stock = future_to_stock[future]
                try:
                    stock_data[stock] = future.result()
                except Exception as e:
                    print(f"  ❌ Error fetching candle for {stock}: {e}")
                    stock_data[stock] = None

        # Step 2: Screen stocks that meet OHLC conditions
        potential_entries = []
        for stock in self.stock_list:
            symbol = self.get_symbol_format(stock)
            
            # Use cache for prev day data
            prev_day = self.prev_day_cache.get(symbol)
            if not prev_day:
                # Fallback to single fetch if not in cache
                prev_day = self.get_previous_day_data(symbol)
                if not prev_day:
                    scan_results['no_prev_day'] += 1
                    continue
                self.prev_day_cache[symbol] = prev_day
            
            first_candle = stock_data.get(stock)
            if not first_candle:
                scan_results['no_first_candle'] += 1
                continue
            
            # Check conditions
            ce_qualified = self.check_entry_conditions(stock, first_candle, prev_day, side='CE')
            pe_qualified = self.check_entry_conditions(stock, first_candle, prev_day, side='PE')
            
            if ce_qualified or pe_qualified:
                side = 'CE' if ce_qualified else 'PE'
                spot_price = first_candle['close']
                atm_strike = self.get_atm_strike(spot_price)
                
                option_symbol = self.get_ce_option_symbol(stock, atm_strike) if side == 'CE' else \
                               self.get_pe_option_symbol(stock, atm_strike)
                
                potential_entries.append({
                    'stock': stock,
                    'symbol': symbol,
                    'side': side,
                    'spot_price': spot_price,
                    'atm_strike': atm_strike,
                    'option_symbol': option_symbol
                })

        if not potential_entries:
            print("No stocks met OHLC entry conditions.")
            return

        # Step 3: Fetch all required option quotes in ONE batch
        print(f"Fetching quotes for {len(potential_entries)} potential entries...")
        option_symbols = [e['option_symbol'] for e in potential_entries]
        option_quotes = self.get_multiple_prices(option_symbols)

        # Step 4: Execute orders for qualified stocks
        for entry in potential_entries:
            stock = entry['stock']
            option_symbol = entry['option_symbol']
            side = entry['side']
            
            option_quote = option_quotes.get(option_symbol)
            if option_quote:
                option_price = option_quote.get('lp')
                # Use CSV-based lot size
                lot_size = self.get_lot_size(option_symbol, fallback_lot_size=option_quote.get('ls', 1))
                
                if option_price:
                    self.qualified_stocks[stock] = {
                        'spot_symbol': entry['symbol'],
                        'option_symbol': option_symbol,
                        'type': side,
                        'strike': entry['atm_strike'],
                        'entry_time': datetime.now(),
                        'entry_price': option_price,
                        'spot_price': entry['spot_price'],
                        'lot_size': lot_size,
                        'status': 'RUNNING'
                    }
                    
                    if side == 'CE': scan_results['qualified_ce'] += 1
                    else: scan_results['qualified_pe'] += 1
                    
                    print(f"  ✅ {side} QUALIFIED: {stock} at ₹{option_price:.2f}")

                    # PLACING ORDER
                    order_data = {
                        "symbol": option_symbol,
                        "qty": int(lot_size),
                        "type": 1, "side": 1, "productType": "INTRADAY",
                        "limitPrice": float(option_price), "stopPrice": 0, "validity": "DAY",
                        "disclosedQty": 0, "offlineOrder": False, "orderTag": "AutoEntryScanFast"
                    }
                    
                    try:
                        if self.virtual_trading:
                            print(f"    📝 VIRTUAL ORDER (SIMULATED): {option_symbol} qty {lot_size}")
                            self.log_activity(f"📝 Virtual Order: {stock} {side} at ₹{option_price:.2f}")
                        else:
                            resp = self.rate_limiter.make_call(self.fyers.place_order, order_data)
                            if resp['s'] == 'ok':
                                print(f"    🚀 ORDER PLACED: {resp.get('id')}")
                                self.log_activity(f"🚀 Live Order: {stock} {side} at ₹{option_price:.2f}")
                            else:
                                print(f"    ❌ ORDER FAILED: {resp.get('message')}")
                                self.log_activity(f"❌ Order Failed: {stock} {side} - {resp.get('message')}")
                    except Exception as e:
                        print(f"    ❌ ERROR: {e}")
        
        # Print summary
        print(f"\n{'='*60}")
        print(f"SCAN SUMMARY")
        print(f"{'='*60}")
        print(f"Total stocks scanned: {scan_results['total']}")
        print(f"✅ Qualified CE: {scan_results['qualified_ce']}")
        print(f"✅ Qualified PE: {scan_results['qualified_pe']}")
        print(f"❌ No previous day data: {scan_results['no_prev_day']}")
        print(f"❌ No first candle: {scan_results['no_first_candle']}")
        print(f"❌ Failed conditions: {scan_results['failed_conditions']}")
        print(f"{'='*60}\n")
        
    def calculate_pnl(self, entry_price, current_price, lot_size):
        """
        Calculate PnL with lot size
        """
        # Calculate per share P&L
        pnl_per_share = current_price - entry_price
        
        # Calculate total P&L (per share * lot size)
        total_pnl = pnl_per_share * lot_size
        
        # Calculate percentage
        pnl_percent = ((current_price - entry_price) / entry_price) * 100
        
        # Calculate total investment
        total_investment = entry_price * lot_size
        
        # Calculate current value
        current_value = current_price * lot_size
        
        return {
            'pnl_per_share': pnl_per_share,
            'total_pnl': total_pnl,
            'pnl_percent': pnl_percent,
            'entry_price': entry_price,
            'current_price': current_price,
            'lot_size': lot_size,
            'total_investment': total_investment,
            'current_value': current_value
        }
    
    def monitor_pnl(self):
        """
        Monitor PnL for all qualified stocks every minute
        Optimized to use batch API calls
        """
        if not self.qualified_stocks:
            print("No stocks to monitor")
            return
        
        print(f"\n{'='*80}")
        print(f"PnL Update at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        # Get all option symbols to fetch
        symbols = [details['option_symbol'] for details in self.qualified_stocks.values()]
        
        # Fetch all prices in batch
        try:
            prices = self.get_multiple_prices(symbols)
        except Exception as e:
            print(f"Error fetching batch prices: {e}")
            prices = {}
        
        totals = {
            'CE': {'invested': 0, 'value': 0, 'count': 0},
            'PE': {'invested': 0, 'value': 0, 'count': 0}
        }
        
        for stock, details in self.qualified_stocks.items():
            opt_symbol = details['option_symbol']
            side = details['type']
            
            # Get price from batch result
            current_price = prices.get(opt_symbol, {}).get('lp')
            
            if current_price:
                pnl_data = self.calculate_pnl(
                    details['entry_price'], 
                    current_price,
                    details['lot_size']
                )
                
                # Update totals
                totals[side]['invested'] += pnl_data['total_investment']
                totals[side]['value'] += pnl_data['current_value']
                totals[side]['count'] += 1
                
                # Color coding for PnL
                pnl_symbol = "🟢" if pnl_data['total_pnl'] >= 0 else "🔴"
                
                print(f"\n{stock} ({details['strike']} {side}) - Lot: {details['lot_size']}")
                print(f"  Entry: ₹{details['entry_price']:.2f} at {details['entry_time'].strftime('%H:%M:%S')}")
                print(f"  LTP: ₹{current_price:.2f} ({pnl_symbol} P&L: ₹{pnl_data['total_pnl']:,.2f} / {pnl_data['pnl_percent']:+.2f}%)")
            else:
                print(f"\n{stock}: Could not fetch LTP for {opt_symbol}")
        
        # Print summary
        total_inv = totals['CE']['invested'] + totals['PE']['invested']
        total_val = totals['CE']['value'] + totals['PE']['value']
        
        if total_inv > 0:
            overall_pnl = total_val - total_inv
            overall_pnl_pct = (overall_pnl / total_inv) * 100
            
            print(f"\n{'='*80}")
            print(f"SUMMARY")
            print(f"  CE Positions: {totals['CE']['count']} (Invested: ₹{totals['CE']['invested']:,.2f})")
            print(f"  PE Positions: {totals['PE']['count']} (Invested: ₹{totals['PE']['invested']:,.2f})")
            print(f"  {'🟢' if overall_pnl >= 0 else '🔴'} Total P&L: ₹{overall_pnl:,.2f} ({overall_pnl_pct:+.2f}%)")
            
            # Show API usage stats
            stats = self.rate_limiter.get_stats()
            print(f"\n📊 API Calls: Today: {stats['calls_today']} | Min: {stats['calls_last_minute']} | Sec: {stats['calls_last_second']}")
            print(f"{'='*80}")
    
    def exit_position(self, stock):
        """
        Square off an open position at LTP
        
        Args:
            stock: Stock symbol (e.g., 'SBIN')
            
        Returns:
            dict: Success/Failure status and message
        """
        if stock not in self.qualified_stocks:
            return {"success": False, "message": f"No open position for {stock}"}
        
        details = self.qualified_stocks[stock]
        opt_symbol = details['option_symbol']
        lot_size = details['lot_size']
        side = -1  # Default: Sell (since we are squaring off a BUY position)
        
        # Get current LTP for limit order
        ltp = self.get_current_price(opt_symbol)
        if not ltp:
            return {"success": False, "message": f"Could not get LTP for {opt_symbol}"}
        
        data = {
            "symbol": opt_symbol,
            "qty": int(lot_size),
            "type": 1,        # 1: Limit Order
            "side": side,     # -1: Sell
            "productType": "INTRADAY",
            "limitPrice": float(ltp),
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": False,
            "orderTag": "ExitDashboard"
        }
        
        try:
            print(f"SQUARING OFF {stock}: {opt_symbol} at {ltp}...")
            
            if self.virtual_trading:
                print(f"    📝 VIRTUAL EXIT (SIMULATED): {opt_symbol} at {ltp}")
                self.log_activity(f"✅ Virtual Exit: {stock} at ₹{ltp:.2f}")
                # Mark as EXITED
                self.qualified_stocks[stock]['status'] = 'EXITED'
                self.qualified_stocks[stock]['exit_price'] = ltp
                self.qualified_stocks[stock]['exit_time'] = datetime.now()
                return {"success": True, "message": f"Virtual Exit {stock} at ₹{ltp:.2f}"}
            
            response = self.rate_limiter.make_call(self.fyers.place_order, data)
            
            if response['s'] == 'ok':
                # Mark as EXITED instead of deleting
                self.qualified_stocks[stock]['status'] = 'EXITED'
                self.qualified_stocks[stock]['exit_price'] = ltp
                self.qualified_stocks[stock]['exit_time'] = datetime.now()
                self.log_activity(f"✅ Live Exit: {stock} at ₹{ltp:.2f}")
                return {"success": True, "message": f"Exited {stock} at ₹{ltp:.2f}", "order_id": response.get('id')}
            else:
                self.log_activity(f"❌ Exit Failed: {stock} - {response.get('message', 'Unknown error')}")
                return {"success": False, "message": f"Fyers Error: {response.get('message', 'Unknown error')}"}
        except Exception as e:
            print(f"Error exiting position for {stock}: {e}")
            return {"success": False, "message": str(e)}

    def exit_all_positions(self):
        """Exit all currently running positions immediately"""
        results = []
        running_stocks = [s for s, d in self.qualified_stocks.items() if d.get('status') == 'RUNNING']
        
        if not running_stocks:
            return {"success": True, "message": "No running positions to exit"}
            
        self.log_activity(f"⚠️ PANIC EXIT TRIGGERED for {len(running_stocks)} positions")
        
        for stock in running_stocks:
            res = self.exit_position(stock)
            results.append(res)
            if res.get('success'):
                self.log_activity(f"✅ Panic Exit: {stock} successful")
            else:
                self.log_activity(f"❌ Panic Exit: {stock} failed - {res.get('message')}")
        
        return {"success": True, "results": results}
    
    def run(self):
        """
        Main execution loop - Scans ONCE at 9:18:10 AM, then monitors P&L
        """
        print("Starting FnO Trading Strategy...")
        print(f"Monitoring stocks: {', '.join(self.stock_list)}")
        print("\n⚠️  Entry conditions will be checked ONCE at 9:18:10 AM")
        print("After that, only P&L monitoring will continue")
        
        # Wait until 9:18:10 AM to scan
        now = datetime.now()
        target_time = now.replace(hour=9, minute=18, second=10, microsecond=0)
        
        # If already past 9:18:10, scan immediately
        if now >= target_time:
            print(f"\n⚠️  Already past 9:18:10 AM - scanning now...")
        else:
            wait_seconds = (target_time - now).total_seconds()
            print(f"\nWaiting until 9:18:10 AM ({wait_seconds:.0f} seconds)...")
            time.sleep(wait_seconds)
        
        # Scan stocks at 9:18:10 (ONLY ONCE)
        print("\n🔍 Starting ENTRY SCAN...")
        self.scan_stocks_at_918()
        
        if not self.qualified_stocks:
            print("\n✗ No stocks qualified for trading today")
            print("Strategy will remain idle. You can stop it.")
            return
        
        print(f"\n✓ Tracking {len(self.qualified_stocks)} stock(s)")
        print("📊 Starting P&L monitoring (every 2 seconds)...")
        print("Entry scan complete - will NOT scan again until you restart")
        
        # Monitor P&L continuously (every 2 seconds)
        last_monitor = time.time()
        monitor_interval = 2  # 2 seconds
        
        while True:
            try:
                current_time = time.time()
                
                # Update P&L every 2 seconds
                if current_time - last_monitor >= monitor_interval:
                    self.monitor_pnl()
                    last_monitor = current_time
                
                time.sleep(0.5)  # Small sleep to prevent CPU spinning
                
            except KeyboardInterrupt:
                print("\n\nStopping strategy...")
                break
            except Exception as e:
                print(f"\nError in monitoring loop: {e}")
                time.sleep(2)

def main():
    """
    Main function to run the strategy
    """
    # Configuration
    CLIENT_ID = "YOUR_CLIENT_ID"
    ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
    
    # List of FnO stocks to monitor
    STOCK_LIST = [
        "SBIN",
        "RELIANCE", 
        "TCS",
        "INFY",
        "HDFCBANK",
        "ICICIBANK",
        "KOTAKBANK",
        "BHARTIARTL",
        "ITC",
        "HINDUNILVR"
    ]
    
    # Initialize and run strategy
    strategy = FnOTradingStrategy(
        client_id=CLIENT_ID,
        access_token=ACCESS_TOKEN,
        stock_list=STOCK_LIST
    )
    
    strategy.run()

if __name__ == "__main__":
    main()
