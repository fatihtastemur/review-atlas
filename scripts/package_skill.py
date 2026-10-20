#!/usr/bin/env python3
"""Build a minimal, reproducible ReviewAtlas .skill archive."""

from __future__ import annotations

import argparse
import os
import tempfile
import zipfile
from pathlib import Path


SKILL_NAME = "review-atlas"
RUNTIME_ENTRIES = ("SKILL.md", "LICENSE", "assets", "references")
ARCHIVE_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def validate_source(source: Path) -> None:
    missing = [entry for entry in RUNTIME_ENTRIES if not (source / entry).exists()]
    if missing:
        raise RuntimeError("Missing required package entries: " + ", ".join(missing))

    skill_content = (source / "SKILL.md").read_text(encoding="utf-8")
    if not skill_content.startswith("---\n"):
        raise RuntimeError("SKILL.md must start with YAML frontmatter")
    frontmatter = skill_content.split("---", 2)[1]
    if "name: review-atlas" not in frontmatter:
        raise RuntimeError("SKILL.md must declare name: review-atlas")
    if "description:" not in frontmatter:
        raise RuntimeError("SKILL.md must declare a description")


def package_files(source: Path) -> list[Path]:
    files: list[Path] = []
    for entry in RUNTIME_ENTRIES:
        path = source / entry
        if path.is_file():
            files.append(path)
            continue
        for candidate in path.rglob("*"):
            if candidate.is_symlink():
                raise RuntimeError(f"Refusing to package symlink: {candidate}")
            if candidate.is_file() and not any(
                part.startswith(".") for part in candidate.relative_to(source).parts
            ):
                files.append(candidate)
    return sorted(files, key=lambda path: path.relative_to(source).as_posix())


def write_archive(source: Path, destination: Path) -> Path:
    source = source.resolve()
    validate_source(source)
    files = package_files(source)
    destination.parent.mkdir(parents=True, exist_ok=True)

    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=destination.parent, prefix=f".{SKILL_NAME}-", suffix=".tmp", delete=False
        ) as temporary:
            temporary_path = Path(temporary.name)

        with zipfile.ZipFile(
            temporary_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as archive:
            for path in files:
                relative = path.relative_to(source).as_posix()
                info = zipfile.ZipInfo(f"{SKILL_NAME}/{relative}", ARCHIVE_TIMESTAMP)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (0o644 & 0xFFFF) << 16
                archive.writestr(info, path.read_bytes())

        os.replace(temporary_path, destination)
        destination.chmod(0o644)
    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()

    return destination


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="ReviewAtlas repository root",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("dist"),
        help="Directory for review-atlas.skill",
    )
    return parser


def main() -> int:
    args = create_parser().parse_args()
    destination = args.output_dir.resolve() / f"{SKILL_NAME}.skill"
    try:
        archive = write_archive(args.source, destination)
    except (OSError, RuntimeError, zipfile.BadZipFile) as error:
        print(f"error: {error}")
        return 1
    print(f"Packaged: {archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
