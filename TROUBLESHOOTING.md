# 🔧 TROUBLESHOOTING: Internal Server Error

## Quick Fix Steps

### Step 1: Run Diagnostic Script

```bash
cd ~/fno-trading
python3 diagnose.py
```

This will tell you exactly what's wrong!

---

## Common Issues & Solutions

### Issue 1: Missing Dependencies

**Error:** Import errors or module not found

**Solution:**
```bash
pip3 install flask flask-cors fyers-apiv3 pandas numpy
```

Or:
```bash
pip3 install -r requirements.txt
```

---

### Issue 2: Templates Folder Missing

**Error:** "TemplateNotFound: dashboard.html"

**Solution:**
```bash
# Make sure you have this structure:
fno-trading/
  ├── app.py
  ├── templates/
  │   └── dashboard.html
  └── ...other files...

# If templates folder is missing, create it:
mkdir templates

# Then copy dashboard.html into templates/
```

---

### Issue 3: Config Import Error

**Error:** Cannot import from config

**Solution:**

Make sure `config.py` exists and has proper syntax:

```python
# Minimal config.py for testing
FYERS_CONFIG = {
    "CLIENT_ID": "YOUR_CLIENT_ID_HERE",
    "ACCESS_TOKEN": "YOUR_ACCESS_TOKEN_HERE"
}

STOCK_LIST = [
    "SBIN",
    "RELIANCE",
    "TCS"
]

TRADING_CONFIG = {
    "TIMEFRAME": 3,
    "SCAN_TIME": {
        "HOUR": 9,
        "MINUTE": 18,
        "SECOND": 10
    },
    "MONITOR_INTERVAL": 60
}
```

---

### Issue 4: Use the Fixed App

**If app.py has issues, use the fixed version:**

```bash
# Rename current app.py
mv app.py app_old.py

# Use fixed version
mv app_fixed.py app.py

# Or directly:
python3 app_fixed.py
```

---

## Check Server Logs

When you run the server, watch for error messages:

```bash
python3 app.py
```

**Look for errors like:**
- ❌ `ImportError: No module named 'flask'`
- ❌ `ModuleNotFoundError: No module named 'config'`
- ❌ `TemplateNotFound: dashboard.html`
- ❌ `SyntaxError in config.py`

---

## Test Step-by-Step

### Test 1: Can Python find Flask?

```bash
python3 -c "import flask; print('Flask OK')"
```

Should print: `Flask OK`

If not:
```bash
pip3 install flask flask-cors
```

---

### Test 2: Can Python import config?

```bash
python3 -c "from config import FYERS_CONFIG; print('Config OK')"
```

Should print: `Config OK`

If not: Check config.py syntax

---

### Test 3: Does templates folder exist?

```bash
ls -la templates/dashboard.html
```

Should show the file

If not:
```bash
mkdir templates
# Copy dashboard.html to templates/
```

---

### Test 4: Run minimal server

Create `test_server.py`:

```python
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'status': 'ok', 'message': 'Server is working!'})

if __name__ == '__main__':
    print("Test server starting on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000)
```

Run it:
```bash
python3 test_server.py
```

Open browser: http://localhost:5000

Should see: `{"message": "Server is working!", "status": "ok"}`

---

## Complete Fresh Install

If nothing works, start fresh:

```bash
# 1. Create new directory
mkdir ~/fno-trading-fresh
cd ~/fno-trading-fresh

# 2. Copy all files here
# (Copy from your downloaded files)

# 3. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux

# 4. Install dependencies
pip install flask flask-cors fyers-apiv3 pandas numpy requests python-dateutil

# 5. Verify structure
ls -la
# Should see:
# app.py
# config.py
# fno_trading_strategy.py
# requirements.txt
# templates/
#   dashboard.html

# 6. Run diagnostic
python3 diagnose.py

# 7. Start server
python3 app.py
```

---

## Get Detailed Error Info

Run with debug mode to see full error:

```bash
python3 app.py
```

Or check the terminal where server is running - it will show the full error stack trace.

**Copy the error message** and look for:
- File names (what file has the error)
- Line numbers
- Error type (ImportError, SyntaxError, etc.)

---

## Quick Checklist

Before running server, verify:

- [ ] ✅ Python 3.7+ installed
- [ ] ✅ Flask installed (`pip3 install flask`)
- [ ] ✅ Flask-CORS installed (`pip3 install flask-cors`)
- [ ] ✅ All .py files in same directory
- [ ] ✅ templates/ folder exists
- [ ] ✅ dashboard.html inside templates/
- [ ] ✅ config.py has valid syntax
- [ ] ✅ No syntax errors in any .py file

---

## Still Not Working?

**Share this info for help:**

1. Run diagnostic:
```bash
python3 diagnose.py > diagnostic_output.txt
```

2. Try to start server and copy the error:
```bash
python3 app.py 2>&1 | tee server_error.txt
```

3. Check Python version:
```bash
python3 --version
```

4. Check installed packages:
```bash
pip3 list | grep -E '(flask|fyers|pandas)'
```

---

## Emergency: Minimal Working Server

If you just want to test the dashboard UI without strategy:

Create `simple_app.py`:

```python
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'idle',
        'current_time': datetime.now().strftime('%H:%M:%S'),
        'market_status': 'closed',
        'qualified_stocks': {},
        'total_pnl': 0,
        'total_pnl_percent': 0,
        'last_update': datetime.now().isoformat()
    })

@app.route('/api/config')
def config():
    return jsonify({
        'timeframe': 3,
        'scan_time': '09:18:10',
        'stock_count': 10,
        'monitor_interval': 60
    })

if __name__ == '__main__':
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    
    print(f"\nDashboard: http://{ip}:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
```

Run:
```bash
python3 simple_app.py
```

This should at least show you the dashboard UI!

---

**Need more help? Run `python3 diagnose.py` and share the output!**
