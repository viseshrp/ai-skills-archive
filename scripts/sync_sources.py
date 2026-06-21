#!/usr/bin/env python3

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_DIR = REPO_ROOT / "catalog"
ARCHIVES_DIR = REPO_ROOT / "archives"
TEMP_DIR = REPO_ROOT / "tmp_sync"
SOURCES_FILE = CATALOG_DIR / "sources.json"
SKILLS_FILE = CATALOG_DIR / "skills.json"
DUPLICATES_FILE = CATALOG_DIR / "duplicates.json"
SOURCES_REPORT_FILE = CATALOG_DIR / "sources_report.json"
AUTOMATION_FILE = CATALOG_DIR / "automation.json"
AGENT_LOG_FILE = REPO_ROOT / "AGENT_LOG.md"
README_FILE = REPO_ROOT / "README.md"

TEXT_EXTENSIONS = {
    ".json",
    ".md",
    ".mdx",
    ".mjs",
    ".py",
    ".sh",
    ".ps1",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

PATH_TOKEN_RE = re.compile(
    r"(?P<path>(?:\.\.?/|[A-Za-z0-9_-]+/)[^\s'\"`()\[\]<>]+?\.(?:md|mdx|py|mjs|js|json|yaml|yml|toml|sh|ps1|txt))"
)
MD_LINK_RE = re.compile(r"\[[^\]]+\]\((?P<link>[^)]+)\)")
NAME_RE = re.compile(r"^name:\s*[\"']?(.*?)[\"']?\s*$", re.MULTILINE)
DESC_RE = re.compile(r"^description:\s*[\"']?(.*?)[\"']?\s*$", re.MULTILINE)


def run(cmd: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def load_sources() -> list[dict[str, Any]]:
    return json.loads(SOURCES_FILE.read_text())


def ensure_dirs() -> None:
    for path in (CATALOG_DIR, ARCHIVES_DIR, TEMP_DIR):
        path.mkdir(parents=True, exist_ok=True)


def parse_repo_url(url: str) -> tuple[str, str]:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        raise ValueError(f"Unsupported GitHub URL: {url}")
    owner = parts[0]
    repo = parts[1]
    if repo.endswith(".git"):
        repo = repo[:-4]
    return owner, repo


def repo_key(owner: str, repo: str) -> str:
    return f"{owner}__{repo}"


def clone_or_update(url: str, destination: Path) -> None:
    if destination.exists():
        run(["git", "fetch", "--depth", "1", "origin"], cwd=destination)
        default_branch = run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            cwd=destination,
        ).split("/")[-1]
        run(["git", "checkout", default_branch], cwd=destination)
        run(["git", "reset", "--hard", f"origin/{default_branch}"], cwd=destination)
    else:
        run(["git", "clone", "--depth", "1", url, str(destination)])


def copy_repo_snapshot(source: Path, destination: Path) -> dict[str, int]:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)

    file_count = 0
    dir_count = 0
    for root, dirs, files in os.walk(source):
        root_path = Path(root)
        dirs[:] = [d for d in dirs if d != ".git"]
        relative_root = root_path.relative_to(source)
        target_root = destination / relative_root
        target_root.mkdir(parents=True, exist_ok=True)
        dir_count += len(dirs)
        for file_name in files:
            source_file = root_path / file_name
            if ".git" in source_file.parts:
                continue
            target_file = target_root / file_name
            target_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, target_file)
            file_count += 1
    return {"files": file_count, "directories": dir_count}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text_if_possible(path: Path) -> str | None:
    if path.suffix.lower() not in TEXT_EXTENSIONS and path.name != "SKILL.md":
        return None
    try:
        return path.read_text()
    except UnicodeDecodeError:
        return None


def find_linked_paths(skill_path: Path, repo_root: Path) -> list[str]:
    content = skill_path.read_text()
    found: set[str] = set()

    for match in MD_LINK_RE.finditer(content):
        candidate = match.group("link").strip()
        if candidate.startswith(("http://", "https://", "#", "mailto:")):
            continue
        resolved = (skill_path.parent / candidate).resolve()
        if resolved.exists() and resolved.is_file():
            found.add(str(resolved.relative_to(repo_root)))

    for match in PATH_TOKEN_RE.finditer(content):
        candidate = match.group("path")
        resolved = (skill_path.parent / candidate).resolve()
        if resolved.exists() and resolved.is_file():
            found.add(str(resolved.relative_to(repo_root)))

    return sorted(found)


def parse_skill_metadata(skill_path: Path) -> tuple[str, str]:
    content = skill_path.read_text()
    name_match = NAME_RE.search(content)
    desc_match = DESC_RE.search(content)
    skill_name = name_match.group(1).strip() if name_match else skill_path.parent.name
    description = desc_match.group(1).strip() if desc_match else ""
    return skill_name, description


def build_repo_report(source: dict[str, Any], clone_dir: Path, archive_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    owner, repo = parse_repo_url(source["url"])
    branch = run(["git", "branch", "--show-current"], cwd=clone_dir)
    commit = run(["git", "rev-parse", "HEAD"], cwd=clone_dir)
    commit_date = run(["git", "show", "-s", "--format=%cI", "HEAD"], cwd=clone_dir)
    snapshot_dir = archive_root / "snapshot"
    counts = copy_repo_snapshot(clone_dir, snapshot_dir)

    skill_records: list[dict[str, Any]] = []
    for skill_path in sorted(snapshot_dir.rglob("SKILL.md")):
        relative_skill_path = skill_path.relative_to(snapshot_dir)
        skill_name, description = parse_skill_metadata(skill_path)
        skill_text = skill_path.read_text()
        linked_paths = find_linked_paths(skill_path, snapshot_dir)
        skill_records.append(
            {
                "source_repo": f"{owner}/{repo}",
                "repo_key": repo_key(owner, repo),
                "skill_name": skill_name,
                "description": description,
                "path": str(relative_skill_path),
                "relative_directory": str(relative_skill_path.parent),
                "sha256": hashlib.sha256(skill_text.encode("utf-8")).hexdigest(),
                "linked_local_files": linked_paths,
            }
        )

    all_files = [path for path in snapshot_dir.rglob("*") if path.is_file()]
    report = {
        "owner": owner,
        "repo": repo,
        "repo_key": repo_key(owner, repo),
        "url": source["url"],
        "notes": source.get("notes", ""),
        "default_branch": branch,
        "commit": commit,
        "commit_date": commit_date,
        "archived_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "archive_path": str(archive_root.relative_to(REPO_ROOT)),
        "snapshot_path": str(snapshot_dir.relative_to(REPO_ROOT)),
        "file_count": counts["files"],
        "directory_count": counts["directories"],
        "skill_count": len(skill_records),
        "skill_paths": [record["path"] for record in skill_records],
        "all_text_file_hashes": {
            str(path.relative_to(snapshot_dir)): file_sha256(path)
            for path in all_files
            if read_text_if_possible(path) is not None
        },
    }
    return report, skill_records


def build_duplicate_report(skill_records: list[dict[str, Any]]) -> dict[str, Any]:
    by_sha: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_name: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for record in skill_records:
        by_sha[record["sha256"]].append(record)
        by_name[record["skill_name"]].append(record)

    exact_duplicates = []
    for sha, items in sorted(by_sha.items()):
        if len(items) < 2:
            continue
        exact_duplicates.append(
            {
                "sha256": sha,
                "count": len(items),
                "locations": [
                    {
                        "source_repo": item["source_repo"],
                        "path": item["path"],
                    }
                    for item in items
                ],
            }
        )

    repeated_names = []
    for name, items in sorted(by_name.items()):
        if len(items) < 2:
            continue
        repeated_names.append(
            {
                "skill_name": name,
                "count": len(items),
                "locations": [
                    {
                        "source_repo": item["source_repo"],
                        "path": item["path"],
                        "sha256": item["sha256"],
                    }
                    for item in items
                ],
            }
        )

    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "exact_skill_duplicates": exact_duplicates,
        "duplicate_skill_names": repeated_names,
    }


def append_agent_log(message: str, repo_reports: list[dict[str, Any]], duplicate_report: dict[str, Any]) -> None:
    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    exact_duplicate_count = len(duplicate_report["exact_skill_duplicates"])
    duplicate_name_count = len(duplicate_report["duplicate_skill_names"])
    lines = [
        f"## {timestamp}",
        "",
        f"- Action: {message}",
        f"- Sources synced: {len(repo_reports)}",
        f"- Skills indexed: {sum(report['skill_count'] for report in repo_reports)}",
        f"- Exact duplicate groups: {exact_duplicate_count}",
        f"- Repeated skill names: {duplicate_name_count}",
    ]
    for report in repo_reports:
        lines.append(
            f"- Synced `{report['repo_key']}` at commit `{report['commit'][:12]}` with {report['skill_count']} skills and {report['file_count']} files."
        )
    lines.extend(["", ""])
    existing = AGENT_LOG_FILE.read_text() if AGENT_LOG_FILE.exists() else "# Agent Log\n\n"
    AGENT_LOG_FILE.write_text(existing + "\n".join(lines))


def render_readme(repo_reports: list[dict[str, Any]], skill_records: list[dict[str, Any]], duplicate_report: dict[str, Any]) -> str:
    lines = [
        "# AI Skills Archive",
        "",
        "A self-contained archive of popular AI skill repositories from GitHub.",
        "",
        "This repository stores full snapshot copies of source repositories, indexes every discovered `SKILL.md`, records the upstream source metadata, and flags duplicate skills so the archive can grow without losing provenance.",
        "",
        "## Goals",
        "",
        "- Preserve upstream AI skill repositories in a self-contained layout.",
        "- Track source URLs, archived commits, and sync timestamps.",
        "- Index every discovered skill file with links back to the archived snapshot.",
        "- Flag exact duplicate skill content and repeated skill names.",
        "- Support repeatable weekly refreshes and future source additions.",
        "",
        "## Repository Layout",
        "",
        "- `archives/<owner>__<repo>/snapshot/`: full copied snapshot of each upstream repository, excluding upstream `.git` history.",
        "- `archives/<owner>__<repo>/archive.json`: metadata for the archived snapshot.",
        "- `catalog/sources.json`: source registry used by the sync script.",
        "- `catalog/sources_report.json`: generated sync metadata for each source.",
        "- `catalog/skills.json`: generated skill index.",
        "- `catalog/duplicates.json`: generated duplicate report.",
        "- `scripts/sync_sources.py`: refresh/import script for all registered sources.",
        "- `AGENT_LOG.md`: append-only operational log.",
        "",
        "## Source Repositories",
        "",
    ]

    for report in repo_reports:
        lines.extend(
            [
                f"- [{report['owner']}/{report['repo']}]({report['url']})",
                f"  - Archived commit: `{report['commit']}`",
                f"  - Snapshot: [`{report['snapshot_path']}`]({report['snapshot_path']})",
                f"  - Skills discovered: {report['skill_count']}",
                f"  - Files copied: {report['file_count']}",
            ]
        )

    lines.extend(
        [
            "",
            "## Generated Reports",
            "",
            "- [`catalog/sources_report.json`](catalog/sources_report.json): per-source archive metadata, commits, counts, and file hashes.",
            "- [`catalog/skills.json`](catalog/skills.json): discovered skills with source provenance and linked local resources.",
            "- [`catalog/duplicates.json`](catalog/duplicates.json): exact duplicate content groups and repeated skill names.",
            "- [`catalog/automation.json`](catalog/automation.json): recorded weekly automation intent and command.",
            "",
            "## Skill Catalog",
            "",
        ]
    )

    for report in repo_reports:
        lines.append(f"### {report['owner']}/{report['repo']}")
        repo_skills = [record for record in skill_records if record["repo_key"] == report["repo_key"]]
        for record in repo_skills:
            skill_link = f"{report['snapshot_path']}/{record['path']}"
            lines.append(f"- `{record['skill_name']}`: [`{record['path']}`]({skill_link})")
        if not repo_skills:
            lines.append("- No `SKILL.md` files detected.")
        lines.append("")

    lines.extend(
        [
            "## Duplicate Tracking",
            "",
            f"- Exact duplicate groups: {len(duplicate_report['exact_skill_duplicates'])}",
            f"- Repeated skill names: {len(duplicate_report['duplicate_skill_names'])}",
            "- Full report: [`catalog/duplicates.json`](catalog/duplicates.json)",
            "",
            "## Add A Source",
            "",
            "When you provide a new GitHub repository URL, add it with:",
            "",
            "```bash",
            "python3 scripts/sync_sources.py add https://github.com/owner/repo",
            "```",
            "",
            "That command updates `catalog/sources.json`, refreshes every registered source, rebuilds the indexes, and appends a new entry to `AGENT_LOG.md`.",
            "",
            "## Weekly Refresh",
            "",
            "Use `python3 scripts/sync_sources.py` to refresh every registered source. The weekly automation in Codex is configured for Sunday at 3:00 PM America/New_York and appends an entry to `AGENT_LOG.md` every time it updates the archive.",
        ]
    )

    return "\n".join(lines) + "\n"


def write_archive_metadata(report: dict[str, Any]) -> None:
    archive_dir = REPO_ROOT / report["archive_path"]
    (archive_dir / "archive.json").write_text(json.dumps(report, indent=2) + "\n")


def sync_sources(log_note: str) -> None:
    ensure_dirs()
    sources = load_sources()
    repo_reports: list[dict[str, Any]] = []
    skill_records: list[dict[str, Any]] = []

    for source in sources:
        owner, repo = parse_repo_url(source["url"])
        key = repo_key(owner, repo)
        clone_dir = TEMP_DIR / key
        archive_root = ARCHIVES_DIR / key
        clone_or_update(source["url"], clone_dir)
        report, repo_skills = build_repo_report(source, clone_dir, archive_root)
        write_archive_metadata(report)
        repo_reports.append(report)
        skill_records.extend(repo_skills)

    duplicate_report = build_duplicate_report(skill_records)

    SOURCES_REPORT_FILE.write_text(json.dumps(repo_reports, indent=2) + "\n")
    SKILLS_FILE.write_text(json.dumps(skill_records, indent=2) + "\n")
    DUPLICATES_FILE.write_text(json.dumps(duplicate_report, indent=2) + "\n")
    README_FILE.write_text(render_readme(repo_reports, skill_records, duplicate_report))
    append_agent_log(log_note, repo_reports, duplicate_report)


def add_sources(urls: list[str]) -> None:
    sources = load_sources()
    existing_urls = {source["url"] for source in sources}
    added = False
    for url in urls:
        if url in existing_urls:
            continue
        sources.append(
            {
                "url": url,
                "notes": "Added with scripts/sync_sources.py add.",
            }
        )
        added = True
    if added:
        SOURCES_FILE.write_text(json.dumps(sources, indent=2) + "\n")


def write_automation_manifest() -> None:
    payload = {
        "name": "Weekly AI Skills Refresh",
        "schedule_local_time": "Every Sunday at 3:00 PM America/New_York",
        "purpose": "Refresh archived skill repositories, regenerate indexes, and append to AGENT_LOG.md.",
        "command": "python3 scripts/sync_sources.py --log-note 'Weekly automation refresh'",
    }
    AUTOMATION_FILE.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("urls", nargs="+")

    parser.add_argument(
        "--log-note",
        default="Manual sync run",
        help="Text appended to the agent log for this sync run.",
    )

    args = parser.parse_args()
    ensure_dirs()
    write_automation_manifest()

    if args.command == "add":
        add_sources(args.urls)
        sync_sources(f"Added source(s): {', '.join(args.urls)}")
        return

    sync_sources(args.log_note)


if __name__ == "__main__":
    main()
