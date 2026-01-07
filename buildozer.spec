[app]

# (str) Title of your application
title = FnO Trading Bot

# (str) Package name
package.name = fnobot

# (str) Package domain (needed for android/ios packaging)
package.domain = org.rahulkohli

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,html,js,css,json,csv,txt

# (list) Source files to exclude
source.exclude_dirs = tests, bin, .venv, .idea, __pycache__, static/icons

# (str) Application versioning
version = 1.0.3

# Critical: Numpy must come before Pandas for correct recipe ordering
# Added android, pyjnius for native WebView support
requirements = python3,kivy==2.2.1,numpy,pandas,flask,flask-cors,requests,python-dateutil,fyers-apiv3,webcolors,sqlite3,openssl,android,pyjnius

# (str) Icon of the application
icon.filename = static/icons/icon-512.png

# (str) Supported orientations
orientation = portrait

#
# Android specific
#

# (bool) Fullscreen
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (str) Extra xml tree to add to manifest (Allow cleartext for local Flask)
android.manifest.manifest_xml = <manifest xmlns:android="http://schemas.android.com/apk/res/android"><application android:usesCleartextTraffic="true" /></manifest>

# (int) Target Android API
android.api = 31

# (int) Minimum API (Set to 24 for Pandas/Numpy compatibility)
android.minapi = 24

# (int) NDK API (Set to 24 for Pandas/Numpy compatibility)
android.ndk_api = 24

# (bool) Accept SDK license
android.accept_sdk_license = True

# (list) Android architectures (Reduced to arm64 only to save 50% build time)
android.archs = arm64-v8a

# (bool) enables Android auto backup feature
android.allow_backup = True

# (str) The format used to package the app
android.release_artifact = apk
android.debug_artifact = apk

#
# Python for android (p4a) specific
#

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2

#
# Buildozer section
#

[buildozer]

# (int) Log level (2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1


