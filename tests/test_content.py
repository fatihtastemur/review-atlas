from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillContentTests(unittest.TestCase):
    def test_skill_references_exist(self):
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        links = re.findall(r"\[[^]]+\]\(([^)]+\.md)\)", content)

        self.assertGreater(len(links), 10)
        missing = [link for link in links if not (ROOT / link).is_file()]
        self.assertEqual(missing, [])

    def test_skill_frontmatter_identity(self):
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))
        frontmatter = content.split("---", 2)[1]
        self.assertRegex(frontmatter, r"(?m)^name: review-atlas$")
        self.assertRegex(frontmatter, r"(?m)^description: .+$")

    def test_no_unfinished_placeholders(self):
        markdown_files = [ROOT / "SKILL.md", *ROOT.glob("references/**/*.md")]
        unfinished = []
        for path in markdown_files:
            content = path.read_text(encoding="utf-8")
            if "[TODO:" in content or "TBD" in content:
                unfinished.append(str(path.relative_to(ROOT)))

        self.assertEqual(unfinished, [])

    def test_skill_resolves_user_output_language(self):
        content = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("user's preferred language", content)
        self.assertIn("review-atlas.language", content)


if __name__ == "__main__":
    unittest.main()
