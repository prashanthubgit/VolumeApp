[app]
title = MyKivyVolumeApp
package.name = mykivyvolumeapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
orientation = portrait
fullscreen = 0
icon.filename = icon.png

# Android specific settings
android.permissions = INTERNET,MODIFY_AUDIO_SETTINGS,ACCESS_NETWORK_STATE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.arch = armeabi-v7a
android.build_tools = 31.0.0
android.accept_sdk_license = True

# Requirements
requirements = python3,kivy,pyjnius

# Gradle settings
android.gradle_options = org.gradle.jvmargs=-Xmx4096m

# Features
android.features = android.hardware.touchscreen

# Logcat filters
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 1
