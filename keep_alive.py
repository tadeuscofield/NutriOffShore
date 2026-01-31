"""
Keep-alive pinger for Koyeb backend.
Sends a health check request every 3 minutes to prevent the free tier from sleeping.

Usage: python keep_alive.py
Or run as a background task: pythonw keep_alive.py
"""
import urllib.request
import time
import datetime
import sys

BACKEND_URL = "https://nutrioffshore-veridisambiental-0ea3f22c.koyeb.app/health"
INTERVAL_SECONDS = 180  # 3 minutes

def ping():
    try:
        req = urllib.request.Request(BACKEND_URL)
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{now}] Ping OK - Status: {status}")
            return True
    except Exception as e:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] Ping FAILED - {e}")
        return False

if __name__ == "__main__":
    print(f"Keep-alive started for: {BACKEND_URL}")
    print(f"Interval: {INTERVAL_SECONDS}s ({INTERVAL_SECONDS // 60} min)")
    print("Press Ctrl+C to stop\n")

    while True:
        ping()
        time.sleep(INTERVAL_SECONDS)
