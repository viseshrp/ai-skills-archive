---
name: test-audit
description: Audit new or existing tests for behavioral value, duplication, implementation coupling, brittleness, and test-only production seams. Use when writing, changing, reviewing, or pruning tests, including an independent final review of a test diff.
license: MIT
metadata:
  source: https://github.com/openclaw/openclaw/blob/1c8b3187353b1d7b69faf66ca053bcb2257221f3/.agents/skills/test-audit/SKILL.md
  adapted: Language-neutral core with separate Python and JavaScript guidance.
---

# Test Audit

Use one value bar across three modes:

- Authoring mode gates every new or changed test before it lands.
- Audit mode reviews a focused test surface for weak, duplicated, brittle, or implementation-coupled proof.
- Campaign mode reviews a whole subsystem in bounded owner-based batches.

Optimize for confidence, not test count, coverage percentage, or deletion count. Start read-only. Edit tests or production code only when the task authorizes those changes.

## Authoring gate

Before adding or changing a test, answer all four questions:

1. What observable behavior, invariant, or independent contract does it protect?
2. What credible regression makes it fail for the intended reason?
3. Why does existing coverage not already catch that regression?
4. Does the test require an export, flag, wrapper, injection hook, reset function, or other production seam that no production caller needs?

A missing answer means the test is not ready. Prefer extending the strongest existing owner-boundary test over replaying the same scenario at several layers. A test that fails after a behavior-preserving refactor is probably asserting implementation rather than behavior.

For a bug regression, prove that the test fails on the faulty code for the intended reason and passes after the repair. If that control cannot be run safely, state the limitation and provide the strongest available evidence. Do not claim the regression is proven when only the post-fix test was observed.

## Low-value patterns

Reject or investigate tests that rely on any of these patterns:

- no meaningful assertion, self-comparison, or identity copying;
- copied inventories, manifests, export lists, source text, import paths, or exact strings that are not themselves public contracts;
- direct tests of private predicates or call shapes when a stronger public boundary already proves the behavior;
- repeated invocations of the same contract across layers without a distinct transport, lifecycle, serialization, or integration risk;
- expected values produced by the same helper, renderer, parser, or algorithm under test;
- mocks, fakes, or fixtures that implement or precompute the behavior being asserted;
- assertions about persistence, callbacks, acknowledgements, ordering, or side effects that the exercised path never performs;
- capability tests that restate configuration or flags without exercising the promised behavior;
- negative controls that pass because an unrelated guard rejects the input first;
- snapshots that preserve incidental structure while hiding the behavior that matters;
- tests whose only purpose is preserving test-only production exports, globals, wrappers, or dead code;
- names or fixtures that promise a scenario the input and assertions do not exercise.

A matching pattern is a reason to inspect, not an automatic deletion rule. Apply the retention bar before changing anything.

## Retention bar

Keep a test when it independently enforces a meaningful contract such as a public API, protocol, configuration format, migration, storage rule, security boundary, platform behavior, accessibility requirement, package boundary, generated artifact, release invariant, or architecture constraint.

Also keep a test when:

- call ordering is observable behavior;
- it protects a credible regression at the strongest practical boundary;
- source or snapshot inspection is the cheapest independent guard for an exact user-facing byte, key, path, schema, prompt, or generated file;
- a lower-level test covers a failure mode that the higher-level owner cannot reliably reach;
- a retained test fails on the baseline and may expose a product defect.

Static, slow, broad, or implementation-adjacent does not make a test disposable by itself. Prove that stronger surviving evidence covers the same contract before removing it.

## Evidence before judgment

Read the applicable repository instructions first. Before classifying a test, inspect:

- the complete test, including parameter tables, fixtures, helpers, and snapshots;
- the production owner, public entry point, important callers and callees, and sibling implementations;
- overlapping tests at stronger and weaker boundaries;
- test-runner, coverage, and CI routing configuration;
- relevant history that explains why the test or test seam exists;
- dependency source, types, or authoritative documentation when the claim depends on external behavior.

For each proposed repair, consolidation, or deletion, record:

- exact test name and location;
- the failure it can actually detect;
- the pattern that makes it suspect;
- non-test callers of any production or support seam involved;
- the stronger surviving proof, or why no proof is needed;
- relevant history and original purpose;
- code or support cleanup unlocked;
- risk and focused validation command.

Missing evidence means the candidate is not ready to change.

## Audit workflow

1. Define the exact diff, feature, package, or subsystem in scope and record the baseline test state.
2. Map each observable contract to its strongest test owner. Identify distinct risks that justify secondary layers.
3. Classify every candidate as retain, repair, consolidate, or delete, with evidence.
4. Keep discovery read-only until the classification is reviewable.
5. If edits are authorized, change one coherent owner-boundary batch. Remove obsolete test-only seams and dead support code only when their callers and surviving proof are known.
6. Re-run the smallest relevant checks, then the broader repository-required gate. Compare the final proof with the baseline.

For broad work, divide discovery by production-owner boundaries rather than arbitrary filename prefixes. Each test belongs to one primary lane. Serialize edits to shared fixtures, harnesses, and production support through one owner.

## Python-specific instructions

Apply this section only when the relevant tests use Python.

- Detect and preserve the established runner and style, such as pytest or unittest. Do not migrate frameworks during an audit.
- With pytest, prefer existing fixtures and native facilities such as `monkeypatch`, `tmp_path`, `capsys`, `capfd`, `caplog`, `pytest.raises`, `pytest.warns`, and `pytest.mark.parametrize` when they fit the repository's conventions.
- Patch external collaborators at the lookup boundary used by the subject. Do not patch the function, method, or class whose behavior the test claims to prove.
- Treat fixture scopes, autouse fixtures, module imports, environment mutation, working-directory changes, caches, and event loops as possible sources of hidden coupling or order dependence.
- Keep parameter tables behavior-oriented. Rows that exercise different contracts should not be compressed into one opaque parameterized test.
- Use the repository's configured focused test and coverage commands. Common command names are examples, not defaults; inspect `pyproject.toml`, `pytest.ini`, `tox.ini`, `setup.cfg`, and CI before choosing one.

## JavaScript and TypeScript-specific instructions

Apply this section only when the relevant tests use JavaScript or TypeScript.

- Detect and preserve the established runner and style, such as Vitest, Jest, Node's test runner, Mocha, Playwright, or a framework-specific harness. Do not introduce or migrate a runner during an audit.
- Prefer the runner's native setup, teardown, parameterization, fake-timer, and mock-restoration APIs over custom global state management.
- Restore mocked functions, timers, environment variables, module registries, DOM state, and network interceptors. Check for order dependence caused by module caches or shared workers.
- Mock external boundaries, not the module behavior under test. A mock that returns the asserted transformation, rendered output, event order, or state transition proves itself.
- Use snapshots only when the serialized output is an intentional contract and the review can explain meaningful changes. Prefer focused semantic assertions for behavior.
- For browser or UI tests, assert user-observable behavior with the repository's established query and interaction APIs. Avoid DOM structure, generated class names, and private component state unless they are contractual.
- Use repository scripts and configuration to choose focused tests, coverage, type checks, and lint. Do not assume `npm test`, a package manager, or a runner from file names alone.

## Validation

- Run the smallest owner and sibling tests first.
- For a removed source assertion, snapshot, plan check, or generated-file check, run the executable path or dry run that owns the real contract when available.
- When feasible, use a deliberate mutation or pre-fix control to prove that retained or repaired tests go red for the intended regression. Restore the source exactly afterward.
- Run applicable formatting, lint, type, and diff checks required by the repository.
- Run broader tests only when repository policy, changed shared infrastructure, or the claim being made requires them.
- Inspect the final diff and line counts. Report production code, test code, fixtures, snapshots, and test-support changes separately.
- Treat unrelated baseline failures as baseline evidence. Do not delete or weaken a test merely to make the run green.

## Landing and handoff

Commit, push, open a pull request, merge, or alter production code only when the task and repository rules authorize it. Do not turn uncertain candidates into cleanup to increase deletion counts.

Report:

- scope and baseline;
- retained tests and the contracts they protect;
- repaired, consolidated, or removed low-value patterns;
- production or test-support simplifications;
- focused and broader verification actually run;
- production versus test and support changes;
- unresolved risks, baseline failures, and follow-ups;
- commit, pull-request, or merge state when applicable.

Adapted from OpenClaw's `test-audit` skill at the pinned source in the metadata. See [LICENSE](LICENSE).
