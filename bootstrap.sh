#!/data/data/com.termux/files/usr/bin/bash
# One-liner installer. Replace REPO_URL below with your repo, push it, then
# have her run:
#   curl -sSL https://raw.githubusercontent.com/YOUR_USER/YOUR_REPO/main/bootstrap.sh | bash
set -e

REPO_URL="https://github.com/YOUR_USER/YOUR_REPO.git"
DEST="$HOME/mp-bot-src"

pkg install -y git

if [ -d "$DEST/.git" ]; then
    echo "==> Updating existing clone at $DEST"
    git -C "$DEST" pull --ff-only
else
    echo "==> Cloning into $DEST"
    git clone "$REPO_URL" "$DEST"
fi

bash "$DEST/install.sh"
