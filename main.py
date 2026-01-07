import threading
import time
import os
import sys

# Add the project directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Kivy imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

# We'll use the android-specific WebView if available, otherwise a simple label
try:
    from android.webview import WebView
    HAS_WEBVIEW = True
except ImportError:
    HAS_WEBVIEW = False
    from kivy.uix.label import Label

class FnOBotApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical')
        
        if HAS_WEBVIEW:
            self.webview = WebView('http://localhost:5000')
            self.root.add_widget(self.webview)
        else:
            self.root.add_widget(Label(text="FnO Bot Server Running\nOpen http://localhost:5000 in your browser\n\n(WebView only works inside APK)"))
        
        # Start Flask server in a separate thread
        threading.Thread(target=self.start_flask, daemon=True).start()
        
        return self.root

    def start_flask(self):
        from app import app
        # Ensure debug is False when running inside APK
        app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)

if __name__ == '__main__':
    FnOBotApp().run()
