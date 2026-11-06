#!/usr/bin/env python3
"""Claude plan usage (5-hour and weekly limits) as JSON, for the GNOME top bar.

Uses the login the Claude app (Code tab) keeps in ~/.claude/.credentials.json
and the same endpoint as the /usage command. The endpoint is undocumented and may change.
The token is never refreshed here (the app does that) nor printed. If the login
has expired, returns the last known value with "stale": true.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

CREDENTIALS = os.path.expanduser("~/.claude/.credentials.json")
URL = "https://api.anthropic.com/api/oauth/usage"
CACHE = os.path.expanduser("~/.cache/claude-usage.json")


def from_cache(error):
    try:
        with open(CACHE) as f:
            out = json.load(f)
    except (OSError, ValueError):
        return {"error": error}
    out.update(stale=True, error=error)
    return out


def fetch():
    try:
        with open(CREDENTIALS) as f:
            oauth = json.load(f)["claudeAiOauth"]
    except (OSError, ValueError, KeyError):
        return from_cache("Log in to the Claude app")
    if oauth.get("expiresAt", 0) / 1000 < time.time():
        return from_cache("Login expired: open a session in the app's Code tab")

    req = urllib.request.Request(URL, headers={
        "Authorization": f"Bearer {oauth['accessToken']}",
        "anthropic-beta": "oauth-2025-04-20",
        "User-Agent": "claude-code",
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        return from_cache(f"HTTP error {e.code}")
    except (urllib.error.URLError, TimeoutError, ValueError):
        return from_cache("No connection")

    out = {}
    for key, src in (("session", "five_hour"), ("weekly", "seven_day")):
        block = data.get(src) or {}
        util = block.get("utilization")
        out[key] = None if util is None else round(util)
        out[key + "_resets_at"] = block.get("resets_at")
    out["fetched_at"] = int(time.time())
    try:
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        with open(CACHE, "w") as f:
            json.dump(out, f)
    except OSError:
        pass
    return out


if __name__ == "__main__":
    json.dump(fetch(), sys.stdout)
    print()
