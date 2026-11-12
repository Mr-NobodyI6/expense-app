[app]
title = Expense Tracker
package.name = expensetracker
package.domain = org.myname
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = hostpython3==3.11.5,python3==3.11.5,kivy==2.3.0
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.api = 34
android.minapi = 24
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
