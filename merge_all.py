#!/usr/bin/env python3
"""Merge every open PR (oldest first), then pull and open the globe.

    python3 merge_all.py            # merge, pull, build, open
    python3 merge_all.py --dry-run  # list what would merge

Needs the GitHub CLI (gh), signed in as someone who can merge.
A PR that touches anything outside people/ is skipped, never merged.
A PR whose profile wouldn't build (missing field, no photo, bad lat/lon) stays open, with the reason.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from globe import load

ROOT = Path(__file__).resolve().parent  # run gh and git here, wherever the script is started from


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True, cwd=ROOT).stdout


def check(n: int, head: str, folders: set[str]) -> None:
    """Build each people/<folder> exactly as the PR's head commit leaves it; raise ValueError if one is broken."""
    subprocess.run(["git", "fetch", "-q", "origin", f"pull/{n}/head"], check=True, capture_output=True, cwd=ROOT)
    fetched = subprocess.run(["git", "rev-parse", "FETCH_HEAD"], check=True, capture_output=True, text=True, cwd=ROOT).stdout.strip()
    if fetched != head:
        raise ValueError("changed while merging; rerun")
    with tempfile.TemporaryDirectory() as tmp:
        for folder in sorted(folders):
            tar = subprocess.run(["git", "archive", "FETCH_HEAD", f"people/{folder}"], capture_output=True, cwd=ROOT)
            if tar.returncode:
                raise ValueError(f"{folder}: nothing left in people/{folder}")
            subprocess.run(["tar", "-x", "-C", tmp], input=tar.stdout, check=True)
            try:
                load(Path(tmp) / "people" / folder)
            except Exception as e:  # any malformed profile (wrong JSON shape, bad types) skips the PR, never stops the run
                raise ValueError(f"{folder}: {e}") from None


def main() -> None:
    sys.stdout.reconfigure(line_buffering=True)  # keep ✓/✗ lines in order with git's output
    dry = "--dry-run" in sys.argv
    prs = json.loads(gh("pr", "list", "--state", "open", "--limit", "500",
                        "--json", "number,author,files,headRefOid"))
    merged, skipped = 0, []
    for pr in sorted(prs, key=lambda p: p["number"]):
        n, who, head = pr["number"], pr["author"]["login"], pr["headRefOid"]
        paths = [f["path"] for f in pr["files"]]
        outside = [p for p in paths if not p.startswith("people/")]
        if outside:
            skipped.append((n, who, "touches " + ", ".join(outside[:3])))
            continue
        try:
            check(n, head, {p.split("/")[1] for p in paths})
        except (ValueError, subprocess.CalledProcessError) as e:
            skipped.append((n, who, str(e)))
            continue
        if dry:
            print(f"  would merge #{n} ({who})")
            continue
        try:
            gh("pr", "merge", str(n), "--squash", "--match-head-commit", head)  # merge only the commit that was checked
            merged += 1
            print(f"✓ #{n} {who}")
        except subprocess.CalledProcessError as e:
            skipped.append((n, who, e.stderr.strip().splitlines()[-1] if e.stderr else "merge failed"))

    for n, who, why in skipped:
        print(f"✗ #{n} {who}: {why}")
    if dry:
        return
    print(f"{merged} merged, {len(skipped)} skipped")
    subprocess.run(["git", "pull", "--ff-only"], check=True, cwd=ROOT)
    subprocess.run([sys.executable, str(ROOT / "globe.py")], check=True)


if __name__ == "__main__":
    main()
