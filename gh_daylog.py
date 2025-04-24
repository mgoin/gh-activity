# /// script
# dependencies = [
#   "requests",
# ]
# ///
"""
Collect *all* GitHub events for a user on a given calendar date
and dump them as newline-delimited JSON (one event per line).

Usage
$ export GH_TOKEN="ghp_xxx"               # optional but recommended
$ python gh_daylog.py octocat 2025-04-22  # ISO-8601 date
"""
import os
import sys
import json
import requests
import datetime
from pathlib import Path

TOKEN = os.getenv("GH_TOKEN")  # PAT with 'repo' + 'read:org' scopes


def get_events_url(user):
    return f"https://api.github.com/users/{user}/events"


def iso_date(dt):  # datetime → 'YYYY-MM-DD'
    return dt.strftime("%Y-%m-%d")


def wanted(date, evt):
    ts = datetime.datetime.fromisoformat(evt["created_at"].replace("Z", "+00:00"))
    return iso_date(ts) == date


def fetch(date, user):
    headers = {"Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    page = 1
    base_url = get_events_url(user)
    while True:
        url = f"{base_url}?per_page=100&page={page}"
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
    if len(sys.argv) != 3:
        sys.exit("Usage: gh_daylog.py username YYYY-MM-DD")
    user = sys.argv[1]
    date = sys.argv[2]
    path = Path(f"{user}-{date}.ndjson")
    with path.open("w") as fp:
        for evt in fetch(date, user):
            fp.write(json.dumps(evt) + "\n")
    print(f"Wrote {path}.  Lines ≈ events for {user} on {date}")


if __name__ == "__main__":
    main()
