#!/usr/bin/env python3
"""Convert .txt files to .md for an Obsidian vault.

Usage:
    python txt_to_md.py <source_folder> <vault_folder>

- Walks <source_folder> recursively and keeps the same subfolder layout.
- Writes UTF-8 .md files; originals are left untouched.
- Turns "•" bullets into Markdown "-" bullets and fixes Windows line endings.
- Skips any .md that already exists (use --overwrite to replace).
"""
import argparse
import re
from pathlib import Path


def read_text(path: Path) -> str:
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not decode {path}")


def to_markdown(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = []
    for line in text.split("\n"):
        # "• Squat 3x5" / "· Bench" -> "- Squat 3x5"
        line = re.sub(r"^(\s*)[•·▪◦]\s*", r"\1- ", line)
        lines.append(line.rstrip())
    return "\n".join(lines).strip() + "\n"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source", type=Path, help="folder containing .txt files")
    p.add_argument("vault", type=Path, help="Obsidian vault folder (or a subfolder in it)")
    p.add_argument("--overwrite", action="store_true", help="replace existing .md files")
    args = p.parse_args()

    converted = skipped = 0
    for txt in sorted(args.source.rglob("*.txt")):
        out = args.vault / txt.relative_to(args.source).with_suffix(".md")
        if out.exists() and not args.overwrite:
            print(f"skip (exists): {out}")
            skipped += 1
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(to_markdown(read_text(txt)), encoding="utf-8")
        print(f"ok: {txt} -> {out}")
        converted += 1

    print(f"\nDone. {converted} converted, {skipped} skipped.")


if __name__ == "__main__":
    main()
