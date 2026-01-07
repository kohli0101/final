"""
Configuration file for FnO Trading Strategy
Updated with ALL NSE F&O Stocks (165+ stocks)
"""

import os

# ============================================================================
# FYERS API CREDENTIALS
# Update these with your actual credentials
# ============================================================================

FYERS_CONFIG = {
    "CLIENT_ID": "Q8Z7HIY0II-100",      # Example: "ABCD1234-100"
    "SECRET_KEY": "RVRPS35QYQ",     # Your app secret key
    "ACCESS_TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIiwieDoyIl0sImF0X2hhc2giOiJnQUFBQUFCcFhHMFRQUG50LS01eDlFY0xaWC1rRmJuWF9jU3F0VkdYclYwR05aR0Utb3hRWlJjVmYwODY5N1R5LWFqZl9KMncxTVFhUGpCNTliZ3l1RUdpVVY0NF9SNFdXZVRJak5PS1pRMHlteG1ZVl9fb0NBND0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiIyNGNhYTRkMjc5OWU1ZDI0NjA1Y2RjMDUzOGQ5OWVmMjZmZmY0ZTc4MWY2ODFlYzVhOTE0ZDExNyIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWFIwMjcwMCIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzY3NzQ1ODAwLCJpYXQiOjE3Njc2NjQ5MTUsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc2NzY2NDkxNSwic3ViIjoiYWNjZXNzX3Rva2VuIn0.IrAMhDx3o-RT3FBw1M1YNcyER9dAbNbieLSIR_WyekI", # Will be auto-updated by token generator
    "REDIRECT_URI": "https://google.com"  # Must match Fyers app settings
}

# ============================================================================
# ALL NSE F&O STOCKS (Complete List - 165+ stocks)
# ============================================================================

# You can use ALL_FNO_STOCKS or create custom lists below
ALL_FNO_STOCKS = [
    # NIFTY 50 Stocks
    "ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK",
    "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BPCL", "BHARTIARTL",
    "BRITANNIA", "CIPLA", "COALINDIA", "DIVISLAB", "DRREDDY",
    "EICHERMOT", "GRASIM", "HCLTECH", "HDFCBANK", "HDFCLIFE",
    "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", "ITC",
    "INDUSINDBK", "INFY", "JSWSTEEL", "KOTAKBANK", "LT",
    "M&M", "MARUTI", "NTPC", "NESTLEIND", "ONGC",
    "POWERGRID", "RELIANCE", "SBILIFE", "SHRIRAMFIN", "SBIN",
    "SUNPHARMA", "TCS", "TATACONSUM", "TATAMOTORS", "TATAPOWER",
    "TATASTEEL", "TECHM", "TITAN", "ULTRACEMCO", "WIPRO",
    
    # NIFTY Next 50
    "ACC", "ADANIGREEN", "AMBUJACEM", "ATGL", "AUBANK",
    "BANDHANBNK", "BERGEPAINT", "BIOCON", "BOSCHLTD", "CANBK",
    "CHOLAFIN", "COLPAL", "DABUR", "DLF", "DMART",
    "GAIL", "GODREJCP", "HAVELLS", "HINDPETRO", "ICICIGI",
    "ICICIPRULI", "IDEA", "IDFCFIRSTB", "IOC", "IRCTC",
    "JSWENERGY", "LICHSGFIN", "LTIM", "MARICO", "MCDOWELL-N",
    "MOTHERSON", "MPHASIS", "MUTHOOTFIN", "NMDC", "OFSS",
    "PAGEIND", "PERSISTENT", "PETRONET", "PIDILITIND", "PEL",
    "PFC", "PIIND", "PNB", "RECLTD", "SBICARD",
    "SIEMENS", "TRENT", "TVSMOTOR", "UNITDSPR", "VEDL",
    
    # Midcap F&O Stocks
    "ABFRL", "APLAPOLLO", "ASTRAL", "ATUL", "AUROPHARMA",
    "BALKRISIND", "BATAINDIA", "BEL", "BHARATFORG", "BHEL",
    "CANBK", "CANFINHOME", "CHAMBLFERT", "COFORGE", "CONCOR",
    "COROMANDEL", "CROMPTON", "CUB", "CUMMINSIND", "DEEPAKNTR",
    "DELTACORP", "DIXON", "ESCORTS", "EXIDEIND", "FEDERALBNK",
    "GMRINFRA", "GNFC", "GODREJPROP", "GRANULES", "GUJGASLTD",
    "HAL", "HDFCAMC", "HONAUT", "IDFCFIRSTB", "IEX",
    "IGL", "INDHOTEL", "INDIACEM", "INDIAMART", "INDUSTOWER",
    "INTELLECT", "JINDALSTEL", "JKCEMENT", "JUBLFOOD", "KEI",
    "L&TFH", "LALPATHLAB", "LAURUSLABS", "LTTS", "LUPIN",
    "MANAPPURAM", "MAXHEALTH", "MGL", "MINDTREE", "MFSL",
    "NAM-INDIA", "NATIONALUM", "NAUKRI", "NAVINFLUOR", "OBEROIRLTY",
    "OIL", "PAGEIND", "PETRONET", "PFIZER", "PHOENIXLTD",
    "POLYCAB", "PVRINOX", "RAMCOCEM", "RBLBANK", "SAIL",
    "SRF", "SRTRANSFIN", "STAR", "SUNTV", "SUPREMEIND",
    "TATACHEM", "TATACOMM", "TATAELXSI", "TORNTPHARM", "TORNTPOWER",
    "TTML", "UBL", "UPL", "VOLTAS", "WHIRLPOOL",
    "YESBANK", "ZEEL", "ZOMATO",
    
    # Additional F&O Stocks
    "AARTIIND", "ABB", "ABBOTINDIA", "ABCAPITAL", "AJANTPHARM",
    "ALKEM", "AMARAJABAT", "APOLLOTYRE", "ASHOKLEY", "ASIANPAINT",
    "BALRAMCHIN", "BANDHANBNK", "BANKBARODA", "BATAINDIA", "BERGEPAINT",
    "BHARATFORG", "BIOCON", "BOSCHLTD", "BSOFT", "CADILAHC",
    "CHAMBLFERT", "CHOLAFIN", "CIPLA", "CLEAN", "COALINDIA"
]

# ============================================================================
# CUSTOM STOCK LISTS (Choose what you want to monitor)
# ============================================================================

# Option 1: Top 20 Most Liquid F&O Stocks (Recommended for beginners)
TOP_20_LIQUID = [
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK",
    "HINDUNILVR", "ITC", "SBIN", "BHARTIARTL", "KOTAKBANK",
    "LT", "ASIANPAINT", "AXISBANK", "MARUTI", "TITAN",
    "BAJFINANCE", "ULTRACEMCO", "WIPRO", "NESTLEIND", "SUNPHARMA"
]

# Option 2: Nifty 50 Stocks Only
NIFTY_50_STOCKS = [
    "ADANIENT", "ADANIPORTS", "APOLLOHOSP", "ASIANPAINT", "AXISBANK",
    "BAJAJ-AUTO", "BAJFINANCE", "BAJAJFINSV", "BPCL", "BHARTIARTL",
    "BRITANNIA", "CIPLA", "COALINDIA", "DIVISLAB", "DRREDDY",
    "EICHERMOT", "GRASIM", "HCLTECH", "HDFCBANK", "HDFCLIFE",
    "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK", "ITC",
    "INDUSINDBK", "INFY", "JSWSTEEL", "KOTAKBANK", "LT",
    "M&M", "MARUTI", "NTPC", "NESTLEIND", "ONGC",
    "POWERGRID", "RELIANCE", "SBILIFE", "SHRIRAMFIN", "SBIN",
    "SUNPHARMA", "TCS", "TATACONSUM", "TATAMOTORS", "TATAPOWER",
    "TATASTEEL", "TECHM", "TITAN", "TMPV", "ULTRACEMCO", "WIPRO"
]

# Option 3: Bank Nifty Stocks
BANK_NIFTY_STOCKS = [
    "HDFCBANK", "ICICIBANK", "KOTAKBANK", "SBIN", "AXISBANK",
    "INDUSINDBK", "BANDHANBNK", "FEDERALBNK", "IDFCFIRSTB", "PNB",
    "BANKBARODA", "AUBANK"
]

# Option 4: Sector-wise Lists

# Banking & Financial
BANKING_STOCKS = [
    "HDFCBANK", "ICICIBANK", "KOTAKBANK", "SBIN", "AXISBANK",
    "INDUSINDBK", "BANDHANBNK", "FEDERALBNK", "IDFCFIRSTB", "PNB",
    "BANKBARODA", "BAJFINANCE", "BAJAJFINSV", "CHOLAFIN", "SBICARD",
    "HDFCLIFE", "SBILIFE", "ICICIGI", "ICICIPRULI"
]

# IT Sector
IT_STOCKS = [
    "TCS", "INFY", "WIPRO", "HCLTECH", "TECHM",
    "LTIM", "PERSISTENT", "COFORGE", "MPHASIS", "LTTS"
]

# Auto Sector
AUTO_STOCKS = [
    "MARUTI", "TATAMOTORS", "M&M", "BAJAJ-AUTO", "EICHERMOT",
    "HEROMOTOCO", "TVSMOTOR", "ESCORTS", "ASHOKLEY", "MOTHERSON",
    "APOLLOTYRE", "MRF", "BHARATFORG"
]

# FMCG Sector
FMCG_STOCKS = [
    "HINDUNILVR", "ITC", "NESTLEIND", "BRITANNIA", "DABUR",
    "MARICO", "GODREJCP", "TATACONSUM", "COLPAL", "UBL",
    "MCDOWELL-N", "PGHH"
]

# Pharma Sector
PHARMA_STOCKS = [
    "SUNPHARMA", "DRREDDY", "CIPLA", "DIVISLAB", "LUPIN",
    "AUROPHARMA", "BIOCON", "TORNTPHARM", "ALKEM", "LAURUSLABS",
    "ABBOTINDIA", "GRANULES"
]

# Metals & Mining
METALS_STOCKS = [
    "TATASTEEL", "JSWSTEEL", "HINDALCO", "COALINDIA", "VEDL",
    "NATIONALUM", "NMDC", "JINDALSTEL", "SAIL", "HINDZINC"
]

# Energy & Power
ENERGY_STOCKS = [
    "RELIANCE", "ONGC", "BPCL", "IOC", "HINDPETRO",
    "NTPC", "POWERGRID", "TATAPOWER", "ADANIGREEN", "ADANIPORTS",
    "GAIL", "IGL", "MGL", "PETRONET"
]

# Infrastructure & Realty
INFRA_STOCKS = [
    "LT", "DLF", "OBEROIRLTY", "GODREJPROP", "PRESTIGE",
    "PHOENIXLTD", "BRIGADE"
]

# Cement
CEMENT_STOCKS = [
    "ULTRACEMCO", "AMBUJACEM", "ACC", "SHREECEM", "RAMCOCEM",
    "JKCEMENT", "INDIACEM"
]

# ============================================================================
# ACTIVE STOCK LIST (This is what the strategy will monitor)
# CHOOSE ONE OF THE LISTS ABOVE
# ============================================================================

# RECOMMENDED: Start with Top 20 for better performance
STOCK_LIST = NIFTY_50_STOCKS

# Or use ALL F&O stocks (may be slow with 165+ stocks)
# STOCK_LIST = ALL_FNO_STOCKS

# Or use Nifty 50 only
# STOCK_LIST = NIFTY_50_STOCKS

# Or combine multiple sectors
# STOCK_LIST = BANKING_STOCKS + IT_STOCKS + AUTO_STOCKS

# Or create your own custom list
# STOCK_LIST = [
#     "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK",
#     "Add your favorite stocks here..."
# ]

# ============================================================================
# TRADING CONFIGURATION
# ============================================================================

TRADING_CONFIG = {
    # Timeframe in minutes
    "TIMEFRAME": 3,
    
    # Time to check conditions (9:18:10 AM)
    "SCAN_TIME": {
        "HOUR": 9,
        "MINUTE": 18,
        "SECOND": 10
    },
    
    # PnL monitoring interval in seconds (60 = 1 minute)
    "MONITOR_INTERVAL": 1,
    
    # Strike price difference (depends on stock)
    # Most stocks: 50, Bank Nifty: 100, Nifty: 50
    "STRIKE_DIFFERENCE": 50,
    
    # Trading hours
    "MARKET_OPEN": "09:15:00",
    "MARKET_CLOSE": "15:30:00",
    
    # Virtual Trading Mode (Paper Trading)
    # If True, no orders will be actually placed in Fyers
    "VIRTUAL_TRADING": True
}

# ============================================================================
# RISK MANAGEMENT (Optional - for future implementation)
# ============================================================================

RISK_CONFIG = {
    "MAX_LOSS_PER_TRADE": -500,     # Maximum loss per trade in rupees
    "MAX_LOSS_PERCENT": -10,         # Maximum loss percentage
    "TARGET_PROFIT": 1000,           # Target profit in rupees
    "TARGET_PROFIT_PERCENT": 20,     # Target profit percentage
    "TRAILING_STOP_LOSS": True,      # Enable trailing stop loss
    "TRAILING_SL_PERCENT": 5,        # Trailing stop loss percentage
    "MAX_POSITIONS": 10              # Maximum concurrent positions
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOGGING_CONFIG = {
    "ENABLE_LOGGING": True,
    "LOG_FILE": "trading_logs.txt",
    "LOG_LEVEL": "INFO"  # DEBUG, INFO, WARNING, ERROR
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_stock_count():
    """Get number of stocks being monitored"""
    return len(STOCK_LIST)

def get_sector_stocks(sector):
    """Get stocks from a specific sector"""
    sectors = {
        'banking': BANKING_STOCKS,
        'it': IT_STOCKS,
        'auto': AUTO_STOCKS,
        'fmcg': FMCG_STOCKS,
        'pharma': PHARMA_STOCKS,
        'metals': METALS_STOCKS,
        'energy': ENERGY_STOCKS,
        'infra': INFRA_STOCKS,
        'cement': CEMENT_STOCKS
    }
    return sectors.get(sector.lower(), [])

def get_all_sectors():
    """Get list of all available sectors"""
    return ['banking', 'it', 'auto', 'fmcg', 'pharma', 'metals', 'energy', 'infra', 'cement']

# ============================================================================
# PRINT CONFIGURATION (for verification)
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("FnO Trading Configuration")
    print("="*70)
    print(f"\nActive Stock List: {len(STOCK_LIST)} stocks")
    print(f"Timeframe: {TRADING_CONFIG['TIMEFRAME']} minutes")
    print(f"Scan Time: {TRADING_CONFIG['SCAN_TIME']['HOUR']}:{TRADING_CONFIG['SCAN_TIME']['MINUTE']:02d}")
    print(f"Monitor Interval: {TRADING_CONFIG['MONITOR_INTERVAL']} seconds")
    print("\nMonitoring these stocks:")
    for i, stock in enumerate(STOCK_LIST, 1):
        print(f"  {i}. {stock}", end="")
        if i % 5 == 0:
            print()  # New line every 5 stocks
    print("\n" + "="*70 + "\n")
