"""
Diagnostic Script - Check if everything is set up correctly
"""

import sys
import os

print("\n" + "="*70)
print("FnO Trading Dashboard - Diagnostic Check")
print("="*70 + "\n")

errors = []
warnings = []
success = []

# Check 1: Python version
print("1. Checking Python version...")
version = sys.version_info
if version.major >= 3 and version.minor >= 7:
    success.append(f"✓ Python {version.major}.{version.minor}.{version.micro}")
else:
    errors.append(f"✗ Python version too old: {version.major}.{version.minor}")
print(f"   Python: {version.major}.{version.minor}.{version.micro}\n")

# Check 2: Required files
print("2. Checking required files...")
required_files = [
    'app.py',
    'fno_trading_strategy.py',
    'config.py',
    'requirements.txt',
    'templates/dashboard.html'
]

for file in required_files:
    if os.path.exists(file):
        success.append(f"✓ Found {file}")
        print(f"   ✓ {file}")
    else:
        errors.append(f"✗ Missing {file}")
        print(f"   ✗ Missing: {file}")
print()

# Check 3: Python packages
print("3. Checking Python packages...")
packages = {
    'flask': 'Flask',
    'flask_cors': 'Flask-CORS',
    'fyers_apiv3': 'Fyers API',
    'pandas': 'Pandas',
}

for module, name in packages.items():
    try:
        __import__(module)
        success.append(f"✓ {name} installed")
        print(f"   ✓ {name}")
    except ImportError:
        errors.append(f"✗ {name} not installed")
        print(f"   ✗ {name} not installed")
print()

# Check 4: Configuration
print("4. Checking configuration...")
try:
    from config import FYERS_CONFIG, STOCK_LIST, TRADING_CONFIG
    
    client_id = FYERS_CONFIG.get("CLIENT_ID", "")
    access_token = FYERS_CONFIG.get("ACCESS_TOKEN", "")
    
    if client_id and client_id != "YOUR_CLIENT_ID_HERE":
        success.append("✓ Client ID configured")
        print(f"   ✓ Client ID: {client_id[:10]}...")
    else:
        warnings.append("⚠ Client ID not configured")
        print("   ⚠ Client ID not configured in config.py")
    
    if access_token and access_token != "YOUR_ACCESS_TOKEN_HERE":
        success.append("✓ Access Token in config.py")
        print(f"   ✓ Access Token: {access_token[:10]}...")
    elif os.path.exists('access_token.txt'):
        success.append("✓ Access Token in access_token.txt")
        print("   ✓ Access Token found in access_token.txt")
    else:
        warnings.append("⚠ Access Token not found")
        print("   ⚠ Access Token not configured")
        print("   → Run: python3 fyers_auth.py")
    
    if STOCK_LIST and len(STOCK_LIST) > 0:
        success.append(f"✓ {len(STOCK_LIST)} stocks configured")
        print(f"   ✓ Stock list: {len(STOCK_LIST)} stocks")
    else:
        errors.append("✗ No stocks in STOCK_LIST")
        print("   ✗ No stocks configured")
    
except Exception as e:
    errors.append(f"✗ Error loading config: {e}")
    print(f"   ✗ Error loading config.py: {e}")
print()

# Check 5: Templates directory
print("5. Checking templates...")
if os.path.exists('templates'):
    if os.path.exists('templates/dashboard.html'):
        success.append("✓ Dashboard template found")
        print("   ✓ templates/dashboard.html exists")
    else:
        errors.append("✗ dashboard.html not found")
        print("   ✗ templates/dashboard.html missing")
else:
    errors.append("✗ templates directory not found")
    print("   ✗ templates/ directory missing")
print()

# Check 6: Network
print("6. Checking network...")
import socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    success.append(f"✓ Local IP: {local_ip}")
    print(f"   ✓ Local IP Address: {local_ip}")
    print(f"   → Access from phone: http://{local_ip}:5000")
except Exception as e:
    warnings.append("⚠ Could not determine local IP")
    print(f"   ⚠ Could not determine local IP: {e}")
print()

# Summary
print("="*70)
print("DIAGNOSTIC SUMMARY")
print("="*70)

if success:
    print(f"\n✓ SUCCESS ({len(success)}):")
    for item in success[:5]:  # Show first 5
        print(f"  {item}")
    if len(success) > 5:
        print(f"  ... and {len(success) - 5} more")

if warnings:
    print(f"\n⚠ WARNINGS ({len(warnings)}):")
    for item in warnings:
        print(f"  {item}")

if errors:
    print(f"\n✗ ERRORS ({len(errors)}):")
    for item in errors:
        print(f"  {item}")

print("\n" + "="*70)

# Recommendations
if errors:
    print("\n🔧 RECOMMENDED ACTIONS:")
    print()
    if any('package' in e.lower() or 'installed' in e.lower() for e in errors):
        print("1. Install missing packages:")
        print("   pip3 install -r requirements.txt")
        print()
    
    if any('config' in e.lower() for e in errors):
        print("2. Configure Fyers API:")
        print("   python3 fyers_auth.py")
        print()
    
    if any('file' in e.lower() or 'Missing' in e for e in errors):
        print("3. Make sure all files are in the same directory")
        print()

elif warnings:
    print("\n🔧 RECOMMENDED ACTIONS:")
    print()
    if any('token' in w.lower() for w in warnings):
        print("1. Generate access token:")
        print("   python3 fyers_auth.py")
        print()
    
    if any('client' in w.lower() for w in warnings):
        print("2. Update config.py with your Fyers Client ID")
        print()

else:
    print("\n✅ ALL CHECKS PASSED!")
    print("\nYou're ready to start the server:")
    print("   python3 app.py")
    print()
    if success and any('IP' in s for s in success):
        for item in success:
            if 'IP' in item and 'http' in item:
                print(f"Then open on your phone: {item.split(': ')[1]}")

print("="*70 + "\n")
