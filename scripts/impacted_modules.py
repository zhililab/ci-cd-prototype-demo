#!/usr/bin/env python3
# Purpose: compute impacted modules from git diff and module graph

import json
import os
import subprocess
from collections import defaultdict, deque
from pathlib import Path


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


def load_graph(modules_file: Path):
    data = json.loads(modules_file.read_text(encoding="utf-8"))
    modules = {}
    reverse = defaultdict(list)
    seen_paths = {}
    for m in data["modules"]:
        name = m["name"]
        path = m["path"].rstrip("/")
        if name in modules:
            raise ValueError(f"Duplicate module name '{name}' in module graph")
        if path in seen_paths:
            raise ValueError(
                f"Duplicate module path '{path}' used by '{seen_paths[path]}' and '{name}'"
            )

        normalized = {**m, "path": path}
        modules[name] = normalized
        seen_paths[path] = name
        for dep in m.get("deps", []):
            reverse[dep].append(name)
    validate_graph(modules)
    return modules, reverse


def validate_graph(modules: dict) -> None:
    names = set(modules.keys())
    for name, meta in modules.items():
        for dep in meta.get("deps", []):
            if dep not in names:
                raise ValueError(f"Module '{name}' references unknown dependency '{dep}'")

def ensure_acyclic(modules: dict) -> None:
    state = {}  # 0=visiting, 1=done

    def dfs(node: str, chain: list[str]):
        mark = state.get(node)
        if mark == 0:
            cycle_start = chain.index(node)
            cycle = " -> ".join(chain[cycle_start:] + [node])
            raise ValueError(f"Dependency cycle detected: {cycle}")
        if mark == 1:
            return

        state[node] = 0
        for dep in modules[node].get("deps", []):
            dfs(dep, chain + [node])
        state[node] = 1

    for module_name in sorted(modules):
        if module_name not in state:
            dfs(module_name, [])

def detect_modules_from_paths(modules: dict, files: list[str]) -> set[str]:
    impacted = set()
    for f in files:
        for name, meta in modules.items():
            path = meta["path"]
            if f == path or f.startswith(path + "/"):
                impacted.add(name)
    return impacted


def closure_with_dependents(impacted: set[str], reverse: dict) -> set[str]:
    q = deque(impacted)
    seen = set(impacted)
    while q:
        cur = q.popleft()
        for dep in reverse.get(cur, []):
            if dep not in seen:
                seen.add(dep)
                q.append(dep)
    return seen


def main():
    diff_range = os.environ.get("GIT_DIFF_RANGE", "origin/master...HEAD")
    changed_files_raw = run(["git", "diff", "--name-only", diff_range])
    changed_files = changed_files_raw.splitlines() if changed_files_raw else []

    modules, reverse = load_graph(Path("modules.json"))
    impacted = detect_modules_from_paths(modules, changed_files)
    result = closure_with_dependents(impacted, reverse)

    print(",".join(sorted(result)))


if __name__ == "__main__":
    main()
