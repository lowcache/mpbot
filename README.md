# MP Bot

A tiny Termux-based automator. Opens a real browser once so the user can
log in and demonstrate the action, then replays that action on a loop
(every 15 or 30 minutes) in a headless browser.

## What she needs installed first

From F-Droid (the Termux F-Droid repo):
- Termux
- Termux:API

The installer handles **Termux:X11** itself — it downloads the APK from
the official GitHub release and hands it to Android's installer. She
just taps "Install" when prompted. (First time she installs an APK
through Termux, Android will ask her to allow "install from unknown
sources" for Termux — that's one-time.)

## Deploying from your GitHub

Push this folder as the root of a repo. Have her run, in Termux:

```sh
pkg install -y git
git clone https://github.com/YOUR_USER/YOUR_REPO.git ~/mp-bot-src
bash ~/mp-bot-src/install.sh
```

Install takes ~15 minutes (Debian + Chromium is a big download).

If you want a one-liner, drop a `bootstrap.sh` in the repo root with
those three lines and tell her:

```sh
curl -sSL https://raw.githubusercontent.com/YOUR_USER/YOUR_REPO/main/bootstrap.sh | bash
```

## What she does

1. Opens the **Termux:X11** app (just needs to be open — can minimize).
2. In Termux, types `mp`.
3. First time: pick **option 3**. A browser window appears on her phone.
   She logs in, does one full bump/post action, closes the browser.
4. From then on: pick **option 1** (15 min) or **option 2** (30 min).
   The loop runs in the terminal; Ctrl+C stops it.
5. If the site boots her out eventually, option **4** reopens the
   browser just for a fresh login.

## Files

- `install.sh` — one-time setup she runs after `git clone`.
- `mp` — the launcher. Gets copied to `$PREFIX/bin/` by install.
- `scripts/menu.py` — the text menu she sees.
- `scripts/record.py` — opens the browser (codegen or login-only).
- `scripts/worker.py` — the headless replay loop.

Runtime data lives under `/root/mp-bot/` inside the Debian proot:
- `storage.json` — cookies (keeps her logged in).
- `flow.py` — the recorded click sequence.
- `logs/bot.log` — plain-text log.

## Troubleshooting cheatsheet (for her, over the phone)

- **"The browser doesn't open"** → Did she open the Termux:X11 app
  first? It needs to be running (minimized is fine).
- **"It says session expired"** → Pick option 4, log in, done.
- **"It stopped bumping"** → Pick option 5 to see the log. If a selector
  broke because the site changed, pick option 3 and re-record.
