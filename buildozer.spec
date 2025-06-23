[app]
title = MyKivyApp
package.name = mykivyapp
package.domain = org.mylab
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
icon.filename = icon.png
orientation = portrait
fullscreen = 1
source.main = main.py

# Requirements
requirements = python3,kivy,kivymd

# (list) Include image files
presplash.filename = 1234.jpg

# (bool) Hide the statusbar
android.hide_statusbar = 1

# Permissions
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1

[app/android]
android.api = 33
android.ndk = 25b
android.archs = armeabi-v7a, arm64-v8a
android.entrypoint = org.kivy.android.PythonActivity
android.copy_libs = 1