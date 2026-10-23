#!/data/data/com.termux/files/usr/bin/bash
# Launcher — this is what she types.

# Start the Termux X server in the background (connects to the Termux:X11 app).
# Harmless if already running; harmless if the app isn't open (menu options
# 1, 2, 5 don't need a display — only 3 and 4 do).
termux-x11 :0 >/dev/null 2>&1 &
disown 2>/dev/null || true
sleep 1

export DISPLAY=:0
exec proot-distro login debian --shared-tmp -- bash -c '
export DISPLAY=:0
cd /root/mp-bot
./venv/bin/python3 scripts/menu.py
'
