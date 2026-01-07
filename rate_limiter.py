"""
Rate Limiter for Fyers API
Manages API call limits: 10/sec, 200/min, 100,000/day
"""

import time
from datetime import datetime, timedelta
from collections import deque
import threading

class FyersRateLimiter:
    """
    Rate limiter to ensure Fyers API limits are not exceeded
    Limits:
    - 10 calls per second
    - 200 calls per minute
    - 100,000 calls per day
    """
    
    def __init__(self):
        self.lock = threading.Lock()
        
        # Track API calls with timestamps (maxlen adjusted to limits)
        self.calls_per_second = deque(maxlen=8)
        self.calls_per_minute = deque(maxlen=180)
        self.calls_per_day = deque(maxlen=90000)
        
        # Limits (Adjusted as per user request)
        self.LIMIT_PER_SECOND = 8
        self.LIMIT_PER_MINUTE = 180
        self.LIMIT_PER_DAY = 90000
        
        # Statistics
        self.total_calls_today = 0
        self.last_reset = datetime.now().date()
        
    def _clean_old_calls(self):
        """Remove old timestamps that are outside the time windows"""
        now = time.time()
        
        # Clean calls older than 1 second
        while self.calls_per_second and now - self.calls_per_second[0] > 1:
            self.calls_per_second.popleft()
        
        # Clean calls older than 1 minute
        while self.calls_per_minute and now - self.calls_per_minute[0] > 60:
            self.calls_per_minute.popleft()
        
        # Clean calls older than 1 day
        while self.calls_per_day and now - self.calls_per_day[0] > 86400:
            self.calls_per_day.popleft()
    
    def _reset_daily_counter(self):
        """Reset daily counter if it's a new day"""
        today = datetime.now().date()
        if today > self.last_reset:
            self.calls_per_day.clear()
            self.total_calls_today = 0
            self.last_reset = today
    
    def can_make_call(self):
        """
        Check if a call can be made without exceeding limits
        
        Returns:
            bool: True if call can be made, False otherwise
        """
        with self.lock:
            self._clean_old_calls()
            self._reset_daily_counter()
            
            # Check all limits
            if len(self.calls_per_second) >= self.LIMIT_PER_SECOND:
                return False
            if len(self.calls_per_minute) >= self.LIMIT_PER_MINUTE:
                return False
            if len(self.calls_per_day) >= self.LIMIT_PER_DAY:
                return False
            
            return True
    
    def wait_if_needed(self):
        """
        Wait until a call can be made without exceeding limits
        Blocks until rate limit allows
        """
        while not self.can_make_call():
            time.sleep(0.1)  # Wait 100ms before checking again
    
    def record_call(self):
        """Record that an API call was made"""
        with self.lock:
            now = time.time()
            self.calls_per_second.append(now)
            self.calls_per_minute.append(now)
            self.calls_per_day.append(now)
            self.total_calls_today += 1
    
    def make_call(self, api_function, *args, **kwargs):
        """
        Execute an API call with rate limiting
        
        Args:
            api_function: The API function to call
            *args, **kwargs: Arguments to pass to the function
            
        Returns:
            Result of the API call
        """
        self.wait_if_needed()
        self.record_call()
        return api_function(*args, **kwargs)
    
    def get_stats(self):
        """
        Get current API usage statistics
        
        Returns:
            dict: Statistics about API usage
        """
        with self.lock:
            self._clean_old_calls()
            self._reset_daily_counter()
            
            return {
                'calls_last_second': len(self.calls_per_second),
                'calls_last_minute': len(self.calls_per_minute),
                'calls_today': len(self.calls_per_day),
                'limit_per_second': self.LIMIT_PER_SECOND,
                'limit_per_minute': self.LIMIT_PER_MINUTE,
                'limit_per_day': self.LIMIT_PER_DAY,
                'remaining_second': self.LIMIT_PER_SECOND - len(self.calls_per_second),
                'remaining_minute': self.LIMIT_PER_MINUTE - len(self.calls_per_minute),
                'remaining_day': self.LIMIT_PER_DAY - len(self.calls_per_day),
                'percent_used_second': (len(self.calls_per_second) / self.LIMIT_PER_SECOND) * 100,
                'percent_used_minute': (len(self.calls_per_minute) / self.LIMIT_PER_MINUTE) * 100,
                'percent_used_day': (len(self.calls_per_day) / self.LIMIT_PER_DAY) * 100,
                'last_reset': self.last_reset.isoformat()
            }
    
    def get_wait_time(self):
        """
        Calculate how long to wait before next call can be made
        
        Returns:
            float: Wait time in seconds (0 if can call now)
        """
        with self.lock:
            self._clean_old_calls()
            
            wait_times = []
            
            # Check second limit
            if len(self.calls_per_second) >= self.LIMIT_PER_SECOND:
                oldest = self.calls_per_second[0]
                wait_times.append(1 - (time.time() - oldest))
            
            # Check minute limit
            if len(self.calls_per_minute) >= self.LIMIT_PER_MINUTE:
                oldest = self.calls_per_minute[0]
                wait_times.append(60 - (time.time() - oldest))
            
            # Check day limit
            if len(self.calls_per_day) >= self.LIMIT_PER_DAY:
                oldest = self.calls_per_day[0]
                wait_times.append(86400 - (time.time() - oldest))
            
            return max(wait_times) if wait_times else 0


class BatchAPIManager:
    """
    Manages batch API calls efficiently to minimize API usage
    """
    
    def __init__(self, rate_limiter):
        self.rate_limiter = rate_limiter
        self.cache = {}
        self.cache_duration = 5  # Cache for 5 seconds
    
    def get_with_cache(self, key, fetch_function, *args, **kwargs):
        """
        Get data with caching to reduce API calls
        
        Args:
            key: Cache key
            fetch_function: Function to fetch data if not cached
            *args, **kwargs: Arguments for fetch function
            
        Returns:
            Cached or fresh data
        """
        now = time.time()
        
        # Check cache
        if key in self.cache:
            cached_data, timestamp = self.cache[key]
            if now - timestamp < self.cache_duration:
                return cached_data
        
        # Fetch fresh data
        data = self.rate_limiter.make_call(fetch_function, *args, **kwargs)
        self.cache[key] = (data, now)
        return data
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()
    
    def batch_get_quotes(self, fyers_client, symbols):
        """
        Get quotes for multiple symbols in batches
        Fyers allows up to 50 symbols per request
        
        Args:
            fyers_client: Fyers API client
            symbols: List of symbols
            
        Returns:
            dict: Symbol -> quote data
        """
        quotes = {}
        batch_size = 50  # Fyers max symbols per request
        
        for i in range(0, len(symbols), batch_size):
            batch = symbols[i:i + batch_size]
            symbols_str = ",".join(batch)
            
            try:
                response = self.rate_limiter.make_call(
                    fyers_client.quotes,
                    {"symbols": symbols_str}
                )
                
                if response.get('s') == 'ok' and 'd' in response:
                    for quote_data in response['d']:
                        symbol = quote_data['n']
                        quotes[symbol] = quote_data['v']
                
                # Small delay between batches
                time.sleep(0.2)
                
            except Exception as e:
                print(f"Error fetching batch quotes: {e}")
        
        return quotes


# Global rate limiter instance
global_rate_limiter = FyersRateLimiter()
global_batch_manager = BatchAPIManager(global_rate_limiter)


def get_rate_limiter():
    """Get the global rate limiter instance"""
    return global_rate_limiter


def get_batch_manager():
    """Get the global batch manager instance"""
    return global_batch_manager
