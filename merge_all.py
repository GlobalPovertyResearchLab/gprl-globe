#!/usr/bin/env python3
"""Merge every open PR (oldest first), then pull and open the globe.

    python3 merge_all.py            # merge, pull, build, open
    python3 merge_all.py --dry-run  # list what would merge

Needs the GitHub CLI (gh), signed in as someone who can merge.
A PR that touches anything outside people/ is skipped, never merged.
"""
import json
import subprocess
import sys


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def main() -> None:
    dry = "--dry-run" in sys.argv
    prs = json.loads(gh("pr", "list", "--state", "open", "--limit", "500",
                        "--json", "number,author,files"))
    merged, skipped = 0, []
    for pr in sorted(prs, key=lambda p: p["number"]):
        n, who = pr["number"], pr["author"]["login"]
        outside = [f["path"] for f in pr["files"] if not f["path"].startswith("people/")]
        if outside:
            skipped.append((n, who, "touches " + ", ".join(outside[:3])))
            continue
        if dry:
            print(f"  would merge #{n} ({who})")
            continue
        try:
            gh("pr", "merge", str(n), "--squash")
            merged += 1
            print(f"✓ #{n} {who}")
        except subprocess.CalledProcessError as e:
            skipped.append((n, who, e.stderr.strip().splitlines()[-1] if e.stderr else "merge failed"))

    for n, who, why in skipped:
        print(f"✗ #{n} {who}: {why}")
    if dry:
        return
    print(f"{merged} merged, {len(skipped)} skipped")
    subprocess.run(["git", "pull", "--ff-only"], check=True)
    subprocess.run([sys.executable, "globe.py"], check=True)


if __name__ == "__main__":
    main()
