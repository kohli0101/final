# Hosting Guide: FnO Trading Bot

Based on the analysis of your "final" folder, here are the best ways to host this application for free, ensuring it remains active during market hours.

## Project Requirements
- **Language**: Python 3.9+
- **Memory**: ~512MB - 1GB RAM (Mostly for `pandas`)
- **Storage**: ~100MB (including symbols CSV)
- **Uptime**: Critical between **9:00 AM - 4:00 PM IST**.

---

## 1. Cloud Hosting (Recommended: Oracle Cloud)

### A. Oracle Cloud "Always Free" (Best Overall)
Oracle offers the most generous free tier in the industry.
- **Specs**: 4 ARM vCPUs and **24GB RAM**.
- **Pros**: Forever free, extremely powerful, 24/7 uptime.
- **Setup**:
    1. Sign up for Oracle Cloud.
    2. Create a "Compute Instance" using **Ubuntu 22.04 (ARM)**.
    3. Install Python and clone your code.
    4. Use `tmux` or `pm2` to keep the bot running after you logout.

### B. Google Cloud Platform (GCP)
- **Specs**: E2-micro instance (2 vCPUs, 1GB RAM).
- **Pros**: Always free (in `us-west1`, `us-central1` regions).
- **Setup**: Similar to Oracle, but with less RAM.

### C. Why NOT to use Render/Vercel/Heroku
- **Render**: Free tier puts the app to "sleep" after 15 mins of inactivity. Your strategy thread will stop.
- **Railway/Fly.io**: Limited free credits that will run out if running 24/7.

---

## 2. Low-Powered Device (Local Hosting)

### A. Raspberry Pi / Orange Pi
- A Raspberry Pi 3 or 4 is perfect.
- **Setup**: Install "Raspberry Pi OS Lite" (no GUI) to save RAM.
- **Energy Cost**: ~$5 per year in electricity (very low).

### B. Old Android Phone (via Termux)
If you have an old Android phone lying around:
1. Install **Termux** from F-Droid.
2. Run `pkg install python` and `pkg install tur-repo`.
3. Install dependencies using `pip install -r requirements.txt`.
4. Keep the phone plugged into a charger.

---

## 3. How to keep it running 24/7

To ensure the bot doesn't stop when you close your terminal, use **PM2** (Process Manager).

### Installation (Linux/Mac)
```bash
sudo apt update && sudo apt install nodejs npm -y
sudo npm install pm2 -g
```

### Starting your App
```bash
pm2 start app.py --name "trading-bot" --interpreter python3
```

### Auto-start on reboot
```bash
pm2 save
pm2 startup
```

---

## 4. Security Checklist for Web Access
1. **Firewall**: Ensure port `5000` is open in your cloud provider's dashboard (Security Lists/VPC).
2. **Access Token**: Your `access_token.txt` and `config.py` contain sensitive data. **Do not** upload them to public GitHub repositories. Use a `.gitignore` file.
3. **Redirect URI**: If hosting on cloud, update your Fyers App settings to use your server's Public IP instead of `127.0.0.1`.
