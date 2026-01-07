import threading
import time
import os
import sys

# Add the project directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.logger import Logger

# Standard way to implement WebView in Kivy/Android
webview_error = None
try:
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    WebView = autoclass('android.webview.WebView')
    WebViewClient = autoclass('android.webview.WebViewClient')
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
    HAS_WEBVIEW = True
except Exception as e:
    Logger.error(f"WebView: Could not load jnius/android: {e}")
    webview_error = str(e)
    HAS_WEBVIEW = False
    from kivy.uix.label import Label

class FnOBotApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical')
        
        if not HAS_WEBVIEW:
            # Display the actual error on screen for debugging
            msg = f"Error: {webview_error}" if webview_error else "WebView Only in APK"
            self.root.add_widget(Label(text=f"FnO Bot Starting...\n{msg}", halign='center'))
        
        # Start Flask server in a separate thread
        threading.Thread(target=self.start_flask, daemon=True).start()
        
        # If on Android, initialize the WebView after a short delay to let Flask start
        if HAS_WEBVIEW:
            Clock.schedule_once(self.create_webview, 2)
            
        return self.root

    @run_on_ui_thread
    def create_webview(self, *args):
        try:
            webview = WebView(Activity)
            webview.getSettings().setJavaScriptEnabled(True)
            webview.getSettings().setDomStorageEnabled(True)
            webview.setWebViewClient(WebViewClient())
            Activity.setContentView(webview)
            webview.loadUrl('http://127.0.0.1:5000')
            Logger.info("WebView: Native WebView created and loading...")
        except Exception as e:
            Logger.error(f"WebView: Failed to create: {e}")

    def start_flask(self):
        try:
            from app import app
            Logger.info("Flask: Starting server on 127.0.0.1:5000")
            app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
        except Exception as e:
            Logger.error(f"Flask: Failed to start: {e}")

if __name__ == '__main__':
    FnOBotApp().run()

