 #! /bin/bash

#Copyright @pshem, 2018, LGPL-3.0

#strict mode
set -euo pipefail

#check if there is a screenlock accessible through dbus
screensaver=$(dbus-send --session --dest=org.freedesktop.DBus --type=method_call --print-reply /org/freedesktop/DBus org.freedesktop.DBus.ListNames | grep screensaver | awk '{print substr($2, 2, length($2)-2)}')
# the result will be org.kde.screensaver on KDE Plasma

#TODO: detect when there is more than a single screensaver

qdbus $screensaver /ScreenSaver Lock
