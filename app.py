"""
Flask Web Server for FnO Trading Dashboard
Mobile-optimized for Samsung S10
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import threading
import time
from datetime import datetime
import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import rate limiter
from rate_limiter import get_rate_limiter, get_batch_manager

app = Flask(__name__)
CORS(app)

# Global rate limiter
rate_limiter = get_rate_limiter()
batch_manager = get_batch_manager()

# Global strategy instance
strategy = None
strategy_thread = None
is_running = False

# Store real-time data
dashboard_data = {
    'status': 'idle',
    'current_time': '',
    'qualified_stocks': {},
    'scan_results': [],
    'pnl_updates': [],
    'last_update': '',
    'total_pnl': 0,
    'total_pnl_percent': 0,
    'market_status': 'closed',
    'api_stats': {
        'calls_today': 0,
        'calls_last_minute': 0,
        'calls_last_second': 0,
        'limit_per_day': 100000,
        'limit_per_minute': 200,
        'limit_per_second': 10
    },
    'total_positions_ce': 0,
    'total_positions_pe': 0,
    'total_capital_ce': 0,
    'total_capital_pe': 0,
    'funds': 0,
    'orders': [],
    'indices': {
        'NIFTY50': {'lp': 0, 'pc': 0},
        'BANKNIFTY': {'lp': 0, 'pc': 0}
    },
    'is_virtual_trading': __import__('config').TRADING_CONFIG.get('VIRTUAL_TRADING', True),
    'logs': []
}

def load_access_token():
    """Load access token from file"""
    try:
        with open('access_token.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def get_market_status():
    """Check if market is open"""
    now = datetime.now()
    current_time = now.time()
    
    # Market hours: 9:15 AM to 3:30 PM
    market_open = now.replace(hour=9, minute=15, second=0).time()
    market_close = now.replace(hour=15, minute=30, second=0).time()
    
    # Check if today is a weekday (0=Monday, 4=Friday)
    if now.weekday() >= 5:  # Saturday or Sunday
        return 'closed'
    
    if market_open <= current_time <= market_close:
        return 'open'
    elif current_time < market_open:
        return 'pre-market'
    else:
        return 'closed'

def add_log(message):
    """Add a log entry to dashboard data"""
    global dashboard_data
    log_entry = {
        'time': datetime.now().strftime('%H:%M:%S'),
        'message': message
    }
    dashboard_data['logs'].insert(0, log_entry)
    if len(dashboard_data['logs']) > 30:
        dashboard_data['logs'] = dashboard_data['logs'][:30]

def update_dashboard_data():
    """Update dashboard data from strategy with tiered updates"""
    global dashboard_data, strategy, rate_limiter
    
    counter = 0
    while is_running and strategy:
        try:
            now_dt = datetime.now()
            dashboard_data['current_time'] = now_dt.strftime('%H:%M:%S')
            dashboard_data['market_status'] = get_market_status()
            dashboard_data['last_update'] = now_dt.isoformat()
            
            # API Trackers (Tiered)
            # Tier 0 (Every 1s): PnL and Stock Quotes
            # Tier 1 (Every 5s): Market Indices
            # Tier 2 (Every 10s): Order Book
            # Tier 3 (Every 15s): Funds
            
            # Update API stats
            dashboard_data['api_stats'] = rate_limiter.get_stats()
            
            # Tier 1: Market Indices (Nifty / BankNifty)
            if counter % 5 == 0:
                indices = strategy.get_multiple_prices(['NSE:NIFTY50-INDEX', 'NSE:NIFTYBANK-INDEX'])
                if indices:
                    nifty = indices.get('NSE:NIFTY50-INDEX', {})
                    banknifty = indices.get('NSE:NIFTYBANK-INDEX', {})
                    dashboard_data['indices']['NIFTY50'] = {
                        'lp': nifty.get('lp', 0),
                        'pc': nifty.get('pc', 0)
                    }
                    dashboard_data['indices']['BANKNIFTY'] = {
                        'lp': banknifty.get('lp', 0),
                        'pc': banknifty.get('pc', 0)
                    }

            # Tier 2: Order Book
            if counter % 10 == 0:
                dashboard_data['orders'] = strategy.get_orders_book()

            # Tier 3: Funds
            if counter % 15 == 0:
                dashboard_data['funds'] = strategy.get_funds()
                
            # Update activity logs from strategy
            if hasattr(strategy, 'activity_logs'):
                dashboard_data['logs'] = strategy.activity_logs
            
            # Tier 0: Update qualified stocks PnL (BATCHED)
            if hasattr(strategy, 'qualified_stocks') and strategy.qualified_stocks:
                # Ensure we have a place to store existing prices
                if 'qualified_stocks' not in dashboard_data:
                    dashboard_data['qualified_stocks'] = {}
                
                total_pnl = 0
                total_invested = 0
                pos_ce = 0
                pos_pe = 0
                cap_ce = 0
                cap_pe = 0
                
                current_qualified = {}
                
                # Fetch all prices in one batch call
                symbols = [details['option_symbol'] for details in strategy.qualified_stocks.values()]
                prices = strategy.get_multiple_prices(symbols)
                
                for stock, details in strategy.qualified_stocks.items():
                    opt_symbol = details['option_symbol']
                    side = details.get('type', 'CE')
                    lot_size = details.get('lot_size', 1)
                    investment = details['entry_price'] * lot_size
                    
                    # Get price from batch results
                    price_info = prices.get(opt_symbol, {})
                    fresh_price = price_info.get('lp') if isinstance(price_info, dict) else None
                    
                    # Use fresh price if available, otherwise fallback to last known or entry
                    last_known = dashboard_data.get('qualified_stocks', {}).get(stock, {}).get('current_price')
                    current_price = fresh_price if fresh_price is not None else (last_known if last_known is not None else details['entry_price'])
                    
                    pnl_per_share = current_price - details['entry_price']
                    total_pnl_for_stock = pnl_per_share * lot_size
                    pnl_percent = (pnl_per_share / details['entry_price']) * 100
                    
                    total_pnl += total_pnl_for_stock
                    total_invested += investment
                    
                    if side == 'CE':
                        pos_ce += 1
                        cap_ce += investment
                    else:
                        pos_pe += 1
                        cap_pe += investment
                    
                    current_qualified[stock] = {
                        'symbol': stock,
                        'option_symbol': opt_symbol,
                        'type': side,
                        'strike': details['strike'],
                        'entry_price': details['entry_price'],
                        'current_price': current_price,
                        'total_pnl': total_pnl_for_stock,
                        'pnl_percent': pnl_percent,
                        'lot_size': lot_size,
                        'investment': investment,
                        'entry_time': details['entry_time'].strftime('%H:%M:%S'),
                        'is_stale': fresh_price is None
                    }
                
                dashboard_data['qualified_stocks'] = current_qualified
                dashboard_data['total_positions_ce'] = pos_ce
                dashboard_data['total_positions_pe'] = pos_pe
                dashboard_data['total_capital_ce'] = cap_ce
                dashboard_data['total_capital_pe'] = cap_pe
                
                if total_invested > 0:
                    dashboard_data['total_pnl'] = total_pnl
                    dashboard_data['total_pnl_percent'] = (total_pnl / total_invested) * 100
                    dashboard_data['total_invested'] = total_invested
                else:
                    dashboard_data['total_pnl'] = 0
                    dashboard_data['total_pnl_percent'] = 0
                    dashboard_data['total_invested'] = 0
            else:
                dashboard_data['qualified_stocks'] = {}
                dashboard_data['total_positions_ce'] = 0
                dashboard_data['total_positions_pe'] = 0
                dashboard_data['total_capital_ce'] = 0
                dashboard_data['total_capital_pe'] = 0
                dashboard_data['total_pnl'] = 0
                dashboard_data['total_pnl_percent'] = 0
                dashboard_data['total_invested'] = 0
            
            counter += 1
            time.sleep(1)  # 1 second updates for PnL
            
        except Exception as e:
            print(f"Error updating dashboard: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(2)

def run_strategy_background():
    """Run strategy in background thread"""
    global strategy, dashboard_data, is_running
    
    try:
        dashboard_data['status'] = 'running'
        strategy.run()
    except Exception as e:
        dashboard_data['status'] = 'error'
        dashboard_data['error'] = str(e)
        print(f"Strategy error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        is_running = False
        dashboard_data['status'] = 'stopped'

@app.route('/')
def index():
    """Main dashboard page"""
    try:
        return render_template('dashboard.html')
    except Exception as e:
        print(f"Error rendering template: {e}")
        import traceback
        traceback.print_exc()
        return f"Error loading dashboard: {str(e)}", 500

@app.route('/token-generator')
def token_generator():
    """Token generator page"""
    try:
        return render_template('token_generator.html')
    except Exception as e:
        print(f"Error rendering token generator: {e}")
        return f"Error: {str(e)}", 500

@app.route('/api/get-auth-url')
def get_auth_url():
    """Get Fyers authorization URL"""
    try:
        from fyers_apiv3 import fyersModel
        from config import FYERS_CONFIG
        
        client_id = FYERS_CONFIG.get("CLIENT_ID")
        secret_key = FYERS_CONFIG.get("SECRET_KEY", "")
        redirect_uri = FYERS_CONFIG.get("REDIRECT_URI", "https://127.0.0.1:5000")
        
        if not client_id or client_id == "YOUR_CLIENT_ID_HERE":
            return jsonify({
                'success': False,
                'message': 'Client ID not configured'
            })
        
        session = fyersModel.SessionModel(
            client_id=client_id,
            secret_key=secret_key,
            redirect_uri=redirect_uri,
            response_type="code",
            grant_type="authorization_code"
        )
        
        auth_url = session.generate_authcode()
        
        return jsonify({
            'success': True,
            'auth_url': auth_url
        })
    except Exception as e:
        print(f"Error generating auth URL: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/api/generate-token', methods=['POST'])
def generate_token():
    """Generate access token from auth code"""
    try:
        from fyers_apiv3 import fyersModel
        from config import FYERS_CONFIG
        
        data = request.get_json()
        auth_code = data.get('auth_code')
        
        if not auth_code:
            return jsonify({
                'success': False,
                'message': 'Auth code is required'
            })
        
        client_id = FYERS_CONFIG.get("CLIENT_ID")
        secret_key = FYERS_CONFIG.get("SECRET_KEY", "")
        redirect_uri = FYERS_CONFIG.get("REDIRECT_URI", "https://127.0.0.1:5000")
        
        session = fyersModel.SessionModel(
            client_id=client_id,
            secret_key=secret_key,
            redirect_uri=redirect_uri,
            response_type="code",
            grant_type="authorization_code"
        )
        
        session.set_token(auth_code)
        response = session.generate_token()
        
        if 'access_token' in response:
            access_token = response['access_token']
            
            # Save to file
            with open('access_token.txt', 'w') as f:
                f.write(access_token)
            
            # Update config in memory (optional)
            FYERS_CONFIG['ACCESS_TOKEN'] = access_token
            
            return jsonify({
                'success': True,
                'access_token': access_token,
                'message': 'Token generated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': f'Failed to generate token: {response}'
            })
            
    except Exception as e:
        print(f"Error generating token: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/api/status')
def get_status():
    """Get current status"""
    try:
        # Update current time even if strategy not running
        dashboard_data['current_time'] = datetime.now().strftime('%H:%M:%S')
        dashboard_data['market_status'] = get_market_status()
        dashboard_data['last_update'] = datetime.now().isoformat()
        
        # Update API stats
        dashboard_data['api_stats'] = rate_limiter.get_stats()
        
        return jsonify(dashboard_data)
    except Exception as e:
        print(f"Error in get_status: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/start', methods=['POST'])
def start_strategy():
    """Start the trading strategy"""
    global strategy, strategy_thread, is_running
    
    if is_running:
        return jsonify({'success': False, 'message': 'Strategy already running'})
    
    try:
        # Import here to avoid circular imports
        from fno_trading_strategy import FnOTradingStrategy
        from config import FYERS_CONFIG, STOCK_LIST
        
        # Get credentials
        client_id = FYERS_CONFIG.get("CLIENT_ID")
        access_token = FYERS_CONFIG.get("ACCESS_TOKEN")
        
        if not access_token or access_token == "YOUR_ACCESS_TOKEN_HERE":
            access_token = load_access_token()
        
        if not client_id or client_id == "YOUR_CLIENT_ID_HERE":
            return jsonify({
                'success': False, 
                'message': 'Client ID not configured. Please update config.py'
            })
        
        if not access_token:
            return jsonify({
                'success': False, 
                'message': 'Access token not found. Please run: python3 fyers_auth.py'
            })
        
        # Initialize strategy
        strategy = FnOTradingStrategy(
            client_id=client_id,
            access_token=access_token,
            stock_list=STOCK_LIST
        )
        
        # Sync virtual trading mode
        strategy.virtual_trading = dashboard_data['is_virtual_trading']
        
        # Pre-fetch previous day data to speed up scan
        try:
            strategy.pre_fetch_prev_day_data()
        except Exception as e:
            print(f"Error pre-fetching data: {e}")
        
        # Start strategy in background
        is_running = True
        strategy_thread = threading.Thread(target=run_strategy_background, daemon=True)
        strategy_thread.start()
        
        # Start dashboard update thread
        update_thread = threading.Thread(target=update_dashboard_data, daemon=True)
        update_thread.start()
        
        dashboard_data['status'] = 'running'
        dashboard_data['config'] = {
            'timeframe': FYERS_CONFIG.get('TIMEFRAME', '3 MIN'),
            'scan_time': '09:18:10',
            'stock_count': len(STOCK_LIST)
        }
        
        return jsonify({
            'success': True, 
            'message': 'Strategy started successfully'
        })
        
    except ImportError as e:
        print(f"Import error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False, 
            'message': f'Import error: {str(e)}. Make sure all files are in the same directory.'
        })
    except Exception as e:
        print(f"Error starting strategy: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False, 
            'message': f'Error starting strategy: {str(e)}'
        })

@app.route('/api/stop', methods=['POST'])
def stop_strategy():
    """Stop the trading strategy"""
    global is_running
    
    is_running = False
    dashboard_data['status'] = 'stopped'
    
    return jsonify({
        'success': True, 
        'message': 'Strategy stopped'
    })

@app.route('/api/exit-position', methods=['POST'])
def exit_position():
    """Exit an individual position"""
    global strategy
    
    if not strategy:
        return jsonify({'success': False, 'message': 'Strategy not initialized'})
    
    try:
        data = request.get_json()
        stock = data.get('stock')
        
        if not stock:
            return jsonify({'success': False, 'message': 'Stock symbol required'})
        
        result = strategy.exit_position(stock)
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in exit_position API: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/config')
def get_config():
    """Get current configuration"""
    try:
        from config import TRADING_CONFIG, STOCK_LIST
        
        return jsonify({
            'timeframe': TRADING_CONFIG['TIMEFRAME'],
            'stocks': STOCK_LIST,
            'stock_count': len(STOCK_LIST),
            'scan_time': f"{TRADING_CONFIG['SCAN_TIME']['HOUR']}:{TRADING_CONFIG['SCAN_TIME']['MINUTE']:02d}:{TRADING_CONFIG['SCAN_TIME']['SECOND']:02d}",
            'monitor_interval': TRADING_CONFIG['MONITOR_INTERVAL']
        })
    except Exception as e:
        print(f"Error loading config: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'timeframe': 3,
            'stocks': [],
            'stock_count': 0,
            'scan_time': '09:18:10',
            'monitor_interval': 60
        })

@app.route('/api/api-stats')
def get_api_stats():
    """Get API usage statistics"""
    try:
        stats = rate_limiter.get_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/api/test-connection', methods=['POST'])
def test_connection():
    """Test Fyers API connection"""
    try:
        from fyers_apiv3 import fyersModel
        from config import FYERS_CONFIG
        
        client_id = FYERS_CONFIG.get("CLIENT_ID")
        access_token = FYERS_CONFIG.get("ACCESS_TOKEN")
        
        if not access_token or access_token == "YOUR_ACCESS_TOKEN_HERE":
            access_token = load_access_token()
        
        if not client_id or not access_token:
            return jsonify({
                'success': False,
                'message': 'Missing credentials. Please update config.py or run fyers_auth.py'
            })
        
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token)
        response = fyers.get_profile()
        
        if response.get('s') == 'ok':
            return jsonify({
                'success': True,
                'message': 'Connection successful',
                'data': response.get('data', {})
            })
        else:
            return jsonify({
                'success': False,
                'message': f'Connection failed: {response}'
            })
    
    except Exception as e:
        print(f"Error testing connection: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/exit-all', methods=['POST'])
def exit_all():
    """Exit all positions immediately"""
    global strategy
    if not strategy:
        return jsonify({'success': False, 'message': 'Strategy not running'})
    
    try:
        res = strategy.exit_all_positions()
        return jsonify(res)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/toggle-virtual', methods=['POST'])
def toggle_virtual():
    """Toggle between virtual and live trading"""
    global strategy, dashboard_data
    
    try:
        data = request.get_json()
        is_virtual = data.get('is_virtual', True)
        
        dashboard_data['is_virtual_trading'] = is_virtual
        
        if strategy:
            strategy.virtual_trading = is_virtual
            mode_text = "VIRTUAL" if is_virtual else "LIVE"
            strategy.log_activity(f"🔄 Trading mode switched to {mode_text}")
            
        return jsonify({
            'success': True,
            'is_virtual': is_virtual,
            'message': f"Switched to {'Virtual' if is_virtual else 'Live'} Trading"
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/service-worker.js')
def serve_sw():
    return send_from_directory('static', 'service-worker.js')

if __name__ == '__main__':
    print("\n" + "="*70)
    print("FnO Trading Dashboard Server")
    print("="*70)
    print("\nStarting server...")
    print("Access dashboard at: http://localhost:5000")
    
    # Get local IP
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"Or from your phone: http://{local_ip}:5000")
    except:
        print("Or from your phone: http://YOUR_COMPUTER_IP:5000")
    
    print("\nPress Ctrl+C to stop")
    print("="*70 + "\n")
    
    # Run on all interfaces so phone can connect
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
