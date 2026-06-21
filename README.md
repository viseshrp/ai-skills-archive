# AI Skills Archive

A self-contained archive of popular AI skill repositories from GitHub.

This repository stores reduced snapshots that keep every discovered `SKILL.md` plus recursively linked local resources, records the upstream source metadata, and flags duplicate skills so the archive can grow without losing provenance.

## Goals

- Preserve upstream AI skill repositories in a self-contained, skill-focused layout.
- Track source URLs, archived commits, and sync timestamps.
- Index every discovered skill file with links back to the archived snapshot.
- Flag exact duplicate skill content and repeated skill names.
- Support repeatable weekly refreshes and future source additions.

## Repository Layout

- `archives/<owner>__<repo>/snapshot/`: reduced snapshot containing only `SKILL.md` files and recursively related local resources, excluding upstream `.git` history and unrelated repo files.
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
  - Files retained in reduced snapshot: 24
- [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)
  - Archived commit: `2c606141936f1eeef17fa3043a72095b4765b9c2`
  - Snapshot: [`archives/multica-ai__andrej-karpathy-skills/snapshot`](archives/multica-ai__andrej-karpathy-skills/snapshot)
  - Skills discovered: 1
  - Files retained in reduced snapshot: 1
- [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills)
  - Archived commit: `c22c17eed8a5753aa60681be9734919f2e2f5b42`
  - Snapshot: [`archives/Imbad0202__academic-research-skills/snapshot`](archives/Imbad0202__academic-research-skills/snapshot)
  - Skills discovered: 4
  - Files retained in reduced snapshot: 148
- [mattpocock/skills](https://github.com/mattpocock/skills)
  - Archived commit: `6eeb81b5fcfeeb5bd531dd47ab2f9f2bbea27461`
  - Snapshot: [`archives/mattpocock__skills/snapshot`](archives/mattpocock__skills/snapshot)
  - Skills discovered: 34
  - Files retained in reduced snapshot: 57
- [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman)
  - Archived commit: `25d22f864ad68cc447a4cb93aefde918aa4aec9f`
  - Snapshot: [`archives/juliusbrussee__caveman/snapshot`](archives/juliusbrussee__caveman/snapshot)
  - Skills discovered: 11
  - Files retained in reduced snapshot: 13
- [obra/Superpowers](https://github.com/obra/Superpowers)
  - Archived commit: `896224c4b1879920ab573417e68fd51d2ccc9072`
  - Snapshot: [`archives/obra__Superpowers/snapshot`](archives/obra__Superpowers/snapshot)
  - Skills discovered: 14
  - Files retained in reduced snapshot: 29
- [cursor/plugins](https://github.com/cursor/plugins)
  - Archived commit: `e46364b8be46000b7df0f260550cd712afbb8d36`
  - Snapshot: [`archives/cursor__plugins/snapshot`](archives/cursor__plugins/snapshot)
  - Skills discovered: 71
  - Files retained in reduced snapshot: 156

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

### obra/Superpowers
- `brainstorming`: [`skills/brainstorming/SKILL.md`](archives/obra__Superpowers/snapshot/skills/brainstorming/SKILL.md)
- `dispatching-parallel-agents`: [`skills/dispatching-parallel-agents/SKILL.md`](archives/obra__Superpowers/snapshot/skills/dispatching-parallel-agents/SKILL.md)
- `executing-plans`: [`skills/executing-plans/SKILL.md`](archives/obra__Superpowers/snapshot/skills/executing-plans/SKILL.md)
- `finishing-a-development-branch`: [`skills/finishing-a-development-branch/SKILL.md`](archives/obra__Superpowers/snapshot/skills/finishing-a-development-branch/SKILL.md)
- `receiving-code-review`: [`skills/receiving-code-review/SKILL.md`](archives/obra__Superpowers/snapshot/skills/receiving-code-review/SKILL.md)
- `requesting-code-review`: [`skills/requesting-code-review/SKILL.md`](archives/obra__Superpowers/snapshot/skills/requesting-code-review/SKILL.md)
- `subagent-driven-development`: [`skills/subagent-driven-development/SKILL.md`](archives/obra__Superpowers/snapshot/skills/subagent-driven-development/SKILL.md)
- `systematic-debugging`: [`skills/systematic-debugging/SKILL.md`](archives/obra__Superpowers/snapshot/skills/systematic-debugging/SKILL.md)
- `test-driven-development`: [`skills/test-driven-development/SKILL.md`](archives/obra__Superpowers/snapshot/skills/test-driven-development/SKILL.md)
- `using-git-worktrees`: [`skills/using-git-worktrees/SKILL.md`](archives/obra__Superpowers/snapshot/skills/using-git-worktrees/SKILL.md)
- `using-superpowers`: [`skills/using-superpowers/SKILL.md`](archives/obra__Superpowers/snapshot/skills/using-superpowers/SKILL.md)
- `verification-before-completion`: [`skills/verification-before-completion/SKILL.md`](archives/obra__Superpowers/snapshot/skills/verification-before-completion/SKILL.md)
- `writing-plans`: [`skills/writing-plans/SKILL.md`](archives/obra__Superpowers/snapshot/skills/writing-plans/SKILL.md)
- `writing-skills`: [`skills/writing-skills/SKILL.md`](archives/obra__Superpowers/snapshot/skills/writing-skills/SKILL.md)

### cursor/plugins
- `check-agent-compatibility`: [`agent-compatibility/skills/check-agent-compatibility/SKILL.md`](archives/cursor__plugins/snapshot/agent-compatibility/skills/check-agent-compatibility/SKILL.md)
- `cli-for-agents`: [`cli-for-agent/skills/cli-for-agents/SKILL.md`](archives/cursor__plugins/snapshot/cli-for-agent/skills/cli-for-agents/SKILL.md)
- `continual-learning`: [`continual-learning/skills/continual-learning/SKILL.md`](archives/cursor__plugins/snapshot/continual-learning/skills/continual-learning/SKILL.md)
- `create-plugin-scaffold`: [`create-plugin/skills/create-plugin-scaffold/SKILL.md`](archives/cursor__plugins/snapshot/create-plugin/skills/create-plugin-scaffold/SKILL.md)
- `review-plugin-submission`: [`create-plugin/skills/review-plugin-submission/SKILL.md`](archives/cursor__plugins/snapshot/create-plugin/skills/review-plugin-submission/SKILL.md)
- `cursor-sdk`: [`cursor-sdk/skills/cursor-sdk/SKILL.md`](archives/cursor__plugins/snapshot/cursor-sdk/skills/cursor-sdk/SKILL.md)
- `check-compiler-errors`: [`cursor-team-kit/skills/check-compiler-errors/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/check-compiler-errors/SKILL.md)
- `control-cli`: [`cursor-team-kit/skills/control-cli/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/control-cli/SKILL.md)
- `control-ui`: [`cursor-team-kit/skills/control-ui/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/control-ui/SKILL.md)
- `deslop`: [`cursor-team-kit/skills/deslop/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/deslop/SKILL.md)
- `fix-ci`: [`cursor-team-kit/skills/fix-ci/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/fix-ci/SKILL.md)
- `fix-merge-conflicts`: [`cursor-team-kit/skills/fix-merge-conflicts/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/fix-merge-conflicts/SKILL.md)
- `get-pr-comments`: [`cursor-team-kit/skills/get-pr-comments/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/get-pr-comments/SKILL.md)
- `loop-on-ci`: [`cursor-team-kit/skills/loop-on-ci/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/loop-on-ci/SKILL.md)
- `make-pr-easy-to-review`: [`cursor-team-kit/skills/make-pr-easy-to-review/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/make-pr-easy-to-review/SKILL.md)
- `new-branch-and-pr`: [`cursor-team-kit/skills/new-branch-and-pr/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/new-branch-and-pr/SKILL.md)
- `pr-review-canvas`: [`cursor-team-kit/skills/pr-review-canvas/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/pr-review-canvas/SKILL.md)
- `review-and-ship`: [`cursor-team-kit/skills/review-and-ship/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/review-and-ship/SKILL.md)
- `run-smoke-tests`: [`cursor-team-kit/skills/run-smoke-tests/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/run-smoke-tests/SKILL.md)
- `thermo-nuclear-code-quality-review`: [`cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md)
- `verify-this`: [`cursor-team-kit/skills/verify-this/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/verify-this/SKILL.md)
- `weekly-review`: [`cursor-team-kit/skills/weekly-review/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/weekly-review/SKILL.md)
- `what-did-i-get-done`: [`cursor-team-kit/skills/what-did-i-get-done/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/what-did-i-get-done/SKILL.md)
- `workflow-from-chats`: [`cursor-team-kit/skills/workflow-from-chats/SKILL.md`](archives/cursor__plugins/snapshot/cursor-team-kit/skills/workflow-from-chats/SKILL.md)
- `docs-canvas`: [`docs-canvas/skills/docs-canvas/SKILL.md`](archives/cursor__plugins/snapshot/docs-canvas/skills/docs-canvas/SKILL.md)
- `orchestrate`: [`orchestrate/skills/orchestrate/SKILL.md`](archives/cursor__plugins/snapshot/orchestrate/skills/orchestrate/SKILL.md)
- `pr-review-canvas`: [`pr-review-canvas/skills/pr-review-canvas/SKILL.md`](archives/cursor__plugins/snapshot/pr-review-canvas/skills/pr-review-canvas/SKILL.md)
- `architect`: [`pstack/skills/architect/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/architect/SKILL.md)
- `arena`: [`pstack/skills/arena/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/arena/SKILL.md)
- `automate-me`: [`pstack/skills/automate-me/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/automate-me/SKILL.md)
- `blast-radius`: [`pstack/skills/blast-radius/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/blast-radius/SKILL.md)
- `figure-it-out`: [`pstack/skills/figure-it-out/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/figure-it-out/SKILL.md)
- `how`: [`pstack/skills/how/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/how/SKILL.md)
- `interrogate`: [`pstack/skills/interrogate/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/interrogate/SKILL.md)
- `poteto-mode`: [`pstack/skills/poteto-mode/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/poteto-mode/SKILL.md)
- `principle-boundary-discipline`: [`pstack/skills/principle-boundary-discipline/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-boundary-discipline/SKILL.md)
- `principle-build-the-lever`: [`pstack/skills/principle-build-the-lever/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-build-the-lever/SKILL.md)
- `principle-encode-lessons-in-structure`: [`pstack/skills/principle-encode-lessons-in-structure/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-encode-lessons-in-structure/SKILL.md)
- `principle-exhaust-the-design-space`: [`pstack/skills/principle-exhaust-the-design-space/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-exhaust-the-design-space/SKILL.md)
- `principle-experience-first`: [`pstack/skills/principle-experience-first/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-experience-first/SKILL.md)
- `principle-fix-root-causes`: [`pstack/skills/principle-fix-root-causes/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-fix-root-causes/SKILL.md)
- `principle-foundational-thinking`: [`pstack/skills/principle-foundational-thinking/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-foundational-thinking/SKILL.md)
- `principle-guard-the-context-window`: [`pstack/skills/principle-guard-the-context-window/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-guard-the-context-window/SKILL.md)
- `principle-laziness-protocol`: [`pstack/skills/principle-laziness-protocol/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-laziness-protocol/SKILL.md)
- `principle-make-operations-idempotent`: [`pstack/skills/principle-make-operations-idempotent/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-make-operations-idempotent/SKILL.md)
- `principle-migrate-callers-then-delete-legacy-apis`: [`pstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md)
- `principle-minimize-reader-load`: [`pstack/skills/principle-minimize-reader-load/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-minimize-reader-load/SKILL.md)
- `principle-never-block-on-the-human`: [`pstack/skills/principle-never-block-on-the-human/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-never-block-on-the-human/SKILL.md)
- `principle-outcome-oriented-execution`: [`pstack/skills/principle-outcome-oriented-execution/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-outcome-oriented-execution/SKILL.md)
- `principle-prove-it-works`: [`pstack/skills/principle-prove-it-works/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-prove-it-works/SKILL.md)
- `principle-redesign-from-first-principles`: [`pstack/skills/principle-redesign-from-first-principles/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-redesign-from-first-principles/SKILL.md)
- `principle-separate-before-serializing-shared-state`: [`pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md)
- `principle-sequence-verifiable-units`: [`pstack/skills/principle-sequence-verifiable-units/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-sequence-verifiable-units/SKILL.md)
- `principle-subtract-before-you-add`: [`pstack/skills/principle-subtract-before-you-add/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-subtract-before-you-add/SKILL.md)
- `principle-type-system-discipline`: [`pstack/skills/principle-type-system-discipline/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/principle-type-system-discipline/SKILL.md)
- `recall`: [`pstack/skills/recall/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/recall/SKILL.md)
- `reflect`: [`pstack/skills/reflect/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/reflect/SKILL.md)
- `setup-pstack`: [`pstack/skills/setup-pstack/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/setup-pstack/SKILL.md)
- `show-me-your-work`: [`pstack/skills/show-me-your-work/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/show-me-your-work/SKILL.md)
- `tdd`: [`pstack/skills/tdd/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/tdd/SKILL.md)
- `typescript-best-practices`: [`pstack/skills/typescript-best-practices/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/typescript-best-practices/SKILL.md)
- `unslop`: [`pstack/skills/unslop/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/unslop/SKILL.md)
- `why`: [`pstack/skills/why/SKILL.md`](archives/cursor__plugins/snapshot/pstack/skills/why/SKILL.md)
- `cancel-ralph`: [`ralph-loop/skills/cancel-ralph/SKILL.md`](archives/cursor__plugins/snapshot/ralph-loop/skills/cancel-ralph/SKILL.md)
- `ralph-loop`: [`ralph-loop/skills/ralph-loop/SKILL.md`](archives/cursor__plugins/snapshot/ralph-loop/skills/ralph-loop/SKILL.md)
- `ralph-loop-help`: [`ralph-loop/skills/ralph-loop-help/SKILL.md`](archives/cursor__plugins/snapshot/ralph-loop/skills/ralph-loop-help/SKILL.md)
- `create-learning-path`: [`teaching/skills/create-learning-path/SKILL.md`](archives/cursor__plugins/snapshot/teaching/skills/create-learning-path/SKILL.md)
- `run-learning-retrospective`: [`teaching/skills/run-learning-retrospective/SKILL.md`](archives/cursor__plugins/snapshot/teaching/skills/run-learning-retrospective/SKILL.md)
- `thermo-nuclear-code-quality-review`: [`thermos/skills/thermo-nuclear-code-quality-review/SKILL.md`](archives/cursor__plugins/snapshot/thermos/skills/thermo-nuclear-code-quality-review/SKILL.md)
- `thermo-nuclear-review`: [`thermos/skills/thermo-nuclear-review/SKILL.md`](archives/cursor__plugins/snapshot/thermos/skills/thermo-nuclear-review/SKILL.md)
- `thermos`: [`thermos/skills/thermos/SKILL.md`](archives/cursor__plugins/snapshot/thermos/skills/thermos/SKILL.md)

## Duplicate Tracking

- Exact duplicate groups: 5
- Repeated skill names: 8
- Full report: [`catalog/duplicates.json`](catalog/duplicates.json)

## Add A Source

When you provide a new GitHub repository URL, add it with:

```bash
python3 scripts/sync_sources.py add https://github.com/owner/repo
```

That command updates `catalog/sources.json`, refreshes every registered source, rebuilds the indexes, and appends a new entry to `AGENT_LOG.md`.

## Weekly Refresh

Use `python3 scripts/sync_sources.py` to refresh every registered source. The weekly automation in Codex is configured for Sunday at 3:00 PM America/New_York and appends an entry to `AGENT_LOG.md` every time it updates the archive.
