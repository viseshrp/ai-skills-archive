# AGENTS.md

## Purpose

This repository tracks and stores a self-contained archive of popular AI skill repositories from GitHub and clearly attributed, locally maintained adaptations of selected skills.

The archive is intentionally skill-focused:

- Keep every discovered `SKILL.md`.
- Keep recursively related local files referenced by those skills, including scripts, templates, examples, references, assets, and helper files.
- Do not keep unrelated upstream repo files in snapshots.
- Preserve provenance through `archive.json`, the generated catalogs, git history in this repo, and the agent log.
- Keep adapted skills under `skills/`; never edit an upstream snapshot to create a local variant.

## User Instructions To Preserve

These requirements came directly from the user and should continue to govern future work in this repo:

- Create and maintain a GitHub repository for this archive.
- Add and maintain a detailed README with links to archived skills.
- The goal of the repo is to track and store clones of popular AI skills from engineers on GitHub.
- When the user provides a GitHub link for archival, ingest that source repo.
- Pull all skills from each archived source repo.
- When the user requests a modified version of one linked skill, keep it as a curated adaptation under `skills/` instead of altering a snapshot or importing unrelated skills.
- Store the skill files and all other linked local data needed to make the archived skill self-contained.
- Be ultra thorough when preserving related files.
- Flag duplicates.
- Record source repos.
- Maintain a weekly automation every Sunday afternoon to refresh content from source repos.
- Maintain an append-only agent log of substantive archive operations.
- Reduce snapshots so they only keep skills and related files, not full repo mirrors.
- Keep the repo clean after changes; do not leave long-lived uncommitted archive refreshes around.
- Publish archive refreshes directly to `main`; preserve dirty owner work by using an isolated publication checkout when needed, without feature branches or pull requests.

## Key Files

- `scripts/sync_sources.py`: canonical sync/archive/index generator.
- `skills/`: curated adaptations maintained in this repository, with pinned source and license attribution.
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

## Curated Adaptation Rules

- Use `skills/<skill-name>/` when the user asks for a modified version of a specific upstream skill rather than a byte-preserving source archive.
- Record a pinned upstream file URL, the adaptation scope, and the upstream license in the skill package.
- Keep the adapted skill generic unless the user asks for a narrower target. Put substantial language-specific guidance in clearly labeled sections.
- Do not place adaptations under `archives/`; those paths are regenerated from upstream sources.
- Run `python3 scripts/sync_sources.py --log-note '<note>' reindex-curated` after adding or changing an adapted skill so catalogs, duplicate reports, README, and the agent log stay synchronized without refreshing unrelated upstream sources.

## Sync Workflow

When adding or refreshing sources:

1. Record original owner/index state and verify `origin/main`. Continue with dirty, overlapping, divergent, or differently checked-out owner work by automatically using an isolated remote-aligned publication checkout. Never stash, reset, or commit owner work to clean up.
2. Update `catalog/sources.json` if a new repo is being added.
3. Run `python3 scripts/sync_sources.py` or `python3 scripts/sync_sources.py add <url>`.
4. Verify the reduced snapshots still contain all skills and their related files.
5. Verify the generated catalogs and README are updated.
6. Verify duplicate detection still makes sense.
7. Append the operation to `AGENT_LOG.md`.
8. Create one focused published commit, push it directly to `origin/main`, verify the remote SHA in the publication checkout, and preserve original owner state. Recover failed publication attempts safely.

For a curated adaptation, replace steps 2-4 with adding or updating `skills/<skill-name>/` and running the `reindex-curated` command above. Validate the skill before committing.

## Duplicate Policy

- Keep duplicate skills in the archive and curated collection; do not deduplicate by deleting source material.
- Flag exact duplicate content in `catalog/duplicates.json`.
- Flag repeated skill names even when content differs.
- Preserve source provenance for every duplicate entry.

## Automation

- The Codex automation id is `weekly-ai-skills-refresh`.
- Schedule: Sunday at 3:00 PM America/New_York.
- Purpose: refresh all registered sources, rebuild reduced snapshots and catalogs, and append to `AGENT_LOG.md`.
- Branch policy: publish verified refreshes directly to `origin/main` without a pull request. Isolated publication checkouts are authorized when necessary to preserve dirty owner state or recover concurrency; do not switch the owner's branch.

## Notes For Future Agents

- Prefer changing `scripts/sync_sources.py` over making manual archive edits.
- Keep curated adaptations narrow and source-attributed; preserve upstream snapshots separately when a full source import is requested.
- If the archive model changes, regenerate snapshots instead of editing archived files by hand.
- Be conservative about deleting source-linked files from snapshots; if a retained file references another local file, keep following the chain recursively.
- If a repo refresh causes a large deletion set, verify that the new reduced snapshot rules explain it before committing.
- Keep explanations concise, but keep the repository metadata thorough.

## Scheduled automation ownership and recovery

The user's October 28, 2026 instruction takes precedence over earlier
clean-worktree or original-checkout-only automation rules. Dirty working
directories never block scheduled jobs. Automations must commit and push their
own validated changes without committing or rearranging pre-existing work.

- Record the original branch, HEAD, index entries, and owner file hashes.
  Preserve staged, unstaged, untracked, overlapping, private, and live state.
- Use exact owned paths or hunks only. A path that already contains owner edits
  is not wholly owned by the job. If existing staging, overlap, another branch,
  divergence, or concurrent publication complicates separation, automatically
  use an isolated checkout at the verified remote destination and run the job
  there. Its registered output paths are relative to that checkout. Do not
  require the original checkout to be clean or synchronized before proceeding.
- Never stash, reset, clean, move owner files out of the way, stage everything,
  or commit pre-existing work to satisfy a preflight check. Review and validate
  only the job's complete delta, commit it, and push the configured destination.
- Recover a rejected push by fetching the destination in an isolated checkout,
  reapplying only the owned delta, reconciling concurrent append-only changes,
  rerunning affected checks, and retrying normally. Never force-push or alter
  owner history. Verify the published checkout and live remote SHA, required
  CI, and original owner-state preservation; failed attempts may be retried.
- Diagnose and fix recoverable failures within the job's existing scope, then
  rerun validation and finish publication. A missing credential or unavailable
  source fact cannot be invented: report that precise external prerequisite
  and finish independent valid work. Preserve source permissions, privacy,
  validation, no-execution rules, and no-change behavior. Record reusable
  symptom/cause/fix/verification evidence in the existing job continuity files.
