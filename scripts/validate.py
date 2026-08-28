#!/usr/bin/env python3
"""Fast, offline structural checks for mem-news."""

from __future__ import annotations

import json
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    readme_path = ROOT / "README.md"
    projects_path = ROOT / "data" / "projects.json"
    reports_dir = ROOT / "reports"
    if not readme_path.is_file() or not projects_path.is_file():
        fail("README.md or data/projects.json is missing")

    readme = readme_path.read_text(encoding="utf-8")
    data = json.loads(projects_path.read_text(encoding="utf-8"))
    projects = data.get("projects", [])
    if len(projects) != 10:
        fail(f"expected exactly 10 tracked projects, found {len(projects)}")

    names: set[str] = set()
    repos: set[str] = set()
    for project in projects:
        name = project.get("name")
        repo = project.get("repo")
        if not name or not repo or "/" not in repo:
            fail(f"invalid project entry: {project!r}")
        if name in names or repo.lower() in repos:
            fail(f"duplicate project entry: {name} / {repo}")
        names.add(name)
        repos.add(repo.lower())
        if f"github.com/{repo}" not in readme:
            fail(f"README does not link tracked repository {repo}")

    reports = sorted(reports_dir.glob("????-??-??.md"))
    if not reports:
        fail("no dated weekly report found")
    latest = reports[-1]
    if f"reports/{latest.name}" not in readme:
        fail(f"README latest-report link does not point to {latest.name}")

    for markdown in [readme_path, *reports]:
        content = markdown.read_text(encoding="utf-8")
        if "TODO" in content or "TBD" in content:
            fail(f"unfinished marker in {markdown.relative_to(ROOT)}")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
            if target.startswith(("https://", "http://", "#")):
                continue
            local_target = (markdown.parent / target.split("#", 1)[0]).resolve()
            if not local_target.exists():
                fail(
                    f"broken local link in {markdown.relative_to(ROOT)}: {target}"
                )

    print(f"Validated {len(projects)} projects and {len(reports)} report(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
