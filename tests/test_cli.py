from __future__ import annotations

import argparse
import importlib.machinery
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


CLI_PATH = Path(__file__).resolve().parents[1] / "bin" / "review-atlas"
LOADER = importlib.machinery.SourceFileLoader("review_atlas_cli", str(CLI_PATH))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
CLI = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(CLI)


class PromptTests(unittest.TestCase):
    def args(self, **overrides):
        values = {
            "staged": False,
            "branch": None,
            "base": None,
            "commit": None,
            "pr": None,
            "paths": None,
            "focus": None,
        }
        values.update(overrides)
        return argparse.Namespace(**values)

    def test_default_scope(self):
        with mock.patch.object(CLI, "git_value", return_value="feature/orders"):
            with mock.patch.object(
                CLI, "detect_branch_scope", return_value=("feature/orders", "develop")
            ):
                prompt = CLI.build_review_prompt(self.args())
        self.assertTrue(prompt.startswith("/review-atlas"))
        self.assertIn("branch feature/orders compared with develop", prompt)
        self.assertIn("staged, unstaged, and untracked", prompt)
        self.assertIn("do not modify files", prompt)

    def test_default_scope_falls_back_to_agent_detection(self):
        with mock.patch.object(CLI, "git_value", return_value="feature/orders"):
            with mock.patch.object(CLI, "detect_branch_scope", return_value=None):
                prompt = CLI.build_review_prompt(self.args())

        self.assertIn("automatically determining its most likely base", prompt)
        self.assertIn("ask only if the base is genuinely ambiguous", prompt)

    def test_long_lived_branch_shows_helper_instead_of_starting_review(self):
        with mock.patch.object(CLI, "git_value", return_value="develop"):
            with mock.patch.object(CLI, "detect_branch_scope") as detect:
                prompt = CLI.build_review_prompt(self.args())

        self.assertIn("long-lived branch", prompt)
        self.assertIn("Do not start a review yet", prompt)
        self.assertIn("ask which branch or target", prompt)
        detect.assert_not_called()

    def test_remote_long_lived_branch_name_is_recognized(self):
        self.assertTrue(CLI.is_long_lived_branch("origin/stage"))
        self.assertFalse(CLI.is_long_lived_branch("feature/stage-cleanup"))

    def test_explicit_branch_scope(self):
        prompt = CLI.build_review_prompt(self.args(branch="feature/orders"))

        self.assertIn("branch feature/orders", prompt)
        self.assertIn("only changes introduced by that branch", prompt)

    def test_base_and_focus(self):
        prompt = CLI.build_review_prompt(
            self.args(base="main", focus="security and database performance")
        )
        self.assertIn("compared with main", prompt)
        self.assertIn("Focus on security and database performance", prompt)

    def test_pull_request_scope(self):
        prompt = CLI.build_review_prompt(self.args(pr=42))
        self.assertIn("pull request #42", prompt)

    def test_select_base_candidate_chooses_closest_positive_ref(self):
        base = CLI.select_base_candidate(
            "feature/orders",
            [("origin/develop", 3), ("develop", 3), ("origin/main", 18)],
        )

        self.assertEqual(base, "origin/develop")

    def test_select_base_candidate_excludes_current_and_zero_distance(self):
        base = CLI.select_base_candidate(
            "develop", [("develop", 2), ("origin/develop", 0), ("main", 9)]
        )

        self.assertEqual(base, "main")

    def test_configured_base_overrides_candidates(self):
        values = {
            ("branch", "--show-current"): "feature/orders",
            ("config", "--get", "review-atlas.baseBranch"): "release/next",
            ("rev-parse", "--verify", "release/next^{commit}"): "abc123",
        }

        with mock.patch.object(CLI, "github_pull_request_base", return_value=None):
            with mock.patch.object(
                CLI,
                "git_value",
                side_effect=lambda arguments, cwd: values.get(tuple(arguments)),
            ):
                scope = CLI.detect_branch_scope(Path("."))

        self.assertEqual(scope, ("feature/orders", "release/next"))

    def test_pull_request_base_has_highest_precedence(self):
        def git_value(arguments, cwd):
            if arguments == ["branch", "--show-current"]:
                return "feature/orders"
            if arguments == [
                "rev-parse",
                "--verify",
                "origin/release/next^{commit}",
            ]:
                return "abc123"
            return None

        with mock.patch.object(
            CLI, "github_pull_request_base", return_value="release/next"
        ):
            with mock.patch.object(CLI, "git_value", side_effect=git_value):
                scope = CLI.detect_branch_scope(Path("."))

        self.assertEqual(scope, ("feature/orders", "origin/release/next"))


class InstallTests(unittest.TestCase):
    def test_install_link_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            destination = root / "nested" / "skill"
            source.mkdir()

            first = CLI.install_link(source, destination)
            second = CLI.install_link(source, destination)

            self.assertIn("Installed", first)
            self.assertIn("Already installed", second)
            self.assertEqual(destination.resolve(), source.resolve())

    def test_install_link_refuses_existing_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            destination = root / "skill"
            source.mkdir()
            destination.mkdir()

            with self.assertRaises(RuntimeError):
                CLI.install_link(source, destination)

    def test_install_link_refuses_destination_inside_source(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            source.mkdir()
            destination = source / ".claude" / "skills" / "review-atlas"

            with self.assertRaisesRegex(RuntimeError, "inside its own source"):
                CLI.install_link(source, destination)

    def test_project_skill_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            destination = CLI.skill_destination("project", project)

            self.assertEqual(
                destination,
                project.resolve() / ".claude" / "skills" / "review-atlas",
            )


class DoctorTests(unittest.TestCase):
    def test_doctor_accepts_project_scope_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            skill = project / ".claude" / "skills" / "review-atlas"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: review-atlas\n---\n")
            args = argparse.Namespace(scope="project", project=str(project))

            with mock.patch.object(CLI.shutil, "which", return_value="/usr/bin/tool"):
                result = CLI.command_doctor(args)

            self.assertEqual(result, 0)

    def test_doctor_accepts_desktop_without_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            skill = project / ".claude" / "skills" / "review-atlas"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: review-atlas\n---\n")
            args = argparse.Namespace(scope="project", project=str(project))

            def executable(name):
                return "/usr/bin/git" if name == "git" else None

            with mock.patch.object(CLI.shutil, "which", side_effect=executable):
                with mock.patch.object(
                    CLI,
                    "find_claude_desktop",
                    return_value=Path("/Applications/Claude.app"),
                ):
                    result = CLI.command_doctor(args)

            self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
