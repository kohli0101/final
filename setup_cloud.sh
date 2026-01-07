#!/bin/bash

# ============================================================================
# FnO Trading Dashboard - Quick Cloud Setup with Ngrok
# ============================================================================

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  FnO Trading Dashboard - Cloud Setup"
echo "════════════════════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo -e "${YELLOW}⚠️  Ngrok not found. Installing...${NC}"
    
    # Check system
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install ngrok
        else
            echo -e "${RED}❌ Homebrew not found. Please install from: https://brew.sh${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}Please install ngrok manually from: https://ngrok.com/download${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✓ Ngrok installed${NC}"

# Check if ngrok is authenticated
if ! ngrok config check &> /dev/null; then
    echo ""
    echo -e "${YELLOW}⚠️  Ngrok not authenticated${NC}"
    echo ""
    echo "Please follow these steps:"
    echo "1. Go to: https://dashboard.ngrok.com/signup"
    echo "2. Sign up (free)"
    echo "3. Copy your auth token"
    echo "4. Run: ngrok config add-authtoken YOUR_TOKEN"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ Ngrok authenticated${NC}"

# Check if Flask server is running
echo ""
echo "Checking Flask server..."

if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${GREEN}✓ Flask server is running on port 5000${NC}"
else
    echo -e "${YELLOW}⚠️  Flask server not running${NC}"
    echo ""
    echo "Please start the server in another terminal:"
    echo "  cd ~/fno-trading"
    echo "  python3 app.py"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Start ngrok tunnel
echo ""
echo "════════════════════════════════════════════════════════════════════"
echo "  Starting Ngrok Tunnel..."
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "Your dashboard will be accessible from anywhere on the internet!"
echo ""
echo "Press Ctrl+C to stop the tunnel"
echo ""
echo "════════════════════════════════════════════════════════════════════"
echo ""

# Start ngrok with custom domain (if you have it) or random URL
ngrok http 5000 --log=stdout

# When stopped
echo ""
echo -e "${GREEN}Tunnel stopped.${NC}"
echo "Your dashboard is no longer accessible remotely."
echo ""
