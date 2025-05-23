#!/usr/bin/env python3
"""
Generate human-readable daily summaries from a GitHub Events NDJSON file.

Output Sections
---------------
1. Per-repo digest
2. Commit roll-up
3. PR / Issue interaction summary
"""
import sys
import json
import pathlib
import collections

# ─────────────────────────────── helpers ──────────────────────────────
def load_events(ndjson_path):
    with open(ndjson_path, "r") as fp:
        for line in fp:
            if line.strip():
                yield json.loads(line)

def repo_key(evt):
    return evt["repo"]["name"]  # owner/repo

def compare_url(repo, before, head):
    owner_repo = repo
    return f"https://github.com/{owner_repo}/compare/{before}...{head}"

# ────────────────────────── aggregation passes ────────────────────────
def aggregate(events):
    digest = collections.defaultdict(lambda: collections.Counter())
    commits_by_repo_branch = collections.defaultdict(
        lambda: collections.defaultdict(list)
    )
    interactions = collections.defaultdict(lambda: collections.defaultdict(list))
    pr_titles = {}  # Store PR titles by number

    for e in events:
        r = repo_key(e)
        t = e["type"]
        p = e["payload"]

        if t == "PushEvent":
            digest[r]["push_commits"] += p["size"]
            branch = p["ref"].split("/")[-1]  # refs/heads/branch → branch
            commits_by_repo_branch[r][branch].extend(
                [(c["sha"][:7], c["message"].splitlines()[0]) for c in p["commits"]]
            )
            # store compare link once per push
            commits_by_repo_branch[r][branch].append(
                ("COMPARE", compare_url(r, p["before"], p["head"]))
            )

        elif t == "PullRequestEvent":
            act = p["action"]  # opened, closed, merged (via closed+merged), etc.
            digest[r][f"pr_{act}"] += 1
            pr_num = p["number"]
            pr_titles[pr_num] = p["pull_request"]["title"]
            interactions[r][pr_num].append(
                f"PR #{pr_num} {act.upper()}"
            )

        elif t == "PullRequestReviewEvent":
            state = p["review"]["state"]  # APPROVED, CHANGES_REQUESTED…
            digest[r]["reviews"] += 1
            pr_num = p["pull_request"]["number"]
            pr_titles[pr_num] = p["pull_request"]["title"]
            interactions[r][pr_num].append(
                f"Reviewed PR #{pr_num} → {state}"
            )

        elif t == "PullRequestReviewCommentEvent":
            digest[r]["review_comments"] += 1
            pr_num = p["pull_request"]["number"]
            pr_titles[pr_num] = p["pull_request"]["title"]
            interactions[r][pr_num].append(
                f"Commented on PR #{pr_num}: "
                f"{p['comment']['body'].splitlines()[0][:80]}…"
            )

        elif t == "IssuesEvent":
            digest[r][f"issue_{p['action']}"] += 1
            interactions[r]["issues"].append(
                f"Issue #{p['issue']['number']} {p['action'].upper()}: "
                f"{p['issue']['title']}"
            )

        elif t == "IssueCommentEvent":
            digest[r]["issue_comments"] += 1
            interactions[r]["issues"].append(
                f"Commented on Issue #{p['issue']['number']}: "
                f"{p['comment']['body'].splitlines()[0][:80]}…"
            )

        elif t == "CreateEvent" and p["ref_type"] == "branch":
            digest[r]["branches_created"] += 1
            interactions[r]["other"].append(f"Created branch `{p['ref']}`")

    return digest, commits_by_repo_branch, interactions, pr_titles

# ────────────────────────────── printers ──────────────────────────────
def print_digest(digest):
    print("# Per-repo digest\n")
    for repo, ctr in sorted(digest.items()):
        parts = [f"{v} × {k.replace('_', ' ')}" for k, v in ctr.items()]
        print(f"* **{repo}** – " + ", ".join(parts))
    print()

def print_commits(commits):
    print("# Commit roll-up\n")
    for repo, branches in sorted(commits.items()):
        print(f"## {repo}")
        for branch, items in branches.items():
            print(f"### {branch}")
            for sha, msg in items:
                if sha == "COMPARE":
                    print(f"↪︎ compare diff: {msg}")
                else:
                    print(f"- {sha}  {msg}")
        print()
    print()

def print_interactions(interactions, pr_titles):
    print("# PR / Issue interaction summary\n")
    for repo, categories in sorted(interactions.items()):
        print(f"## {repo}")
        
        # Print PR interactions grouped by PR number
        for pr_num, actions in categories.items():
            if pr_num == "issues" or pr_num == "other":
                continue
                
            # Print PR title as header
            if pr_num in pr_titles:
                print(f"- PR #{pr_num}: {pr_titles[pr_num]}")
                for action in actions:
                    print(f"  - {action}")
        
        # Print non-PR interactions
        if "issues" in categories:
            for action in categories["issues"]:
                print(f"- {action}")
                
        if "other" in categories:
            for action in categories["other"]:
                print(f"- {action}")
        
        print()
    print()

# ───────────────────────────────── main ───────────────────────────────
def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: gh_day_summary.py path/to/user-YYYY-MM-DD.ndjson")
    ndjson_path = pathlib.Path(sys.argv[1]).expanduser()
    digest, commits, interactions, pr_titles = aggregate(load_events(ndjson_path))

    print_digest(digest)
    print_commits(commits)
    print_interactions(interactions, pr_titles)

if __name__ == "__main__":
    main()
