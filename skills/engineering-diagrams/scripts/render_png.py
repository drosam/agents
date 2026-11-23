#!/usr/bin/env python3
"""Render an SVG to PNG with headless Chrome, Chromium, Edge or Brave for visual review.

Usage: render_png.py FILE.svg [OUT.png] [--scale N]

Default OUT is <system temp>/engineering-diagrams/<name>.png; default scale is 2.
Set CHROME_PATH to override browser discovery.
Prints JSON {"png": path, "width": w, "height": h, "scale": n}. Exits 2 when no browser
is found and 1 when rendering fails. Standard library only (Python 3.8+).
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

MAC_APPS = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
)
PATH_NAMES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "brave-browser")


def find_browser():
    env = os.environ.get("CHROME_PATH")
    if env and os.path.exists(env):
        return env
    for app in MAC_APPS:
        if os.path.exists(app):
            return app
    for name in PATH_NAMES:
        found = shutil.which(name)
        if found:
            return found
    return None


def size_of(svg):
    root = ET.parse(svg).getroot()
    parts = [p for p in re.split(r"[\s,]+", (root.get("viewBox") or "").strip()) if p]
    if len(parts) == 4:
        return int(float(parts[2]) + 0.5), int(float(parts[3]) + 0.5)
    return int(float(root.get("width", "1200"))), int(float(root.get("height", "800")))


def main(argv):
    args = list(argv)
    scale = 2
    if "--scale" in args:
        k = args.index("--scale")
        scale = float(args[k + 1])
        del args[k:k + 2]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 2
    svg = os.path.abspath(args[0])
    out = args[1] if len(args) > 1 else os.path.join(
        tempfile.gettempdir(), "engineering-diagrams", os.path.splitext(os.path.basename(svg))[0] + ".png")
    out = os.path.abspath(out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    browser = find_browser()
    if not browser:
        print(json.dumps({"error": "no Chrome/Chromium/Edge/Brave found; set CHROME_PATH or skip with 'visual check skipped'"}))
        return 2
    width, height = size_of(svg)
    if os.path.exists(out):
        os.remove(out)
    cmd = [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
           "--force-device-scale-factor=%g" % scale, "--window-size=%d,%d" % (width, height),
           "--screenshot=%s" % out, "file://" + svg]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"error": "render failed: %s" % exc}))
        return 1
    if not os.path.exists(out):
        print(json.dumps({"error": "browser produced no screenshot", "browser": browser}))
        return 1
    print(json.dumps({"png": out, "width": width, "height": height, "scale": scale}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
