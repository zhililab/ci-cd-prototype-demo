#!/usr/bin/env python3
# Purpose: write artifact metadata for traceability
# Output:
#   - metadata json file at output path
import json
import os
from pathlib import Path


def main():
    output = Path(os.environ.get("ARTIFACT_META_OUT", "artifact_meta.json"))
    meta = {
        "commit": os.environ.get("GIT_COMMIT", ""),
        "build_id": os.environ.get("BUILD_ID", ""),
        "branch": os.environ.get("BRANCH_NAME", ""),
        "modules": os.environ.get("IMPACTED_MODULES", "")
    }
    output.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
