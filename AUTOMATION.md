# Weekly automation contract

The Codex weekly task attached to this repository must:

1. Read `README.md`, `data/projects.json`, the most recent file under `reports/`, and `scripts/collect.py`.
2. Run the collector for the seven days ending on the task date. Preserve the raw JSON outside Git or as a temporary artifact. Use `GITHUB_TOKEN` when it is already available; never print or persist it. If the API is rate-limited, use official GitHub pages and repository feeds as a bounded fallback and state the missing metadata explicitly.
3. For every tracked project, inspect official GitHub releases, merged/default-branch commits, relevant pull requests, README/docs and benchmark changes.
4. Classify every finding as one of:
   - released;
   - merged to the default branch but not proven released;
   - in development or proposed;
   - documentation/marketing only.
5. Create `reports/YYYY-MM-DD.md` in Chinese. Include a weekly summary, one section per tracked project, an emerging-project radar, next-week watch items, and evidence boundaries.
6. Search GitHub for Agent Memory projects created during the last 120 days. Prioritize unusual star velocity, sustained commit activity, original architecture, papers or reproducible benchmarks. Exclude generic agent frameworks, vector databases and curated lists unless they reveal a concrete memory project.
7. Update `README.md` only when the durable baseline, ranking, architecture, selection guidance or project metadata materially changes. Do not rewrite it merely to mention weekly news.
8. Validate Markdown links and run `python3 -m py_compile scripts/collect.py` plus the repository validation workflow before committing.
9. Commit and push the report and any justified README changes to `main`. If collection, validation or push fails, preserve the evidence and report the failure instead of fabricating a successful update.

Evidence rules:

- Prefer official repositories, releases, documentation and papers.
- Treat vendor benchmark claims as claims unless independently reproduced under the same harness.
- Never infer a feature from a commit subject alone when the implementation or linked PR contradicts it.
- Report Stars as a dated snapshot, not as a quality score.
