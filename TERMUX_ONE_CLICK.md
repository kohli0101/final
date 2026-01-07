# 📱 One-Click Termux Setup Guide

This guide will turn your Samsung S24 into a powerful trading server that you can launch with a single tap from your home screen.

---

## 🛑 Step 1: Install the Right Apps
Do **NOT** use the Play Store version of Termux (it is outdated).

1.  Download **F-Droid** (an app store for open source apps): [https://f-droid.org/](https://f-droid.org/)
2.  Open F-Droid and search for/install **Termux**.
3.  Search for/install **Termux:Widget**.
4.  Open the **Termux** app once to initialize it.

---

## ⚙️ Step 2: Setup Python Environment
Copy and paste this entire block into your Termux app and hit Enter (this takes ~5 minutes):

```bash
# Update system
pkg update -y && pkg upgrade -y

# Install Python and Git
pkg install python git -y

# Install Trading Dependencies (Pandas works natively here!)
pip install pandas numpy fyers-apiv3 flask flask-cors requests python-dateutil webcolors

# Setup Widget Folder
mkdir -p ~/.shortcuts
```

---

## 📥 Step 3: Get Your Code
Run these commands in Termux to download your bot:

```bash
# Clone your repository
git clone https://github.com/kohli0101/final.git

# Copy the launch script to the shortcuts folder
cp ~/final/launch_bot.sh ~/.shortcuts/
chmod +x ~/.shortcuts/launch_bot.sh
```

---

## 👆 Step 4: Add the Widget
1.  Go to your Samsung S24 **Home Screen**.
2.  Long press on an empty space -> **Widgets**.
3.  Scroll down to **Termux:Widget**.
4.  Drag the **"Single Shortcut"** (or just "Termux Widget") to your home screen.
5.  A menu will pop up. Select **`launch_bot.sh`**.

---

## ✅ How to Use
1.  **Tap the Icon** on your home screen.
2.  Termux will open in the background.
3.  **Safari/Chrome will automatically open** to your dashboard (`http://localhost:5000`).
4.  **Done!** Your bot is running natively on your phone's processor. 🚀
