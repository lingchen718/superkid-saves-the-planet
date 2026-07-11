
[app]

# (str) Title of your application
title = Super Kid Saves the Planet

# (str) Package name (lowercase, no spaces)
package.name = superkid

# (str) Package domain (reverse-DNS, anything unique-looking is fine)
package.domain = org.yourname.superkid

# (str) Source code directory
source.dir = .

# (str) Entry point file
source.main = main.py

# (list) File extensions to include in the APK
# Add any other types you use (e.g. mp3, ogg, wav for sound)
source.include_exts = py,png,jpg,jpeg,ttf,otf,wav,mp3,ogg,json,txt

# (str) Application version
version = 1.0.0

# (list) Requirements
# Only add things you actually `import`. random, math, os, sys, json are built-in.
# If you use pygame only, this is enough. Add more if your code uses them.
requirements = python3,pygame==2.1.3,pillow==10.4.0


# (str) Presplash image shown while the app loads
# Replace `presplash.png` with whatever file you have, or comment this out
# presplash.filename = %(source.dir)s/presplash.png

# (str) App icon
# Replace `icon.png` with your icon file, or comment this out
# icon.filename = %(source.dir)s/images/icon.png

# (str) Supported orientations
# Use: portrait, landscape, or sensor (lets phone rotate)
orientation = landscape

# (bool) Fullscreen app
fullscreen = 1


[buildozer]
# (str) Log level: 0=quiet, 1=info, 2=debug (use 2 if you hit errors)
log_level = 2


[android]
# (int) Target Android API
android.api = 33

# (int) Minimum Android API (Android 5.0)
android.minapi = 24

# (str) NDK version
android.ndk = 25b
android.ndk_api = 24

# (bool) Accept Android SDK licenses automatically
android.accept_sdk_license = True

# Make sure build-tools version is explicit so buildozer downloads it
android.build_tools_version = 33.0.2
# Platform tools (adb, fastboot, etc.)
android.platform_tools_version = 33.0.2
# Add the build-tools directory to PATH
android.sdk_path = $ANDROIDSDK

# (str) Permissions - leave empty unless you need network/storage
android.permissions =

