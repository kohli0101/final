"""
Fyers API Authentication Helper - Simplified with Hardcoded Credentials
"""

from fyers_apiv3 import fyersModel
import webbrowser
from urllib.parse import urlparse, parse_qs

# ============================================================================
# HARDCODE YOUR CREDENTIALS HERE
# ============================================================================

HARDCODED_CREDENTIALS = {
    "CLIENT_ID": "Q8Z7HIY0II-100",           # Example: "ABCD1234-100"
    "SECRET_KEY": "RVRPS35QYQ",         # Your app secret key
    "REDIRECT_URI": "https://google.com"      # Must match Fyers app settings
}

# ============================================================================

class FyersAuth:
    def __init__(self, client_id=None, secret_key=None, redirect_uri=None):
        """
        Initialize Fyers Authentication
        Uses hardcoded credentials if not provided
        """
        self.client_id = client_id or HARDCODED_CREDENTIALS["CLIENT_ID"]
        self.secret_key = secret_key or HARDCODED_CREDENTIALS["SECRET_KEY"]
        self.redirect_uri = redirect_uri or HARDCODED_CREDENTIALS["REDIRECT_URI"]
        self.access_token = None
        
    def generate_auth_code_url(self):
        """Generate the authorization URL"""
        session = fyersModel.SessionModel(
            client_id=self.client_id,
            secret_key=self.secret_key,
            redirect_uri=self.redirect_uri,
            response_type="code",
            grant_type="authorization_code"
        )
        
        auth_url = session.generate_authcode()
        return auth_url
    
    def generate_access_token(self, auth_code):
        """Generate access token from auth code"""
        session = fyersModel.SessionModel(
            client_id=self.client_id,
            secret_key=self.secret_key,
            redirect_uri=self.redirect_uri,
            response_type="code",
            grant_type="authorization_code"
        )
        
        session.set_token(auth_code)
        response = session.generate_token()
        
        if 'access_token' in response:
            self.access_token = response['access_token']
            print(f"\n✓ Access Token Generated Successfully!")
            print(f"Access Token: {self.access_token}\n")
            
            # Save to file
            with open('access_token.txt', 'w') as f:
                f.write(self.access_token)
            print("✓ Access token saved to 'access_token.txt'")
            
            # Also save to config.py
            self.update_config_file()
            
            return self.access_token
        else:
            print(f"✗ Error generating token: {response}")
            return None
    
    def update_config_file(self):
        """Update config.py with the new access token"""
        try:
            # Read current config
            with open('config.py', 'r') as f:
                config_content = f.read()
            
            # Find and replace access token
            if 'ACCESS_TOKEN' in config_content:
                # Replace the token value
                import re
                pattern = r'"ACCESS_TOKEN":\s*"[^"]*"'
                replacement = f'"ACCESS_TOKEN": "{self.access_token}"'
                config_content = re.sub(pattern, replacement, config_content)
                
                # Write back
                with open('config.py', 'w') as f:
                    f.write(config_content)
                
                print("✓ Updated config.py with new access token")
        except Exception as e:
            print(f"⚠ Could not update config.py: {e}")
    
    def quick_auth(self):
        """Quick authentication with minimal steps"""
        print("\n" + "="*70)
        print("QUICK TOKEN GENERATOR")
        print("="*70)
        
        # Verify credentials
        if (self.client_id == "YOUR_CLIENT_ID_HERE" or 
            self.secret_key == "YOUR_SECRET_KEY_HERE"):
            print("\n⚠️  WARNING: Credentials not set!")
            print("\nPlease edit this file and update:")
            print("  - CLIENT_ID")
            print("  - SECRET_KEY")
            print("  - REDIRECT_URI")
            print("\nIn the HARDCODED_CREDENTIALS section at the top.")
            return None
        
        print(f"\nUsing Client ID: {self.client_id[:10]}...")
        
        # Generate auth URL
        auth_url = self.generate_auth_code_url()
        
        print("\n" + "="*70)
        print("STEP 1: Opening browser for authorization...")
        print("="*70)
        
        # Auto-open browser
        try:
            webbrowser.open(auth_url)
            print("✓ Browser opened automatically")
        except:
            print(f"\n⚠️  Could not open browser automatically")
            print(f"\nPlease open this URL manually:")
            print(f"\n{auth_url}\n")
        
        print("\n" + "="*70)
        print("STEP 2: After authorization, paste the redirect URL")
        print("="*70)
        print("\nAfter you authorize:")
        print("1. You'll be redirected to a URL")
        print("2. Copy the ENTIRE URL")
        print("3. Paste it below")
        print("\nExample redirect URL:")
        print("https://127.0.0.1:5000/?auth_code=XXXXX&state=sample")
        
        redirect_url = input("\n📋 Paste redirect URL here: ").strip()
        
        # Extract auth code
        try:
            parsed_url = urlparse(redirect_url)
            auth_code = parse_qs(parsed_url.query).get('auth_code', [None])[0]
            
            if auth_code:
                print(f"\n✓ Auth code extracted: {auth_code[:20]}...")
                print("\nGenerating access token...")
                
                access_token = self.generate_access_token(auth_code)
                
                if access_token:
                    print("\n" + "="*70)
                    print("✅ SUCCESS!")
                    print("="*70)
                    print("\nAccess token generated and saved to:")
                    print("  • access_token.txt")
                    print("  • config.py")
                    print("\n✓ You can now run: python3 app.py")
                    print("\nToken valid for: 24 hours")
                    print("="*70 + "\n")
                    return access_token
            else:
                print("\n✗ Could not extract auth code from URL")
                print("Please make sure you copied the complete redirect URL")
        
        except Exception as e:
            print(f"\n✗ Error processing URL: {e}")
        
        return None


def main():
    """Main function - Ultra-simplified token generation"""
    
    print("\n" + "🔐"*35)
    print("FYERS TOKEN GENERATOR - ONE COMMAND")
    print("🔐"*35)
    
    # Check if credentials are set
    if (HARDCODED_CREDENTIALS["CLIENT_ID"] == "YOUR_CLIENT_ID_HERE" or
        HARDCODED_CREDENTIALS["SECRET_KEY"] == "YOUR_SECRET_KEY_HERE"):
        
        print("\n" + "="*70)
        print("⚠️  SETUP REQUIRED")
        print("="*70)
        print("\nBefore running this script, please:")
        print("\n1. Open this file: fyers_auth.py")
        print("\n2. Find the HARDCODED_CREDENTIALS section (top of file)")
        print("\n3. Update these values:")
        print('   CLIENT_ID: "YOUR_ACTUAL_CLIENT_ID"')
        print('   SECRET_KEY: "YOUR_ACTUAL_SECRET_KEY"')
        print('   REDIRECT_URI: "https://127.0.0.1:5000"  (or your custom URI)')
        print("\n4. Save the file and run again")
        print("\n" + "="*70)
        print("\n📝 Get credentials from: https://myapi.fyers.in/dashboard")
        print("="*70 + "\n")
        return
    
    # Initialize with hardcoded credentials
    auth = FyersAuth()
    
    # Quick authentication
    auth.quick_auth()


if __name__ == "__main__":
    main()
