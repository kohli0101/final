# 📱 Standalone Android App Guide (Samsung S24)

This guide will help you turn your trading dashboard into a standalone app on your Samsung S24.

---

## 🚀 Step 1: Run the Server on your S24

To make the app truly standalone, you can run the entire Python backend directly on your Samsung S24 using **Termux**.

1. **Install Termux** from [F-Droid](https://f-droid.org/en/packages/com.termux/) (do not use the Play Store version).
2. **Setup Environment**:
   Open Termux and run:
   ```bash
   pkg update && pkg upgrade
   pkg install python python-pip git -y
   ```
3. **Copy Files**:
   Transfer your project folder to your phone or clone it via git.
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Start the Server**:
   ```bash
   python app.py
   ```
   *The server will now be running on `http://localhost:5000` on your phone.*

---

## 📲 Step 2: Install the App on Home Screen

Once the server is running (either on your computer or on the phone itself):

1. **Open Google Chrome** on your Samsung S24.
2. **Navigate to the dashboard**:
   - If running on phone: `http://localhost:5000`
   - If running on computer: `http://YOUR_COMPUTER_IP:5000`
3. **Install App**:
   - Tap the **three dots (⋮)** in the top right corner.
   - Select **"Install app"** or **"Add to Home screen"**.
   - A popup will appear with the logo I generated. Tap **"Install"**.
4. **Standalone Mode**:
   Go to your home screen and look for the **"FnO Bot"** icon. Open it! It will now run in a full-screen, standalone window without any browser bars.

---

## 🛠 Step 3: Optimization for S24

### 🔋 Keep it Running
- **Disable Battery Optimization**: Long press the Termux app icon > Info > Battery > Select **"Unrestricted"**.
- **Acquire Wake Lock**: In Termux, pull down the notification bar and tap **"Acquire wakelock"** to prevent the CPU from sleeping.

### 🏠 Edge-to-Edge Display
The app is now configured with `viewport-fit=cover`, meaning it will utilize the area around your S24's camera cutout for a truly immersive look.

---

## ⚠️ Important Notes
- **Fyers Token**: You still need to generate a new access token every 24 hours. You can do this via the dashboard's "Token Generator" link or by running `python fyers_auth.py` in Termux.
- **Background Activity**: PWAs on Android stay active quite well, but if you notice the P&L stops updating, just reopen the app from the home screen.

**Happy Trading! 📈**
