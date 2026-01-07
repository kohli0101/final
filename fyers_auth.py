"""
Fyers API Authentication Helper
Helps generate access token for daily trading
"""

from fyers_apiv3 import fyersModel
import webbrowser
from urllib.parse import urlparse, parse_qs

class FyersAuth:
    def __init__(self, client_id, secret_key, redirect_uri="https://google.com"):
        """
        Initialize Fyers Authentication
        
        Args:
            client_id: Your Fyers App ID
            secret_key: Your Fyers App Secret Key
            redirect_uri: Redirect URI (must match app settings)
        """
        self.client_id = client_id
        self.secret_key = secret_key
        self.redirect_uri = redirect_uri
        self.access_token = None
        
    def generate_auth_code_url(self):
        """
        Generate the authorization URL
        User needs to visit this URL to authorize the app
        
        Returns:
            str: Authorization URL
        """
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
        """
        Generate access token from auth code
        
        Args:
            auth_code: Authorization code received after user authorization
            
        Returns:
            str: Access token
        """
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
            
            # Save to file for later use
            with open('access_token.txt', 'w') as f:
                f.write(self.access_token)
            print("✓ Access token saved to 'access_token.txt'")
            
            return self.access_token
        else:
            print(f"✗ Error generating token: {response}")
            return None
    
    def interactive_auth(self):
        """
        Interactive authentication flow
        """
        print("="*60)
        print("Fyers API Authentication")
        print("="*60)
        
        # Step 1: Generate auth URL
        print("\nStep 1: Generating authorization URL...")
        auth_url = self.generate_auth_code_url()
        print(f"\nAuthorization URL:\n{auth_url}\n")
        
        # Step 2: Open browser
        open_browser = input("Open this URL in browser? (y/n): ").strip().lower()
        if open_browser == 'y':
            webbrowser.open(auth_url)
        else:
            print("\nPlease copy and paste the URL in your browser manually.")
        
        # Step 3: Get redirect URL
        print("\n" + "="*60)
        print("After authorizing, you'll be redirected to a URL.")
        print("Copy the ENTIRE redirect URL and paste it below.")
        print("="*60)
        
        redirect_url = input("\nPaste the redirect URL here: ").strip()
        
        # Step 4: Extract auth code
        try:
            parsed_url = urlparse(redirect_url)
            auth_code = parse_qs(parsed_url.query).get('auth_code', [None])[0]
            
            if auth_code:
                print(f"\n✓ Auth code extracted: {auth_code[:20]}...")
                
                # Step 5: Generate access token
                print("\nGenerating access token...")
                access_token = self.generate_access_token(auth_code)
                
                if access_token:
                    print("\n" + "="*60)
                    print("✓ Authentication Successful!")
                    print("="*60)
                    print("\nYou can now use this access token in your trading script.")
                    print("The token is valid for 24 hours.")
                    return access_token
            else:
                print("✗ Could not extract auth code from URL")
                print("Please make sure you copied the complete redirect URL")
        
        except Exception as e:
            print(f"✗ Error processing URL: {e}")
        
        return None


def main():
    """
    Main function for interactive authentication
    """
    print("\n" + "="*60)
    print("Fyers API - Access Token Generator")
    print("="*60 + "\n")
    
    # Get credentials
    print("Enter your Fyers API credentials:")
    client_id = input("Client ID (App ID): ").strip()
    secret_key = input("Secret Key: ").strip()
    
    # Optional: custom redirect URI
    use_custom_redirect = input("\nUse custom redirect URI? (y/n, default: n): ").strip().lower()
    redirect_uri = "https://127.0.0.1:5000"
    
    if use_custom_redirect == 'y':
        redirect_uri = input("Enter redirect URI: ").strip()
    
    print(f"\nUsing redirect URI: {redirect_uri}")
    
    # Initialize auth
    auth = FyersAuth(client_id, secret_key, redirect_uri)
    
    # Start interactive authentication
    access_token = auth.interactive_auth()
    
    if access_token:
        print("\n" + "="*60)
        print("Next Steps:")
        print("="*60)
        print("1. Copy the access token from 'access_token.txt'")
        print("2. Update your config.py with the access token")
        print("3. Run your trading strategy script")
        print("\nNote: Access token expires in 24 hours")
        print("="*60 + "\n")


if __name__ == "__main__":
    main()
