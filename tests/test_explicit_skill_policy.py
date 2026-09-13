from __future__ import annotations

from pathlib import Path
import shutil
import tempfile
import unittest

import yaml

from shared.scripts.enforce_explicit_skill_policy import (
    EXPLICIT_DESCRIPTION_PREFIX,
    MANIFEST,
    process_root,
)


ROOT = Path(__file__).resolve().parents[1]


class ExplicitSkillPolicyTests(unittest.TestCase):
    def test_repository_policy_has_no_drift(self):
        changed, missing = process_root(ROOT, check=True)
        self.assertEqual([], missing)
        self.assertEqual([], changed)

    def test_enforcement_preserves_bodies_and_protects_optional_skills_and_commands(self):
        manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in [*manifest["skills"], "explicit-skill-router"]:
                source = ROOT / name
                target = root / name
                (target / "agents").mkdir(parents=True)
                shutil.copy2(source / "SKILL.md", target / "SKILL.md")
                shutil.copy2(source / "agents" / "openai.yaml", target / "agents" / "openai.yaml")

            external = root / "planning-with-files"
            (external / "agents").mkdir(parents=True)
            (external / "SKILL.md").write_text(
                "---\nname: planning-with-files\n"
                "description: Plan work that must resume across sessions.\n"
                "custom: keep-me\n---\n\nBody.\n",
                encoding="utf-8",
            )
            (external / "agents" / "openai.yaml").write_text(
                "interface:\n  display_name: Planning\n",
                encoding="utf-8",
            )

            command = root / "source-command-plan"
            command.mkdir()
            (command / "SKILL.md").write_text(
                "---\nname: source-command-plan\ndescription: Start planning.\n---\n\nBody.\n",
                encoding="utf-8",
            )

            changed, missing = process_root(root, check=False)
            self.assertEqual([], missing)
            self.assertIn("planning-with-files/SKILL.md", changed)
            self.assertIn("planning-with-files/agents/openai.yaml", changed)
            self.assertIn("source-command-plan/SKILL.md", changed)
            self.assertIn("source-command-plan/agents/openai.yaml", changed)

            external_text = (external / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("\nBody.\n", external_text)
            self.assertIn(f"description: {EXPLICIT_DESCRIPTION_PREFIX}", external_text)
            self.assertIn(manifest["external_skills"]["planning-with-files"]["deployed_description"], external_text)
            self.assertNotIn("Plan work that must resume across sessions.", external_text)
            external_metadata = yaml.safe_load((external / "agents" / "openai.yaml").read_text(encoding="utf-8"))
            self.assertEqual("Planning", external_metadata["interface"]["display_name"])
            self.assertFalse(external_metadata["policy"]["allow_implicit_invocation"])

            command_text = (command / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("\nBody.\n", command_text)
            self.assertIn(f"description: {EXPLICIT_DESCRIPTION_PREFIX}", command_text)
            command_metadata = yaml.safe_load((command / "agents" / "openai.yaml").read_text(encoding="utf-8"))
            self.assertFalse(command_metadata["policy"]["allow_implicit_invocation"])

            checked, _ = process_root(root, check=True)
            self.assertEqual([], checked)


if __name__ == "__main__":
    unittest.main()
