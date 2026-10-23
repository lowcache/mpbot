#!/usr/bin/env python3
"""Headless loop: replay the recorded flow every N seconds."""
import importlib.util
import sys
import time
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent.parent
STORAGE = ROOT / "storage.json"
FLOW_PATH = ROOT / "flow.py"
LOG = ROOT / "logs" / "bot.log"
LOG.parent.mkdir(exist_ok=True)


def log(msg):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def load_flow():
    spec = importlib.util.spec_from_file_location("flow", FLOW_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_once(flow):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        ctx_kwargs = {}
        if STORAGE.exists():
            ctx_kwargs["storage_state"] = str(STORAGE)
        context = browser.new_context(**ctx_kwargs)
        page = context.new_page()
        try:
            flow.run(page)
            context.storage_state(path=str(STORAGE))
            log("Bump completed")
        finally:
            context.close()
            browser.close()


def main():
    interval = int(sys.argv[1]) if len(sys.argv) > 1 else 1800
    log(f"Loop started (every {interval // 60} min). Ctrl+C to stop.")
    flow = load_flow()
    while True:
        try:
            run_once(flow)
        except KeyboardInterrupt:
            log("Stopped by user.")
            return
        except Exception as e:
            log(f"Error: {type(e).__name__}: {e}")
        log(f"Sleeping {interval // 60} min...")
        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            log("Stopped by user.")
            return


if __name__ == "__main__":
    main()
