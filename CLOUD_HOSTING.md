# 🌐 Free Cloud Hosting Guide for FnO Dashboard

## Access Dashboard from Anywhere (Internet)

There are several free options to host your trading dashboard online:

---

## 🚀 **OPTION 1: Render.com (Recommended - Easiest)**

### ✅ Pros:
- Completely free
- No credit card required
- Automatic HTTPS
- Easy deployment from GitHub
- Stays online 24/7
- Access from anywhere

### 📋 Setup Steps:

#### Step 1: Prepare Your Code

Create a new file called `Procfile` (no extension):

```
web: gunicorn app:app
```

Update `requirements.txt` to include gunicorn:

```
fyers-apiv3
pandas
numpy
requests
python-dateutil
flask
flask-cors
gunicorn
```

#### Step 2: Create GitHub Repository

```bash
cd ~/fno-trading

# Initialize git
git init

# Create .gitignore
echo "access_token.txt
*.pyc
__pycache__/
.env" > .gitignore

# Add files
git add .
git commit -m "Initial commit"

# Create repo on GitHub (github.com)
# Then push:
git remote add origin https://github.com/YOUR_USERNAME/fno-trading.git
git push -u origin main
```

#### Step 3: Deploy on Render

1. **Go to:** https://render.com
2. **Sign up** (free, use GitHub login)
3. **Click:** "New +" → "Web Service"
4. **Connect** your GitHub repository
5. **Configure:**
   - Name: `fno-trading-dashboard`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Instance Type: `Free`

6. **Add Environment Variables:**
   - Click "Environment" tab
   - Add:
     ```
     CLIENT_ID = your_fyers_client_id
     SECRET_KEY = your_fyers_secret_key
     ACCESS_TOKEN = your_access_token
     ```

7. **Deploy!**

#### Step 4: Update Code for Environment Variables

Modify `config.py`:

```python
import os

FYERS_CONFIG = {
    "CLIENT_ID": os.environ.get("CLIENT_ID", "YOUR_CLIENT_ID_HERE"),
    "SECRET_KEY": os.environ.get("SECRET_KEY", "YOUR_SECRET_KEY_HERE"),
    "ACCESS_TOKEN": os.environ.get("ACCESS_TOKEN", "YOUR_ACCESS_TOKEN_HERE")
}
```

#### Step 5: Access Your Dashboard

Your dashboard will be at:
```
https://fno-trading-dashboard.onrender.com
```

**⚠️ Important:** Render free tier sleeps after 15 mins of inactivity. First request takes ~30 seconds to wake up.

---

## 🚀 **OPTION 2: Railway.app (Better Performance)**

### ✅ Pros:
- Free $5/month credit
- Faster than Render
- No sleep on inactivity
- Easy deployment

### 📋 Setup Steps:

1. **Go to:** https://railway.app
2. **Sign up** with GitHub
3. **New Project** → "Deploy from GitHub repo"
4. **Select** your fno-trading repository
5. **Add Variables:**
   - CLIENT_ID
   - SECRET_KEY
   - ACCESS_TOKEN
6. **Deploy!**

Your URL: `https://fno-trading.up.railway.app`

---

## 🚀 **OPTION 3: PythonAnywhere (24/7 Free)**

### ✅ Pros:
- Always on (no sleep)
- Free forever tier
- Terminal access
- Good for trading apps

### ⚠️ Cons:
- More complex setup
- Limited to PythonAnywhere domain

### 📋 Setup Steps:

1. **Sign up:** https://www.pythonanywhere.com
2. **Upload files** via Files tab
3. **Open Bash console:**
   ```bash
   cd ~
   git clone https://github.com/YOUR_USERNAME/fno-trading.git
   cd fno-trading
   pip3 install --user -r requirements.txt
   ```

4. **Web tab** → "Add a new web app"
   - Python version: 3.10
   - Framework: Flask
   - Source code: `/home/yourusername/fno-trading`
   - WSGI file: Point to `app.py`

5. **Configure WSGI file:**
   ```python
   import sys
   path = '/home/yourusername/fno-trading'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

6. **Set environment variables** in Web tab

Your URL: `https://yourusername.pythonanywhere.com`

---

## 🚀 **OPTION 4: Ngrok (Temporary - Best for Testing)**

### ✅ Pros:
- Instant setup (2 minutes)
- No code changes
- Perfect for testing
- Works with your MacBook

### ⚠️ Cons:
- MacBook must be running
- URL changes each time (free tier)
- Not permanent solution

### 📋 Setup Steps:

#### Step 1: Install Ngrok

```bash
# On MacBook M4
brew install ngrok

# Or download from: https://ngrok.com/download
```

#### Step 2: Sign Up (Free)

1. Go to: https://ngrok.com
2. Sign up (free)
3. Get your auth token
4. Run: `ngrok config add-authtoken YOUR_TOKEN`

#### Step 3: Start Your Server

```bash
# Terminal 1: Start Flask server
cd ~/fno-trading
python3 app.py
```

#### Step 4: Create Tunnel

```bash
# Terminal 2: Create ngrok tunnel
ngrok http 5000
```

You'll see:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:5000
```

#### Step 5: Access Anywhere!

Open on your phone or any device:
```
https://abc123.ngrok.io
```

**Perfect for:** Testing, showing to friends, temporary access

---

## 🔒 **OPTION 5: Cloudflare Tunnel (Free & Secure)**

### ✅ Pros:
- Completely free
- Custom domain support
- DDoS protection
- Always HTTPS

### 📋 Quick Setup:

```bash
# Install cloudflared
brew install cloudflare/cloudflare/cloudflared

# Login
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create fno-trading

# Run tunnel
cloudflared tunnel --url http://localhost:5000
```

Get permanent URL:
```bash
cloudflared tunnel route dns fno-trading fno.yourdomain.com
```

---

## 📊 **Comparison Table**

| Platform | Free Tier | Always On | Setup Time | Best For |
|----------|-----------|-----------|------------|----------|
| **Render** | ✅ Yes | ⚠️ Sleeps | 10 min | Production |
| **Railway** | ✅ $5/mo | ✅ Yes | 5 min | Best balance |
| **PythonAnywhere** | ✅ Yes | ✅ Yes | 20 min | 24/7 trading |
| **Ngrok** | ✅ Yes | ⚠️ Need Mac | 2 min | Testing |
| **Cloudflare** | ✅ Yes | ⚠️ Need Mac | 15 min | Security |

---

## 🎯 **RECOMMENDED APPROACH**

### For Daily Trading (Best Option):

**Use PythonAnywhere or Railway:**

1. **Deploy once** to cloud
2. **Keep it running** 24/7
3. **Generate token daily** via API or web interface
4. **Access dashboard** from anywhere

### For Testing/Development:

**Use Ngrok:**
1. Quick setup
2. Test from phone
3. No cloud deployment needed

---

## 🔐 **Security Considerations**

### When Hosting Online:

1. **Add Authentication:**

Create `auth.py`:
```python
from functools import wraps
from flask import request, jsonify

USERNAME = "your_username"
PASSWORD = "your_password"

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != USERNAME or auth.password != PASSWORD:
            return jsonify({'message': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated
```

Update `app.py`:
```python
from auth import require_auth

@app.route('/')
@require_auth
def index():
    return render_template('dashboard.html')
```

2. **Use Environment Variables:**
   - Never commit credentials to GitHub
   - Use `.env` file locally
   - Set env vars in cloud platform

3. **Add IP Whitelist (Optional):**
```python
ALLOWED_IPS = ['YOUR_HOME_IP', 'YOUR_PHONE_IP']

@app.before_request
def limit_remote_addr():
    if request.remote_addr not in ALLOWED_IPS:
        abort(403)
```

---

## 🚀 **EASIEST PATH: Step-by-Step**

### Complete Setup in 15 Minutes:

```bash
# 1. Install ngrok
brew install ngrok

# 2. Sign up at ngrok.com and get auth token
ngrok config add-authtoken YOUR_TOKEN

# 3. Start your server
cd ~/fno-trading
python3 app.py

# 4. In new terminal, create tunnel
ngrok http 5000

# 5. Copy the https URL shown
# Example: https://abc123.ngrok.io

# 6. Open on your phone or anywhere!
```

**Now you can access from:**
- ✅ Your phone (anywhere)
- ✅ Office computer
- ✅ Friend's device
- ✅ Any internet connection

---

## 📱 **Access Token Management for Cloud**

### Problem: Token expires every 24 hours

### Solution 1: Auto-Refresh Script

Create `refresh_token.py`:
```python
from fyers_auth_improved import FyersAuth
import schedule
import time

def refresh_token():
    print("Refreshing token...")
    auth = FyersAuth()
    # Add auto-refresh logic here

# Run every 23 hours
schedule.every(23).hours.do(refresh_token)

while True:
    schedule.run_pending()
    time.sleep(3600)  # Check every hour
```

### Solution 2: Manual Daily Refresh

```bash
# Every morning before trading
python3 fyers_auth_improved.py
```

### Solution 3: API Endpoint for Token Refresh

Add to `app.py`:
```python
@app.route('/refresh-token')
def refresh_token_page():
    return render_template('refresh_token.html')
```

Create a simple page to generate token via web interface!

---

## 💡 **Best Practice Workflow**

### Daily Morning Routine:

1. **Open dashboard** (from anywhere)
2. **Generate token** (via web or script)
3. **Start strategy**
4. **Monitor on phone**
5. **Stop after market close**

### Setup Once, Use Forever!

---

## 🎯 **My Recommendation**

**For you specifically:**

1. **Now (Testing):** Use **Ngrok**
   - 2-minute setup
   - Access from Samsung S10 anywhere
   - Keep MacBook running at home

2. **Later (Production):** Deploy to **PythonAnywhere**
   - 24/7 availability
   - No need to keep MacBook on
   - Professional setup

3. **Token Management:** Use **fyers_auth_improved.py**
   - Hardcoded credentials
   - One-command token generation
   - Auto-updates config

---

Would you like me to:
1. Create the files for a specific hosting option?
2. Add authentication to the dashboard?
3. Create a web-based token refresh page?
4. Set up automatic token renewal?

Let me know which option you prefer! 🚀
