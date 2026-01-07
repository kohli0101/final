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

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to include all the files)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to include all the files)
source.exclude_dirs = tests, bin, .venv, .idea, __pycache__

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,flask,flask-cors,requests,pandas,numpy,python-dateutil,fyers-apiv3,webcolors

# (str) Custom source folders for requirements
# Specify list of folders to add to sys.path
#requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
icon.filename = static/icons/icon-512.png

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
#android.ndk = 25b

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess downloads or network errors
#android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If False,
# the default, you will be shown the license when installing.
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is ok for Kivy-based app
# android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to whitelist for the libpybundle.so
#android.lib_whitelist =

# (str) Full name including package path of the Java class that implements Android Activity
# use that parameter if you use a custom activity class.
#android.activity_class = org.kivy.android.PythonActivity

# (list) Android additionnal libraries to copy into libs/armeabi
#android.add_libs_armeabi = lib/armeabi/libtest.so

# (list) Android application meta-data to set (api-key-name=value)
#android.meta_data =

# (list) Android library project to add (path)
#android.library_references =

# (list) Android shared libraries which will be added to AndroidManifest.xml using <uses-library> tag
#android.uses_library =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (str) Android additional text to add to manifest
#android.manifest.add_activity_xml =

# (str) Android additional xml tree to add to manifest
#android.manifest.add_xml =

# (list) Android extra packages to download
#android.add_pkgs =

# (list) Android architectures to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) enables Android auto backup feature (on API >= 23)
android.allow_backup = True

# (str) The format used to package the app for release mode (aab or apk or default).
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or default).
android.debug_artifact = apk

#
# Python for android (p4a) specific
#

# (str) python-for-android fork to use, defaults to upstream
#p4a.fork = kivy

# (str) python-for-android branch to use, defaults to master
#p4a.branch = master

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
#p4a.source_dir =

# (str) The directory in which python-for-android should look for your own recipes (if any)
#p4a.local_recipes =

# (str) Filename to the hook for p4a
#p4a.hook =

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2

# (list) List of recipes to add to requirements
#p4a.extra_recipes =


#
# Buildozer section
#

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1

# (str) Path to build artifacts (default is .buildozer)
#build_dir = ./.buildozer

# (str) Path to bin directory (default is ./bin)
#bin_dir = ./bin
