# 📱 Mobile Dashboard Setup Guide

## Complete Setup for Samsung S10

---

## 🎯 What You'll Need

1. **Computer** (Windows/Mac/Linux) - to run the server
2. **Samsung S10** (or any Android phone)
3. **Both devices on the same WiFi network**
4. **Python 3.8+** installed on computer

---

## 📦 Installation Steps

### Step 1: Install Python Packages

```bash
pip install -r requirements.txt
```

### Step 2: Configure Fyers API

1. **Generate Access Token:**
   ```bash
   python fyers_auth.py
   ```

2. **Update config.py** with your credentials

### Step 3: Find Your Computer's IP

**Windows:**
```bash
ipconfig
```

**Mac/Linux:**
```bash
ifconfig
```

Example: `192.168.1.100`

---

## 🚀 Running the Dashboard

### Start Server:
```bash
python app.py
```

### Access from Phone:
Open Chrome and go to: `http://YOUR_IP:5000`

Example: `http://192.168.1.100:5000`

---

## 📱 Dashboard Features

- **Live Updates** - Every 5 seconds
- **Market Status** - Open/Closed indicator
- **P&L Tracking** - Real-time profit/loss
- **Active Positions** - All qualified stocks
- **Touch Optimized** - Perfect for mobile

---

## 🎮 Usage

1. Click **START** before 9:15 AM
2. Strategy scans at 9:18:10 AM
3. Monitors qualified stocks automatically
4. Real-time P&L updates
5. Click **STOP** to end session

---

## 💡 Tips

### Phone Settings:
- Keep screen on while charging
- Disable battery saver
- Use Chrome browser
- Add to home screen

### Network:
- Both devices same WiFi
- Use 5GHz for better performance
- Allow port 5000 in firewall

---

## 🔧 Troubleshooting

**Can't connect?**
- Check both on same WiFi
- Verify IP address
- Check firewall settings

**Strategy not starting?**
- Regenerate access token
- Check credentials in config.py

**No updates?**
- Refresh page
- Check server is running
- Verify WiFi connection

---

## 📊 Strategy Logic

**Entry Conditions at 9:18:10 AM:**
1. First candle Open == Low
2. Open < Previous Day High
3. Close > Previous Day High

When met → Track ATM CE option P&L

---

## ⚠️ Important

- Access tokens expire in 24 hours
- Generate new token daily
- Test before live trading
- Practice risk management

---

**Happy Trading! 📈**
