#!/usr/bin/env python3
"""
Collect *all* GitHub events for a user on a given calendar date
and dump them as newline-delimited JSON (one event per line).

Usage
$ export GH_TOKEN="ghp_xxx"          # optional but recommended
$ python gh_daylog.py 2025-04-22     # ISO-8601 date
"""
import os, sys, json, requests, datetime
from pathlib import Path

USER = "mgoin"                                   # <-- change if needed
TOKEN = os.getenv("GH_TOKEN")                    # PAT with 'repo' + 'read:org' scopes
BASE  = f"https://api.github.com/users/{USER}/events"

def iso_date(dt):      # datetime → 'YYYY-MM-DD'
    return dt.strftime("%Y-%m-%d")

def wanted(date, evt):
    ts = datetime.datetime.fromisoformat(evt["created_at"].replace("Z", "+00:00"))
    return iso_date(ts) == date

def fetch(date):
    headers = {"Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    page = 1
    while True:
        url = f"{BASE}?per_page=100&page={page}"
        data = requests.get(url, headers=headers, timeout=15).json()
        if not data:
            break
        for evt in data:
            if wanted(date, evt):
                yield evt
        # Short-circuit once events fall outside the target date
        if not wanted(date, data[-1]):
            break
        page += 1

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: gh_daylog.py YYYY-MM-DD")
    date = sys.argv[1]
    path = Path(f"{USER}-{date}.ndjson")
    with path.open("w") as fp:
        for evt in fetch(date):
            fp.write(json.dumps(evt) + "\n")
    print(f"Wrote {path}.  Lines ≈ events for {date}")

if __name__ == "__main__":
    main()
