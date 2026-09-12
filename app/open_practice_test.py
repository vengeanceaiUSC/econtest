#!/usr/bin/env python3
"""One-click launcher — opens Practice Test 1 in your browser."""
import http.server
import os
import socketserver
import sys
import webbrowser
from pathlib import Path

PORT = 8765
DIR = Path(__file__).resolve().parent / "dist"


def main():
    if not DIR.exists():
        print("Run from the app folder after: npm install && npm run build")
        sys.exit(1)
    os.chdir(DIR)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        url = f"http://localhost:{PORT}/"
        print(f"\n  ECON 351 Practice Test 1")
        print(f"  Open in browser: {url}\n")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
