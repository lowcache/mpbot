#!/usr/bin/env python3
"""Text menu — this is the only thing she interacts with."""
import os
import sys
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCRIPTS = ROOT / "scripts"
FLOW = ROOT / "flow.py"
LOG = ROOT / "logs" / "bot.log"

LOG.parent.mkdir(exist_ok=True)


def banner():
    os.system("clear")
    print()
    print("  +-------------------------------+")
    print("  |           MP Bot              |")
    print("  +-------------------------------+")
    print()


def pause():
    print()
    try:
        input("  Press Enter to continue...")
    except (EOFError, KeyboardInterrupt):
        print()


def run_loop(interval_seconds):
    if not FLOW.exists():
        banner()
        print("  No flow recorded yet. Pick option 3 first.")
        pause()
        return
    banner()
    print(f"  Running every {interval_seconds // 60} minutes.")
    print("  Press Ctrl+C to stop and go back to the menu.")
    print()
    try:
        subprocess.run(
            [str(ROOT / "venv" / "bin" / "python3"),
             str(SCRIPTS / "worker.py"),
             str(interval_seconds)]
        )
    except KeyboardInterrupt:
        pass
    print()
    print("  Stopped.")
    time.sleep(1)


def record_flow():
    banner()
    print("  A browser window will open on your phone.")
    print("  (Make sure the Termux:X11 app is already open.)")
    print()
    print("  Then:")
    print("    1. Log in to the site.")
    print("    2. Do ONE full bump/post action.")
    print("    3. Close the browser window.")
    print()
    try:
        input("  Press Enter when ready...")
    except (EOFError, KeyboardInterrupt):
        return
    subprocess.run(
        [str(ROOT / "venv" / "bin" / "python3"), str(SCRIPTS / "record.py")]
    )
    print()
    if FLOW.exists():
        print("  Flow saved. You can now pick option 1 or 2.")
    else:
        print("  No flow was saved. Try again.")
    pause()


def relogin():
    banner()
    print("  A browser window will open on your phone.")
    print("  (Make sure the Termux:X11 app is already open.)")
    print()
    print("  Just log in, then close the browser window.")
    print()
    try:
        input("  Press Enter when ready...")
    except (EOFError, KeyboardInterrupt):
        return
    subprocess.run(
        [str(ROOT / "venv" / "bin" / "python3"),
         str(SCRIPTS / "record.py"),
         "--login-only"]
    )
    print()
    print("  Done.")
    pause()


def view_log():
    banner()
    if LOG.exists():
        for line in LOG.read_text().splitlines()[-25:]:
            print("  " + line)
    else:
        print("  No log entries yet.")
    pause()


def menu():
    while True:
        banner()
        if not FLOW.exists():
            print("  First time? Pick option 3 to set up.")
            print()
        print("  1) Run bump every 15 min")
        print("  2) Run bump every 30 min")
        print("  3) Record flow (first time / after site changes)")
        print("  4) Log in again (if it stops working)")
        print("  5) View recent log")
        print("  6) Quit")
        print()
        try:
            choice = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return

        if choice == "1":
            run_loop(15 * 60)
        elif choice == "2":
            run_loop(30 * 60)
        elif choice == "3":
            record_flow()
        elif choice == "4":
            relogin()
        elif choice == "5":
            view_log()
        elif choice == "6":
            return
        else:
            print("  Not a valid choice.")
            time.sleep(1)


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        pass
    print()
