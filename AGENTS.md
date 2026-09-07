# AGENTS.md

## Purpose

This repository tracks and stores a self-contained archive of popular AI skill repositories from GitHub.

The archive is intentionally skill-focused:

- Keep every discovered `SKILL.md`.
- Keep recursively related local files referenced by those skills, including scripts, templates, examples, references, assets, and helper files.
- Do not keep unrelated upstream repo files in snapshots.
- Preserve provenance through `archive.json`, the generated catalogs, git history in this repo, and the agent log.

## User Instructions To Preserve

These requirements came directly from the user and should continue to govern future work in this repo:

- Create and maintain a GitHub repository for this archive.
- Add and maintain a detailed README with links to archived skills.
- The goal of the repo is to track and store clones of popular AI skills from engineers on GitHub.
- When the user provides a GitHub link, ingest that source repo.
- Pull all skills from each source repo.
- Store the skill files and all other linked local data needed to make the archived skill self-contained.
- Be ultra thorough when preserving related files.
- Flag duplicates.
- Record source repos.
- Maintain a weekly automation every Sunday afternoon to refresh content from source repos.
- Maintain an append-only agent log of substantive archive operations.
- Reduce snapshots so they only keep skills and related files, not full repo mirrors.
- Keep the repo clean after changes; do not leave long-lived uncommitted archive refreshes around.
- Run archive refreshes directly on `main`; do not create or use feature branches or automation worktrees.

## Key Files

- `scripts/sync_sources.py`: canonical sync/archive/index generator.
- `catalog/sources.json`: source registry.
- `catalog/sources_report.json`: generated per-source sync metadata.
- `catalog/skills.json`: generated skill index.
- `catalog/duplicates.json`: generated duplicate report.
- `catalog/automation.json`: recorded automation intent.
- `README.md`: user-facing repo guide.
- `AGENT_LOG.md`: append-only operational log.

## Snapshot Rules

- Each source repo archives into `archives/<owner>__<repo>/`.
- `archives/<owner>__<repo>/snapshot/` is a reduced snapshot, not a full repo copy.
- A snapshot should contain:
  - every `SKILL.md` discovered in the source repo
  - recursively referenced local files reachable from those skills
- A snapshot should not contain:
  - upstream `.git` data
  - unrelated docs, tests, configs, or packaging files unless they are actually referenced by a retained skill-related file
- `archives/<owner>__<repo>/archive.json` must record the upstream commit and sync metadata.

## Sync Workflow

When adding or refreshing sources:

1. Start from a clean, remote-aligned `main` checkout using `git pull --ff-only origin main`; stop on dirt or divergence instead of stashing or resetting.
2. Update `catalog/sources.json` if a new repo is being added.
3. Run `python3 scripts/sync_sources.py` or `python3 scripts/sync_sources.py add <url>`.
4. Verify the reduced snapshots still contain all skills and their related files.
5. Verify the generated catalogs and README are updated.
6. Verify duplicate detection still makes sense.
7. Append the operation to `AGENT_LOG.md`.
8. Create one focused commit, push it directly to `origin/main`, verify the remote SHA, and leave the worktree clean.

## Duplicate Policy

- Keep duplicate skills in the archive; do not deduplicate by deleting source material.
- Flag exact duplicate content in `catalog/duplicates.json`.
- Flag repeated skill names even when content differs.
- Preserve source provenance for every duplicate entry.

## Automation

- The Codex automation id is `weekly-ai-skills-refresh`.
- Schedule: Sunday at 3:00 PM America/New_York.
- Purpose: refresh all registered sources, rebuild reduced snapshots and catalogs, and append to `AGENT_LOG.md`.
- Branch policy: use the saved local checkout on `main`, never create or use a feature branch or worktree, and publish verified refreshes directly to `origin/main` without a pull request.

## Notes For Future Agents

- Prefer changing `scripts/sync_sources.py` over making manual archive edits.
- If the archive model changes, regenerate snapshots instead of editing archived files by hand.
- Be conservative about deleting source-linked files from snapshots; if a retained file references another local file, keep following the chain recursively.
- If a repo refresh causes a large deletion set, verify that the new reduced snapshot rules explain it before committing.
- Keep explanations concise, but keep the repository metadata thorough.
