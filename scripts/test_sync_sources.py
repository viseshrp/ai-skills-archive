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


if __name__ == "__main__":
    unittest.main()
