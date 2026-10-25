from pathlib import Path
import tempfile
import unittest

import sync_sources


class SkillBaseReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.skill = self.root / "skills/demo/SKILL.md"

    def write(self, relative, content="payload"):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def related(self, content):
        self.write("skills/demo/SKILL.md", content)
        return set(sync_sources.collect_related_files(self.skill, self.root))

    def test_literal_skill_base_reference(self):
        self.write("skills/demo/references/workflow.md")
        self.assertEqual(
            self.related("Read $SKILLBASE/references/workflow.md."),
            {"skills/demo/references/workflow.md"},
        )

    def test_braced_skill_base_reference(self):
        self.write("skills/demo/references/workflow.md")
        self.assertEqual(
            self.related("Read '" + "$" + "{SKILLBASE}/references/workflow.md'."),
            {"skills/demo/references/workflow.md"},
        )

    def test_transitive_reference_keeps_original_skill_base(self):
        self.write(
            "skills/demo/references/workflow.md",
            "Read '$SKILLBASE/references/templates/output.md'.",
        )
        self.write("skills/demo/references/templates/output.md")
        self.assertEqual(
            self.related("Read '$SKILLBASE/references/workflow.md'."),
            {
                "skills/demo/references/workflow.md",
                "skills/demo/references/templates/output.md",
            },
        )

    def test_step_placeholder_preserves_processes_and_their_templates(self):
        self.write(
            "skills/demo/references/research/process.md",
            "Read '$SKILLBASE/references/research/template.md'.",
        )
        self.write("skills/demo/references/research/template.md")
        self.write("skills/demo/references/design/process.md")
        self.write("skills/demo/references/design/unrelated.md")
        self.write("skills/demo/unrelated.md")
        self.assertEqual(
            self.related("Read '$SKILLBASE/references/<step>/process.md'."),
            {
                "skills/demo/references/research/process.md",
                "skills/demo/references/research/template.md",
                "skills/demo/references/design/process.md",
            },
        )

    def test_named_subagent_placeholder(self):
        self.write("skills/demo/references/subagents/analyzer.md")
        self.write("skills/demo/references/subagents/locator.md")
        self.write("skills/demo/references/subagents/unrelated.txt")
        self.assertEqual(
            self.related("$SKILLBASE/references/subagents/SUBAGENT_NAME.md"),
            {
                "skills/demo/references/subagents/analyzer.md",
                "skills/demo/references/subagents/locator.md",
            },
        )

    def test_directory_glob_preserves_referenced_subtree(self):
        self.write("skills/demo/references/deep/guide.md")
        self.write("skills/demo/references/another.txt")
        self.assertEqual(
            self.related("Read '$SKILLBASE/references/*'."),
            {
                "skills/demo/references/deep/guide.md",
                "skills/demo/references/another.txt",
            },
        )

    def test_literal_uppercase_filename_is_not_a_placeholder(self):
        self.write("skills/demo/references/README.md")
        self.write("skills/demo/references/unrelated.md")
        self.assertEqual(
            self.related("$SKILLBASE/references/README.md"),
            {"skills/demo/references/README.md"},
        )

    def test_escape_outside_repository_is_rejected(self):
        outside = self.root.parent / (self.root.name + "-outside.md")
        outside.write_text("private")
        self.addCleanup(outside.unlink)
        self.assertEqual(
            self.related(f"$SKILLBASE/../../../{outside.name}"), set()
        )

    def test_git_metadata_is_rejected(self):
        self.write(".git/config")
        self.assertEqual(self.related("$SKILLBASE/../../.git/config"), set())

    def test_symlink_outside_repository_is_rejected(self):
        outside = self.root.parent / (self.root.name + "-outside.md")
        outside.write_text("private")
        self.addCleanup(outside.unlink)
        target = self.root / "skills/demo/references/escape.md"
        target.parent.mkdir(parents=True)
        target.symlink_to(outside)
        self.assertEqual(
            self.related("$SKILLBASE/references/escape.md"), set()
        )

    def test_ordinary_relative_links_still_work(self):
        self.write("skills/demo/references/workflow.md", "[output](output.md)")
        self.write("skills/demo/references/output.md")
        self.assertEqual(
            self.related("[workflow](references/workflow.md)"),
            {
                "skills/demo/references/workflow.md",
                "skills/demo/references/output.md",
            },
        )

    def test_module_relative_library_directory_is_preserved(self):
        self.write(
            "skills/demo/scripts/draw.mjs",
            "const HERE = dirname(fileURLToPath(import.meta.url));\n"
            "const LIB = join(HERE, '..', 'library');\n"
            "const load = name => readFileSync(join(LIB, name + '.json'));\n",
        )
        self.write("skills/demo/library/directions.json", "{}")
        self.write("skills/demo/library/nested/palettes.json", "{}")
        self.write("skills/demo/unrelated.md")
        self.assertEqual(
            self.related("Run `scripts/draw.mjs`."),
            {
                "skills/demo/scripts/draw.mjs",
                "skills/demo/library/directions.json",
                "skills/demo/library/nested/palettes.json",
            },
        )

    def test_module_relative_library_rejects_escape_and_dynamic_bases(self):
        outside = Path(self.temp.name + "-outside")
        outside.mkdir()
        self.addCleanup(outside.rmdir)
        payload = outside / "private.json"
        payload.write_text("{}")
        self.addCleanup(payload.unlink)
        self.write(
            "skills/demo/scripts/draw.mjs",
            "const HERE = dirname(fileURLToPath(import.meta.url));\n"
            f"const LIB = join(HERE, '../../../..', '{outside.name}');\n"
            "const OTHER = join(process.cwd(), 'library');\n",
        )
        self.write("skills/demo/scripts/library/unrelated.json", "{}")
        self.assertEqual(
            self.related("Run `scripts/draw.mjs`."),
            {"skills/demo/scripts/draw.mjs"},
        )

    def test_module_relative_library_rejects_symlink_escape(self):
        outside = Path(self.temp.name + "-outside")
        outside.mkdir()
        self.addCleanup(outside.rmdir)
        payload = outside / "private.json"
        payload.write_text("{}")
        self.addCleanup(payload.unlink)
        self.write(
            "skills/demo/scripts/draw.mjs",
            "const HERE = dirname(fileURLToPath(import.meta.url));\n"
            "const LIB = join(HERE, '..', 'library');\n",
        )
        (self.root / "skills/demo/library").symlink_to(outside, target_is_directory=True)
        self.assertEqual(
            self.related("Run `scripts/draw.mjs`."),
            {"skills/demo/scripts/draw.mjs"},
        )

    def test_linked_guide_can_reference_skill_root_helpers(self):
        self.write("skills/demo/guides/run.md", "Run `scripts/check.mjs`.")
        self.write("skills/demo/scripts/check.mjs")
        self.assertEqual(
            self.related("Read [guide](guides/run.md)."),
            {"skills/demo/guides/run.md", "skills/demo/scripts/check.mjs"},
        )

    def test_repository_relative_reference_in_linked_guide(self):
        self.write(
            "skills/demo/guides/run.md",
            "Run `node skills/demo/scripts/check.mjs`.",
        )
        self.write("skills/demo/scripts/check.mjs")
        self.assertEqual(
            self.related("Read [guide](guides/run.md)."),
            {"skills/demo/guides/run.md", "skills/demo/scripts/check.mjs"},
        )

    def test_markdown_directory_link_preserves_examples(self):
        self.write("skills/demo/references/examples/README.md", "Read [case](case.md).")
        self.write("skills/demo/references/examples/case.md")
        self.write("skills/demo/unrelated.md")
        self.assertEqual(
            self.related("Follow [examples](references/examples/)."),
            {
                "skills/demo/references/examples/README.md",
                "skills/demo/references/examples/case.md",
            },
        )

    def test_link_to_sibling_application_does_not_mirror_its_tree(self):
        self.write("engine/runtime.go")
        self.write("engine/runtime_test.go")
        self.assertEqual(
            self.related("See the [application](../../engine/)."), set()
        )

    def test_explicit_inline_directory_preserves_module_helpers(self):
        self.write("skills/demo/scripts/__main__.py", "from .cli import main")
        self.write("skills/demo/scripts/cli.py")
        self.write("skills/demo/unrelated.md")
        self.assertEqual(
            self.related("The module lives in `scripts/`."),
            {"skills/demo/scripts/__main__.py", "skills/demo/scripts/cli.py"},
        )

    def test_linked_extensionless_script_preserves_imports(self):
        self.write("skills/demo/scripts/runner", "#!/usr/bin/env bun\nimport './cli.ts';")
        self.write("skills/demo/scripts/cli.ts", "import '../bootstrap.ts';")
        self.write("skills/demo/bootstrap.ts")
        self.assertEqual(
            self.related("Run `scripts/runner`."),
            {
                "skills/demo/scripts/runner",
                "skills/demo/scripts/cli.ts",
                "skills/demo/bootstrap.ts",
            },
        )

    def test_linked_guide_directory_glob_is_recursive(self):
        self.write("skills/demo/guides/run.md", "Use `scripts/*`.")
        self.write("skills/demo/scripts/deep/check.mjs")
        self.assertEqual(
            self.related("Read [guide](guides/run.md)."),
            {"skills/demo/guides/run.md", "skills/demo/scripts/deep/check.mjs"},
        )

    def test_root_and_git_directories_are_not_expanded(self):
        self.write("unrelated.md")
        self.write(".git/private")
        self.assertEqual(self.related("Read [root](../../) and `.git/`."), set())

    def test_nearest_local_file_wins_over_skill_and_repo_fallbacks(self):
        self.write("skills/demo/guides/run.md", "Read `references/guide.md`.")
        self.write("skills/demo/guides/references/guide.md")
        self.write("skills/demo/references/guide.md")
        self.write("references/guide.md")
        self.assertEqual(
            self.related("Read [guide](guides/run.md)."),
            {
                "skills/demo/guides/run.md",
                "skills/demo/guides/references/guide.md",
            },
        )

    def test_inline_directory_does_not_include_git_metadata(self):
        self.write("skills/demo/scripts/check.py")
        self.write("skills/demo/scripts/.git/config")
        self.assertEqual(
            self.related("Read `scripts/`."), {"skills/demo/scripts/check.py"}
        )

    def test_generic_directory_examples_do_not_import_repo_configuration(self):
        self.write(".claude/owner.md")
        self.write("scripts/unrelated.py")
        self.assertEqual(self.related("Examples: `.claude/` and `scripts/`."), set())

    def test_generic_skill_glob_is_not_source_root_anchored(self):
        self.write("skills/another/SKILL.md")
        self.assertEqual(self.related("Classify `skills/*` in the target project."), set())

    def test_parent_relative_reference_keeps_containing_file_anchor(self):
        self.write("skills/demo/guides/run.md", "Read `../../owner.md`.")
        self.write("owner.md")
        self.assertEqual(
            self.related("Read [guide](guides/run.md)."),
            {"skills/demo/guides/run.md"},
        )

    def test_bun_module_directory_preserves_declared_lockfile(self):
        self.write(
            "skills/demo/scripts/bootstrap.ts",
            'const scriptsDirectory = import.meta.dir;\n'
            'readFileSync(join(scriptsDirectory, "bun.lock"));\n',
        )
        self.write("skills/demo/scripts/bun.lock", "{}")
        self.assertEqual(
            self.related("Run `scripts/bootstrap.ts`."),
            {"skills/demo/scripts/bootstrap.ts", "skills/demo/scripts/bun.lock"},
        )

    def test_python_sibling_imports_are_followed_recursively_without_execution(self):
        self.write(
            "skills/demo/scripts/check.py",
            "raise RuntimeError('must not execute')\nimport helper as local\n",
        )
        self.write("skills/demo/scripts/helper.py", "from final_helper import VALUE\n")
        self.write("skills/demo/scripts/final_helper.py", "VALUE = 1\n")
        self.write("skills/demo/scripts/unrelated.py")
        self.assertEqual(
            self.related("Run `scripts/check.py`."),
            {
                "skills/demo/scripts/check.py",
                "skills/demo/scripts/helper.py",
                "skills/demo/scripts/final_helper.py",
            },
        )

    def test_python_package_and_relative_imports_preserve_initializers(self):
        self.write("skills/demo/scripts/check.py", "from pkg.tools import run\n")
        self.write("skills/demo/scripts/pkg/__init__.py", "")
        self.write("skills/demo/scripts/pkg/tools.py", "from . import detail\n")
        self.write("skills/demo/scripts/pkg/detail.py", "from ..shared import VALUE\n")
        self.write("skills/demo/scripts/shared.py", "VALUE = 1\n")
        self.assertEqual(
            self.related("Run `scripts/check.py`."),
            {
                "skills/demo/scripts/check.py",
                "skills/demo/scripts/pkg/__init__.py",
                "skills/demo/scripts/pkg/tools.py",
                "skills/demo/scripts/pkg/detail.py",
                "skills/demo/scripts/shared.py",
            },
        )

    def test_python_from_package_imports_local_submodule(self):
        self.write("skills/demo/scripts/check.py", "from pkg import worker as local\n")
        self.write("skills/demo/scripts/pkg/__init__.py", "")
        self.write("skills/demo/scripts/pkg/worker.py", "")
        self.write("skills/demo/scripts/pkg/unrelated.py", "")
        self.assertEqual(
            self.related("Run `scripts/check.py`."),
            {
                "skills/demo/scripts/check.py",
                "skills/demo/scripts/pkg/__init__.py",
                "skills/demo/scripts/pkg/worker.py",
            },
        )

    def test_extensionless_python_shebang_preserves_local_import(self):
        self.write(
            "skills/demo/scripts/runner",
            "#!/usr/bin/env python3\nfrom helper import main\n",
        )
        self.write("skills/demo/scripts/helper.py", "")
        self.assertEqual(
            self.related("Run `scripts/runner`."),
            {"skills/demo/scripts/runner", "skills/demo/scripts/helper.py"},
        )

    def test_python_imports_do_not_use_source_root_or_dynamic_fallbacks(self):
        self.write(
            "skills/demo/scripts/check.py",
            "import owner\nimport importlib\nimportlib.import_module('hidden')\n",
        )
        self.write("owner.py", "")
        self.write("skills/demo/scripts/hidden.py", "")
        self.assertEqual(
            self.related("Run `scripts/check.py`."), {"skills/demo/scripts/check.py"}
        )

    def test_python_import_rejects_symlink_escape_and_git_metadata(self):
        outside = self.root.parent / (self.root.name + "-outside.py")
        outside.write_text("private")
        self.addCleanup(outside.unlink)
        self.write(".git/private.py", "private")
        self.write("skills/demo/scripts/check.py", "import escaped\nimport secret\n")
        (self.root / "skills/demo/scripts/escaped.py").symlink_to(outside)
        (self.root / "skills/demo/scripts/secret.py").symlink_to(self.root / ".git/private.py")
        self.assertEqual(
            self.related("Run `scripts/check.py`."), {"skills/demo/scripts/check.py"}
        )

    def test_python_syntax_error_keeps_ordinary_file_references(self):
        self.write("skills/demo/scripts/check.py", "not python (\n# Read notes.md\n")
        self.write("skills/demo/scripts/notes.md")
        self.assertEqual(
            self.related("Run `scripts/check.py`."),
            {"skills/demo/scripts/check.py", "skills/demo/scripts/notes.md"},
        )


if __name__ == "__main__":
    unittest.main()
