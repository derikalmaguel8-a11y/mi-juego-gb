nano buildozer.spec   # pega la config
[app]
title = Mi Juego GB
package.name = mijuegogb
package.domain = org.mijuego

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf
source.include_patterns = assets/*,images/*

version = 0.1

requirements = python3==3.10.12, kivy==2.3.0, pygame-ce==2.4.0, cython<3.0.0

orientation = landscape
fullscreen = 1

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

android.permissions = VIBRATE
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
