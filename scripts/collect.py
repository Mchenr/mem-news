#!/usr/bin/env python3
"""Collect a reproducible GitHub snapshot for the mem-news weekly report.

The script intentionally performs collection, not editorial ranking. A human or
agent should read the linked changes and turn the raw snapshot into a bounded
weekly analysis before committing it.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import sys
import time
from typing import Dict, List, Optional, Union
import urllib.error
import urllib.parse
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parents[1]
PROJECTS_FILE = ROOT / "data" / "projects.json"
API_ROOT = "https://api.github.com"
USER_AGENT = "mem-news-collector/1.0"


def api_get(
    path: str,
    params: Optional[Dict[str, Union[str, int]]] = None,
    attempts: int = 3,
):
    url = f"{API_ROOT}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code == 403 and "rate limit" in detail.lower():
                reset = exc.headers.get("X-RateLimit-Reset", "unknown")
                raise RuntimeError(
                    "GitHub API rate limit exceeded for "
                    f"{url}; reset={reset}. Set GITHUB_TOKEN or use the "
                    "official-page fallback documented in AUTOMATION.md."
                ) from exc
            if exc.code not in {429, 500, 502, 503, 504} or attempt == attempts:
                raise RuntimeError(
                    f"GitHub API {exc.code} for {url}: {detail}"
                ) from exc
        except urllib.error.URLError as exc:
            if attempt == attempts:
                raise RuntimeError(f"GitHub API network error for {url}: {exc}") from exc
        time.sleep(2 ** (attempt - 1))
    raise AssertionError("unreachable")


def load_projects() -> List[Dict[str, str]]:
    with PROJECTS_FILE.open(encoding="utf-8") as handle:
        return json.load(handle)["projects"]


def collect_project(project: Dict[str, str], since: str) -> dict:
    repo = project["repo"]
    metadata = api_get(f"/repos/{repo}")
    if not metadata:
        raise RuntimeError(f"Repository not found: {repo}")
    release = api_get(f"/repos/{repo}/releases/latest") or {}
    commits = api_get(
        f"/repos/{repo}/commits",
        {"since": f"{since}T00:00:00Z", "per_page": 30},
    ) or []
    return {
        "name": project["name"],
        "repo": repo,
        "url": metadata["html_url"],
        "description": metadata.get("description"),
        "category": project["category"],
        "stars": metadata["stargazers_count"],
        "forks": metadata["forks_count"],
        "open_issues": metadata["open_issues_count"],
        "license": (metadata.get("license") or {}).get("spdx_id") or "unknown",
        "pushed_at": metadata.get("pushed_at"),
        "latest_release": {
            "tag": release.get("tag_name"),
            "published_at": release.get("published_at"),
            "url": release.get("html_url"),
        },
        "commits": [
            {
                "sha": item["sha"][:7],
                "date": item["commit"]["author"]["date"],
                "subject": item["commit"]["message"].splitlines()[0],
                "url": item["html_url"],
            }
            for item in commits
        ],
    }


def search_emerging(today: dt.date) -> List[dict]:
    created_after = today - dt.timedelta(days=120)
    queries = [
        f'"agent memory" in:name,description,readme created:>{created_after} stars:>100',
        f'"memory layer" agent in:name,description,readme created:>{created_after} stars:>100',
        f"topic:agent-memory created:>{created_after} stars:>100",
    ]
    found: Dict[str, dict] = {}
    for query in queries:
        result = api_get(
            "/search/repositories",
            {"q": query, "sort": "stars", "order": "desc", "per_page": 20},
        ) or {}
        for item in result.get("items", []):
            found[item["full_name"]] = {
                "repo": item["full_name"],
                "url": item["html_url"],
                "description": item.get("description"),
                "stars": item["stargazers_count"],
                "created_at": item["created_at"],
                "pushed_at": item["pushed_at"],
            }
    tracked = {item["repo"] for item in load_projects()}
    candidates = [item for key, item in found.items() if key not in tracked]
    return sorted(candidates, key=lambda item: item["stars"], reverse=True)


def render_markdown(snapshot: dict) -> str:
    lines = [
        f"# Agent Memory 周报原始快照：{snapshot['date']}",
        "",
        f"采集区间：{snapshot['since']} 至 {snapshot['date']}。",
        "",
        "> 本文件由脚本生成，只证明 GitHub 元数据和提交记录；提交主题不等于已发布特性。发布前必须阅读相关 PR、Release 和文档并补充编辑判断。",
        "",
        "## 固定跟踪项目",
        "",
    ]
    for project in snapshot["projects"]:
        release = project["latest_release"]
        release_text = release["tag"] or "无 GitHub Release"
        if release.get("url"):
            release_text = f"[{release_text}]({release['url']})"
        lines.extend(
            [
                f"### [{project['name']}]({project['url']})",
                "",
                f"- Stars/Forks：{project['stars']:,} / {project['forks']:,}",
                f"- 最新 Release：{release_text}",
                f"- 最近推送：{project['pushed_at']}",
                f"- 区间内提交数（最多采集 30）：{len(project['commits'])}",
                "",
            ]
        )
        for commit in project["commits"][:10]:
            lines.append(
                f"- [{commit['sha']}]({commit['url']}) {commit['date'][:10]} — {commit['subject']}"
            )
        if not project["commits"]:
            lines.append("- 本区间未观察到默认分支提交。")
        lines.append("")
    lines.extend(["## 新兴项目候选", ""])
    for item in snapshot["emerging"][:20]:
        lines.append(
            f"- [{item['repo']}]({item['url']}) — {item['stars']:,} Stars；创建于 {item['created_at'][:10]}；{item['description'] or '无描述'}"
        )
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    today = dt.date.today()
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=today.isoformat(), help="snapshot date (YYYY-MM-DD)")
    parser.add_argument(
        "--since",
        default=(today - dt.timedelta(days=7)).isoformat(),
        help="inclusive collection start date (YYYY-MM-DD)",
    )
    parser.add_argument("--output", type=pathlib.Path, help="Markdown output path")
    parser.add_argument("--json-output", type=pathlib.Path, help="JSON output path")
    parser.add_argument(
        "--project",
        action="append",
        help="collect only this project name or owner/repo; repeat as needed",
    )
    parser.add_argument(
        "--skip-emerging",
        action="store_true",
        help="skip GitHub repository search (useful for a low-rate-limit smoke test)",
    )
    parser.add_argument("--force", action="store_true", help="overwrite existing outputs")
    return parser.parse_args()


def write_new(path: pathlib.Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise RuntimeError(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    snapshot_date = dt.date.fromisoformat(args.date)
    dt.date.fromisoformat(args.since)
    projects = load_projects()
    if args.project:
        selected = {value.lower() for value in args.project}
        projects = [
            project
            for project in projects
            if project["name"].lower() in selected
            or project["repo"].lower() in selected
        ]
        if not projects:
            raise RuntimeError(f"No tracked project matched: {', '.join(args.project)}")
    snapshot = {
        "schema_version": 1,
        "date": args.date,
        "since": args.since,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "projects": [collect_project(project, args.since) for project in projects],
        "emerging": [] if args.skip_emerging else search_emerging(snapshot_date),
    }
    markdown = render_markdown(snapshot)
    if args.output:
        write_new(args.output, markdown, args.force)
    else:
        sys.stdout.write(markdown)
    if args.json_output:
        write_new(
            args.json_output,
            json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
            args.force,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
