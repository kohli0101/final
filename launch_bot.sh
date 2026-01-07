#!/data/data/com.termux/files/usr/bin/bash

# 1. Kill any existing instances to prevent port errors
pkill -f "python3 app.py"

# 2. Navigate to the project folder
cd ~/final

# 3. Start the Flask server in the background and log output
# nohup allows it to run even if the terminal closes
nohup python3 app.py > termux_log.txt 2>&1 &

# 4. Wait a few seconds for the server to initialize
echo "Starting FnO Bot..."
sleep 5

# 5. Open the dashboard in your default browser (Chrome/Samsung Internet)
termux-open-url http://localhost:5000

echo "Bot is running in background!"
