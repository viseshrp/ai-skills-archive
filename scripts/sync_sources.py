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
from collections import deque
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
    ".cjs",
    ".cmd",
    ".css",
    ".dot",
    ".gif",
    ".html",
    ".jpeg",
    ".jpg",
    ".json",
    ".md",
    ".mdx",
    ".mjs",
    ".js",
    ".pdf",
    ".png",
    ".py",
    ".sh",
    ".svg",
    ".tex",
    ".ts",
    ".tsx",
    ".ps1",
    ".toml",
    ".txt",
    ".webp",
    ".yaml",
    ".yml",
}

PATH_TOKEN_RE = re.compile(
    r"(?P<path>(?:\.\.?/)?(?:[A-Za-z0-9._-]+/)+[A-Za-z0-9._-]+(?:\.(?:md|mdx|txt|json|ya?ml|toml|py|sh|ps1|js|mjs|cjs|ts|tsx|html|css|svg|png|jpg|jpeg|gif|webp|pdf|tex|dot|cmd))?)"
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
    return json.loads(SOURCES_FILE.read_text(encoding="utf-8"))


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


def canonical_repo_url(url: str) -> str:
    owner, repo = parse_repo_url(url)
    return f"https://github.com/{owner}/{repo}"


def repo_key(owner: str, repo: str) -> str:
    return f"{owner}__{repo}"


def repo_relpath(path: Path) -> str:
    return path.as_posix()


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


def copy_selected_files(source: Path, destination: Path, selected_files: set[Path]) -> dict[str, int]:
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)

    for relative_path in sorted(selected_files):
        target_file = destination / relative_path
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / relative_path, target_file)

    directories = {path.parent for path in selected_files if path.parent != Path(".")}
    return {"files": len(selected_files), "directories": len(directories)}


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
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def normalize_reference(candidate: str) -> str:
    return candidate.strip().strip("'\"`").split("#", 1)[0].split("?", 1)[0].rstrip(".,:;")


def resolve_local_reference(base_path: Path, repo_root: Path, candidate: str) -> Path | None:
    candidate = normalize_reference(candidate)
    if not candidate or candidate.startswith(("http://", "https://", "#", "mailto:", "data:")):
        return None

    resolved = (base_path.parent / candidate).resolve()
    try:
        resolved.relative_to(repo_root)
    except ValueError:
        return None
    if not resolved.exists() or not resolved.is_file() or ".git" in resolved.parts:
        return None
    return resolved


def extract_local_file_refs(path: Path, repo_root: Path) -> list[Path]:
    content = read_text_if_possible(path)
    if content is None:
        return []

    found: set[Path] = set()
    for match in MD_LINK_RE.finditer(content):
        resolved = resolve_local_reference(path, repo_root, match.group("link"))
        if resolved is not None:
            found.add(resolved)

    for match in PATH_TOKEN_RE.finditer(content):
        resolved = resolve_local_reference(path, repo_root, match.group("path"))
        if resolved is not None:
            found.add(resolved)

    return sorted(found)


def collect_related_files(start_path: Path, repo_root: Path) -> list[str]:
    queue: deque[Path] = deque([start_path])
    visited_text_files: set[Path] = set()
    related_files: set[Path] = set()

    while queue:
        current = queue.popleft()
        if current in visited_text_files:
            continue
        visited_text_files.add(current)
        for linked_path in extract_local_file_refs(current, repo_root):
            if linked_path == start_path:
                continue
            if linked_path not in related_files:
                related_files.add(linked_path)
            if read_text_if_possible(linked_path) is not None:
                queue.append(linked_path)

    return sorted(repo_relpath(path.relative_to(repo_root)) for path in related_files)


def parse_skill_metadata(skill_path: Path) -> tuple[str, str]:
    content = skill_path.read_text(encoding="utf-8")
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
    source_skill_paths = sorted(
        path for path in clone_dir.rglob("SKILL.md") if ".git" not in path.parts
    )

    selected_files: set[Path] = set()
    skill_records: list[dict[str, Any]] = []
    for skill_path in source_skill_paths:
        relative_skill_path = skill_path.relative_to(clone_dir)
        related_paths = collect_related_files(skill_path, clone_dir)
        selected_files.add(relative_skill_path)
        selected_files.update(Path(path) for path in related_paths)
        skill_name, description = parse_skill_metadata(skill_path)
        skill_text = skill_path.read_text(encoding="utf-8")
        skill_records.append(
            {
                "source_repo": f"{owner}/{repo}",
                "repo_key": repo_key(owner, repo),
                "skill_name": skill_name,
                "description": description,
                "path": repo_relpath(relative_skill_path),
                "relative_directory": repo_relpath(relative_skill_path.parent),
                "sha256": hashlib.sha256(skill_text.encode("utf-8")).hexdigest(),
                "linked_local_files": related_paths,
            }
        )

    counts = copy_selected_files(clone_dir, snapshot_dir, selected_files)
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
        "archive_path": repo_relpath(archive_root.relative_to(REPO_ROOT)),
        "snapshot_path": repo_relpath(snapshot_dir.relative_to(REPO_ROOT)),
        "file_count": counts["files"],
        "directory_count": counts["directories"],
        "skill_count": len(skill_records),
        "snapshot_mode": "skills-and-related-files-only",
        "skill_paths": [record["path"] for record in skill_records],
        "all_text_file_hashes": {
            repo_relpath(path.relative_to(snapshot_dir)): file_sha256(path)
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
    existing = (
        AGENT_LOG_FILE.read_text(encoding="utf-8")
        if AGENT_LOG_FILE.exists()
        else "# Agent Log\n\n"
    )
    AGENT_LOG_FILE.write_text(existing + "\n".join(lines), encoding="utf-8")


def render_readme(repo_reports: list[dict[str, Any]], skill_records: list[dict[str, Any]], duplicate_report: dict[str, Any]) -> str:
    lines = [
        "# AI Skills Archive",
        "",
        "A self-contained archive of popular AI skill repositories from GitHub.",
        "",
        "This repository stores reduced snapshots that keep every discovered `SKILL.md` plus recursively linked local resources, records the upstream source metadata, and flags duplicate skills so the archive can grow without losing provenance.",
        "",
        "## Goals",
        "",
        "- Preserve upstream AI skill repositories in a self-contained, skill-focused layout.",
        "- Track source URLs, archived commits, and sync timestamps.",
        "- Index every discovered skill file with links back to the archived snapshot.",
        "- Flag exact duplicate skill content and repeated skill names.",
        "- Support repeatable weekly refreshes and future source additions.",
        "",
        "## Repository Layout",
        "",
        "- `archives/<owner>__<repo>/snapshot/`: reduced snapshot containing only `SKILL.md` files and recursively related local resources, excluding upstream `.git` history and unrelated repo files.",
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
                f"  - Files retained in reduced snapshot: {report['file_count']}",
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
    (archive_dir / "archive.json").write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )


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

    SOURCES_REPORT_FILE.write_text(
        json.dumps(repo_reports, indent=2) + "\n",
        encoding="utf-8",
    )
    SKILLS_FILE.write_text(
        json.dumps(skill_records, indent=2) + "\n",
        encoding="utf-8",
    )
    DUPLICATES_FILE.write_text(
        json.dumps(duplicate_report, indent=2) + "\n",
        encoding="utf-8",
    )
    README_FILE.write_text(
        render_readme(repo_reports, skill_records, duplicate_report),
        encoding="utf-8",
    )
    append_agent_log(log_note, repo_reports, duplicate_report)


def add_sources(urls: list[str]) -> None:
    sources = load_sources()
    existing_urls = {source["url"] for source in sources}
    added = False
    for url in urls:
        canonical_url = canonical_repo_url(url)
        if canonical_url in existing_urls:
            continue
        sources.append(
            {
                "url": canonical_url,
                "notes": f"Added with scripts/sync_sources.py add from {url}.",
            }
        )
        added = True
    if added:
        SOURCES_FILE.write_text(json.dumps(sources, indent=2) + "\n", encoding="utf-8")


def write_automation_manifest() -> None:
    payload = {
        "name": "Weekly AI Skills Refresh",
        "schedule_local_time": "Every Sunday at 3:00 PM America/New_York",
        "purpose": "Refresh archived skill repositories, regenerate indexes, and append to AGENT_LOG.md.",
        "command": "python3 scripts/sync_sources.py --log-note 'Weekly automation refresh'",
    }
    AUTOMATION_FILE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


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
