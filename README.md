# AI Skills Archive

A self-contained archive of popular AI skill repositories from GitHub.

This repository stores full snapshot copies of source repositories, indexes every discovered `SKILL.md`, records the upstream source metadata, and flags duplicate skills so the archive can grow without losing provenance.

## Goals

- Preserve upstream AI skill repositories in a self-contained layout.
- Track source URLs, archived commits, and sync timestamps.
- Index every discovered skill file with links back to the archived snapshot.
- Flag exact duplicate skill content and repeated skill names.
- Support repeatable weekly refreshes and future source additions.

## Repository Layout

- `archives/<owner>__<repo>/snapshot/`: full copied snapshot of each upstream repository, excluding upstream `.git` history.
- `archives/<owner>__<repo>/archive.json`: metadata for the archived snapshot.
- `catalog/sources.json`: source registry used by the sync script.
- `catalog/sources_report.json`: generated sync metadata for each source.
- `catalog/skills.json`: generated skill index.
- `catalog/duplicates.json`: generated duplicate report.
- `scripts/sync_sources.py`: refresh/import script for all registered sources.
- `AGENT_LOG.md`: append-only operational log.

## Source Repositories

- [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
  - Archived commit: `17214a29c429a19f7a9607f2c06f9d650ea87eb0`
  - Snapshot: [`archives/addyosmani__agent-skills/snapshot`](archives/addyosmani__agent-skills/snapshot)
  - Skills discovered: 24
  - Files copied: 93
- [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)
  - Archived commit: `2c606141936f1eeef17fa3043a72095b4765b9c2`
  - Snapshot: [`archives/multica-ai__andrej-karpathy-skills/snapshot`](archives/multica-ai__andrej-karpathy-skills/snapshot)
  - Skills discovered: 1
  - Files copied: 9
- [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills)
  - Archived commit: `c22c17eed8a5753aa60681be9734919f2e2f5b42`
  - Snapshot: [`archives/Imbad0202__academic-research-skills/snapshot`](archives/Imbad0202__academic-research-skills/snapshot)
  - Skills discovered: 4
  - Files copied: 1027
- [mattpocock/skills](https://github.com/mattpocock/skills)
  - Archived commit: `6eeb81b5fcfeeb5bd531dd47ab2f9f2bbea27461`
  - Snapshot: [`archives/mattpocock__skills/snapshot`](archives/mattpocock__skills/snapshot)
  - Skills discovered: 34
  - Files copied: 84
- [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman)
  - Archived commit: `25d22f864ad68cc447a4cb93aefde918aa4aec9f`
  - Snapshot: [`archives/juliusbrussee__caveman/snapshot`](archives/juliusbrussee__caveman/snapshot)
  - Skills discovered: 11
  - Files copied: 148

## Generated Reports

- [`catalog/sources_report.json`](catalog/sources_report.json): per-source archive metadata, commits, counts, and file hashes.
- [`catalog/skills.json`](catalog/skills.json): discovered skills with source provenance and linked local resources.
- [`catalog/duplicates.json`](catalog/duplicates.json): exact duplicate content groups and repeated skill names.
- [`catalog/automation.json`](catalog/automation.json): recorded weekly automation intent and command.

## Skill Catalog

### addyosmani/agent-skills
- `api-and-interface-design`: [`skills/api-and-interface-design/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/api-and-interface-design/SKILL.md)
- `browser-testing-with-devtools`: [`skills/browser-testing-with-devtools/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/browser-testing-with-devtools/SKILL.md)
- `ci-cd-and-automation`: [`skills/ci-cd-and-automation/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/ci-cd-and-automation/SKILL.md)
- `code-review-and-quality`: [`skills/code-review-and-quality/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/code-review-and-quality/SKILL.md)
- `code-simplification`: [`skills/code-simplification/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/code-simplification/SKILL.md)
- `context-engineering`: [`skills/context-engineering/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/context-engineering/SKILL.md)
- `debugging-and-error-recovery`: [`skills/debugging-and-error-recovery/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/debugging-and-error-recovery/SKILL.md)
- `deprecation-and-migration`: [`skills/deprecation-and-migration/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/deprecation-and-migration/SKILL.md)
- `documentation-and-adrs`: [`skills/documentation-and-adrs/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/documentation-and-adrs/SKILL.md)
- `doubt-driven-development`: [`skills/doubt-driven-development/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/doubt-driven-development/SKILL.md)
- `frontend-ui-engineering`: [`skills/frontend-ui-engineering/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/frontend-ui-engineering/SKILL.md)
- `git-workflow-and-versioning`: [`skills/git-workflow-and-versioning/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/git-workflow-and-versioning/SKILL.md)
- `idea-refine`: [`skills/idea-refine/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/idea-refine/SKILL.md)
- `incremental-implementation`: [`skills/incremental-implementation/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/incremental-implementation/SKILL.md)
- `interview-me`: [`skills/interview-me/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/interview-me/SKILL.md)
- `observability-and-instrumentation`: [`skills/observability-and-instrumentation/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/observability-and-instrumentation/SKILL.md)
- `performance-optimization`: [`skills/performance-optimization/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/performance-optimization/SKILL.md)
- `planning-and-task-breakdown`: [`skills/planning-and-task-breakdown/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/planning-and-task-breakdown/SKILL.md)
- `security-and-hardening`: [`skills/security-and-hardening/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/security-and-hardening/SKILL.md)
- `shipping-and-launch`: [`skills/shipping-and-launch/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/shipping-and-launch/SKILL.md)
- `source-driven-development`: [`skills/source-driven-development/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/source-driven-development/SKILL.md)
- `spec-driven-development`: [`skills/spec-driven-development/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/spec-driven-development/SKILL.md)
- `test-driven-development`: [`skills/test-driven-development/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/test-driven-development/SKILL.md)
- `using-agent-skills`: [`skills/using-agent-skills/SKILL.md`](archives/addyosmani__agent-skills/snapshot/skills/using-agent-skills/SKILL.md)

### multica-ai/andrej-karpathy-skills
- `karpathy-guidelines`: [`skills/karpathy-guidelines/SKILL.md`](archives/multica-ai__andrej-karpathy-skills/snapshot/skills/karpathy-guidelines/SKILL.md)

### Imbad0202/academic-research-skills
- `academic-paper`: [`academic-paper/SKILL.md`](archives/Imbad0202__academic-research-skills/snapshot/academic-paper/SKILL.md)
- `academic-paper-reviewer`: [`academic-paper-reviewer/SKILL.md`](archives/Imbad0202__academic-research-skills/snapshot/academic-paper-reviewer/SKILL.md)
- `academic-pipeline`: [`academic-pipeline/SKILL.md`](archives/Imbad0202__academic-research-skills/snapshot/academic-pipeline/SKILL.md)
- `deep-research`: [`deep-research/SKILL.md`](archives/Imbad0202__academic-research-skills/snapshot/deep-research/SKILL.md)

### mattpocock/skills
- `design-an-interface`: [`skills/deprecated/design-an-interface/SKILL.md`](archives/mattpocock__skills/snapshot/skills/deprecated/design-an-interface/SKILL.md)
- `qa`: [`skills/deprecated/qa/SKILL.md`](archives/mattpocock__skills/snapshot/skills/deprecated/qa/SKILL.md)
- `request-refactor-plan`: [`skills/deprecated/request-refactor-plan/SKILL.md`](archives/mattpocock__skills/snapshot/skills/deprecated/request-refactor-plan/SKILL.md)
- `ubiquitous-language`: [`skills/deprecated/ubiquitous-language/SKILL.md`](archives/mattpocock__skills/snapshot/skills/deprecated/ubiquitous-language/SKILL.md)
- `ask-matt`: [`skills/engineering/ask-matt/SKILL.md`](archives/mattpocock__skills/snapshot/skills/engineering/ask-matt/SKILL.md)
- `codebase-design`: [`skills/engineering/codebase-design/SKILL.md`](archives/mattpocock__skills/snapshot/skills/engineering/codebase-design/SKILL.md)
- `diagnosing-bugs`: [`skills/engineering/diagnosing-bugs/SKILL.md`](archives/mattpocock__skills/snapshot/skills/engineering/diagnosing-bugs/SKILL.md)
- `domain-modeling`: [`skills/engineering/domain-modeling/SKILL.md`](archives/mattpocock__skills/snapshot/skills/engineering/domain-modeling/SKILL.md)
- `grill-with-docs`: [`skills/engineering/grill-with-docs/SKILL.md`](archives/mattpocock__skills/snapshot/skills/engineering/grill-with-docs/SKILL.md)
- `implement`: [`skills/engineering/implement/SKILL.md`](archives/mattpocock__skills/snapshot/skills/engineering/implement/SKILL.md)
- `improve-codebase-architecture`: [`skills/engineering/improve-codebase-architecture/SKILL.md`](archives/mattpocock__skills/snapshot/skills/engineering/improve-codebase-architecture/SKILL.md)
- `prototype`: [`skills/engineering/prototype/SKILL.md`](archives/mattpocock__skills/snapshot/skills/engineering/prototype/SKILL.md)
- `resolving-merge-conflicts`: [`skills/engineering/resolving-merge-conflicts/SKILL.md`](archives/mattpocock__skills/snapshot/skills/engineering/resolving-merge-conflicts/SKILL.md)
- `setup-matt-pocock-skills`: [`skills/engineering/setup-matt-pocock-skills/SKILL.md`](archives/mattpocock__skills/snapshot/skills/engineering/setup-matt-pocock-skills/SKILL.md)
- `tdd`: [`skills/engineering/tdd/SKILL.md`](archives/mattpocock__skills/snapshot/skills/engineering/tdd/SKILL.md)
- `to-issues`: [`skills/engineering/to-issues/SKILL.md`](archives/mattpocock__skills/snapshot/skills/engineering/to-issues/SKILL.md)
- `to-prd`: [`skills/engineering/to-prd/SKILL.md`](archives/mattpocock__skills/snapshot/skills/engineering/to-prd/SKILL.md)
- `triage`: [`skills/engineering/triage/SKILL.md`](archives/mattpocock__skills/snapshot/skills/engineering/triage/SKILL.md)
- `decision-mapping`: [`skills/in-progress/decision-mapping/SKILL.md`](archives/mattpocock__skills/snapshot/skills/in-progress/decision-mapping/SKILL.md)
- `review`: [`skills/in-progress/review/SKILL.md`](archives/mattpocock__skills/snapshot/skills/in-progress/review/SKILL.md)
- `writing-beats`: [`skills/in-progress/writing-beats/SKILL.md`](archives/mattpocock__skills/snapshot/skills/in-progress/writing-beats/SKILL.md)
- `writing-fragments`: [`skills/in-progress/writing-fragments/SKILL.md`](archives/mattpocock__skills/snapshot/skills/in-progress/writing-fragments/SKILL.md)
- `writing-shape`: [`skills/in-progress/writing-shape/SKILL.md`](archives/mattpocock__skills/snapshot/skills/in-progress/writing-shape/SKILL.md)
- `git-guardrails-claude-code`: [`skills/misc/git-guardrails-claude-code/SKILL.md`](archives/mattpocock__skills/snapshot/skills/misc/git-guardrails-claude-code/SKILL.md)
- `migrate-to-shoehorn`: [`skills/misc/migrate-to-shoehorn/SKILL.md`](archives/mattpocock__skills/snapshot/skills/misc/migrate-to-shoehorn/SKILL.md)
- `scaffold-exercises`: [`skills/misc/scaffold-exercises/SKILL.md`](archives/mattpocock__skills/snapshot/skills/misc/scaffold-exercises/SKILL.md)
- `setup-pre-commit`: [`skills/misc/setup-pre-commit/SKILL.md`](archives/mattpocock__skills/snapshot/skills/misc/setup-pre-commit/SKILL.md)
- `edit-article`: [`skills/personal/edit-article/SKILL.md`](archives/mattpocock__skills/snapshot/skills/personal/edit-article/SKILL.md)
- `obsidian-vault`: [`skills/personal/obsidian-vault/SKILL.md`](archives/mattpocock__skills/snapshot/skills/personal/obsidian-vault/SKILL.md)
- `grill-me`: [`skills/productivity/grill-me/SKILL.md`](archives/mattpocock__skills/snapshot/skills/productivity/grill-me/SKILL.md)
- `grilling`: [`skills/productivity/grilling/SKILL.md`](archives/mattpocock__skills/snapshot/skills/productivity/grilling/SKILL.md)
- `handoff`: [`skills/productivity/handoff/SKILL.md`](archives/mattpocock__skills/snapshot/skills/productivity/handoff/SKILL.md)
- `teach`: [`skills/productivity/teach/SKILL.md`](archives/mattpocock__skills/snapshot/skills/productivity/teach/SKILL.md)
- `writing-great-skills`: [`skills/productivity/writing-great-skills/SKILL.md`](archives/mattpocock__skills/snapshot/skills/productivity/writing-great-skills/SKILL.md)

### juliusbrussee/caveman
- `cavecrew`: [`plugins/caveman/skills/cavecrew/SKILL.md`](archives/juliusbrussee__caveman/snapshot/plugins/caveman/skills/cavecrew/SKILL.md)
- `caveman`: [`plugins/caveman/skills/caveman/SKILL.md`](archives/juliusbrussee__caveman/snapshot/plugins/caveman/skills/caveman/SKILL.md)
- `caveman-compress`: [`plugins/caveman/skills/caveman-compress/SKILL.md`](archives/juliusbrussee__caveman/snapshot/plugins/caveman/skills/caveman-compress/SKILL.md)
- `caveman-stats`: [`plugins/caveman/skills/caveman-stats/SKILL.md`](archives/juliusbrussee__caveman/snapshot/plugins/caveman/skills/caveman-stats/SKILL.md)
- `cavecrew`: [`skills/cavecrew/SKILL.md`](archives/juliusbrussee__caveman/snapshot/skills/cavecrew/SKILL.md)
- `caveman`: [`skills/caveman/SKILL.md`](archives/juliusbrussee__caveman/snapshot/skills/caveman/SKILL.md)
- `caveman-commit`: [`skills/caveman-commit/SKILL.md`](archives/juliusbrussee__caveman/snapshot/skills/caveman-commit/SKILL.md)
- `caveman-compress`: [`skills/caveman-compress/SKILL.md`](archives/juliusbrussee__caveman/snapshot/skills/caveman-compress/SKILL.md)
- `caveman-help`: [`skills/caveman-help/SKILL.md`](archives/juliusbrussee__caveman/snapshot/skills/caveman-help/SKILL.md)
- `caveman-review`: [`skills/caveman-review/SKILL.md`](archives/juliusbrussee__caveman/snapshot/skills/caveman-review/SKILL.md)
- `caveman-stats`: [`skills/caveman-stats/SKILL.md`](archives/juliusbrussee__caveman/snapshot/skills/caveman-stats/SKILL.md)

## Duplicate Tracking

- Exact duplicate groups: 4
- Repeated skill names: 4
- Full report: [`catalog/duplicates.json`](catalog/duplicates.json)

## Add A Source

When you provide a new GitHub repository URL, add it with:

```bash
python3 scripts/sync_sources.py add https://github.com/owner/repo
```

That command updates `catalog/sources.json`, refreshes every registered source, rebuilds the indexes, and appends a new entry to `AGENT_LOG.md`.

## Weekly Refresh

Use `python3 scripts/sync_sources.py` to refresh every registered source. The weekly automation in Codex is configured for Sunday at 3:00 PM America/New_York and appends an entry to `AGENT_LOG.md` every time it updates the archive.
