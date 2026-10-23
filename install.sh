#!/data/data/com.termux/files/usr/bin/bash
# One-time setup. Run on her phone after cloning the repo.
# Usage:  bash install.sh

set -e

BASE="$(cd "$(dirname "$0")" && pwd)"
echo "==> Installing from: $BASE"
echo

echo "==> Step 1/5: Termux packages"
yes | pkg update
yes | pkg install -y proot-distro x11-repo git termux-api
yes | pkg install -y termux-x11-nightly || \
    echo "   (termux-x11-nightly not in repo — the APK step below still installs the app)"

echo
echo "==> Step 2/5: Termux:X11 Android app"
# The APK is a separate install (the pkg above is just the server binary).
# We download the official nightly APK and hand it to Android's installer.
APK_URL="https://github.com/termux/termux-x11/releases/download/nightly/app-arm64-v8a-debug.apk"
APK_PATH="$HOME/termux-x11.apk"
if ! command -v termux-open >/dev/null; then
    echo "   termux-open missing — install Termux:API from F-Droid first, then re-run."
    exit 1
fi
if [ ! -f "$APK_PATH" ]; then
    echo "   Downloading Termux:X11 APK..."
    curl -L --fail -o "$APK_PATH" "$APK_URL"
fi
echo "   Opening the APK — tap Install when Android prompts you."
echo "   (You may need to allow 'Install from unknown sources' for Termux once.)"
termux-open "$APK_PATH"
echo
read -r -p "   Press Enter here AFTER Termux:X11 shows up in your app drawer..."

echo
echo "==> Step 3/5: Installing Debian (large download, be patient)"
if proot-distro list --installed 2>/dev/null | grep -q debian; then
    echo "   Debian already present, skipping."
else
    proot-distro install debian
fi

echo
echo "==> Step 4/5: Chromium + Playwright inside Debian"
proot-distro login debian --shared-tmp -- bash -c '
set -e
apt-get update -y
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv ca-certificates wget \
    libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 libxcomposite1 \
    libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 \
    libcairo2 libasound2 libxss1 fonts-liberation \
    libnspr4 libgtk-3-0 libatspi2.0-0 xdg-utils
mkdir -p /root/mp-bot
[ -d /root/mp-bot/venv ] || python3 -m venv /root/mp-bot/venv
/root/mp-bot/venv/bin/pip install --upgrade pip
/root/mp-bot/venv/bin/pip install playwright
/root/mp-bot/venv/bin/playwright install chromium
'

echo
echo "==> Step 5/5: Copying scripts"
proot-distro login debian --shared-tmp --bind "$BASE:/host-src" -- bash -c '
mkdir -p /root/mp-bot/scripts /root/mp-bot/logs
cp /host-src/scripts/*.py /root/mp-bot/scripts/
chmod +x /root/mp-bot/scripts/*.py
'

cp "$BASE/mp" "$PREFIX/bin/mp"
chmod +x "$PREFIX/bin/mp"

echo
echo "========================================"
echo "  Setup complete."
echo "========================================"
echo
echo "  Next steps for her:"
echo "    1. Open the Termux:X11 app once (minimize is fine)."
echo "    2. In Termux, type:   mp"
echo "    3. First time, pick option 3 and record the flow."
echo
