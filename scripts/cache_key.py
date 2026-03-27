#!/usr/bin/env python3
# Purpose: generate cache key for CI dependency caches

import hashlib
import os
from pathlib import Path


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def main():
    branch = os.environ.get("BRANCH_NAME", "unknown")
    tool_ver = os.environ.get("TOOL_VERSION", "v0")
    lockfile = os.environ.get("LOCKFILE", "")
    lock_hash = sha256(Path(lockfile)) if lockfile and Path(lockfile).exists() else "nolock"
    print(f"{branch}-{lock_hash}-{tool_ver}")


if __name__ == "__main__":
    main()
