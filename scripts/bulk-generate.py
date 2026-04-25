#!/usr/bin/env python3
"""
bulk-generate.py — Reborn Master Prompt Generator (v2.1.0)

Reads niches.json (see niches.example.json) and emits one ready-to-paste
INPUT block per niche, prefixed with the META-PROMPT contents. Output is
written to outputs/staged/{niche}-INPUT.md and (optionally) copied to the
clipboard via pyperclip.

Usage:
    python scripts/bulk-generate.py [--niches niches.json] [--open-claude]

Stdlib only (json, pathlib, webbrowser). pyperclip is optional.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import webbrowser
from pathlib import Path

REQUIRED_FIELDS = ("niche", "youtube_url", "target_tool", "duration", "language", "extra_notes")
ROOT = Path(__file__).resolve().parent.parent
META_PROMPT = ROOT / "META-PROMPT.md"
STAGED = ROOT / "outputs" / "staged"


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "niche"


def validate(entries: list[dict]) -> None:
    if not isinstance(entries, list):
        raise ValueError("niches.json must be a JSON array")
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            raise ValueError(f"entry {i} is not an object")
        missing = [f for f in REQUIRED_FIELDS if f not in e]
        if missing:
            raise ValueError(f"entry {i} ({e.get('niche', '?')}) missing fields: {missing}")


def build_input_block(e: dict) -> str:
    return (
        "## INPUT BLOCK\n\n"
        f"NICHE: {e['niche']}\n"
        f"YOUTUBE_URL: {e['youtube_url']}\n"
        f"TARGET_TOOL: {e['target_tool']}\n"
        f"DURATION: {e['duration']}\n"
        f"LANGUAGE: {e['language']}\n"
        f"EXTRA_NOTES: {e['extra_notes']}\n"
    )


def build_invocation(meta: str, e: dict) -> str:
    return f"{meta.rstrip()}\n\n---\n\n{build_input_block(e)}"


def try_clipboard(text: str) -> bool:
    try:
        import pyperclip  # type: ignore
        pyperclip.copy(text)
        return True
    except Exception:
        return False


def main() -> int:
    p = argparse.ArgumentParser(description="Bulk-stage Reborn master-prompt INPUT blocks.")
    p.add_argument("--niches", default=str(ROOT / "niches.json"), help="Path to niches.json")
    p.add_argument("--open-claude", action="store_true", help="Open https://claude.ai/new per niche")
    args = p.parse_args()

    src = Path(args.niches)
    if not src.exists():
        print(f"[ERR] niches file not found: {src}", file=sys.stderr)
        print(f"[hint] copy {ROOT / 'niches.example.json'} -> {src}", file=sys.stderr)
        return 2
    if not META_PROMPT.exists():
        print(f"[ERR] META-PROMPT.md not found at {META_PROMPT}", file=sys.stderr)
        return 2

    entries = json.loads(src.read_text(encoding="utf-8"))
    validate(entries)
    meta = META_PROMPT.read_text(encoding="utf-8")
    STAGED.mkdir(parents=True, exist_ok=True)

    print(f"[info] staging {len(entries)} niche(s) -> {STAGED}")
    last_block = ""
    for e in entries:
        block = build_invocation(meta, e)
        out = STAGED / f"{slugify(e['niche'])}-INPUT.md"
        out.write_text(block, encoding="utf-8")
        print(f"  wrote {out.relative_to(ROOT)} ({len(block):,} chars)")
        last_block = block
        if args.open_claude:
            webbrowser.open("https://claude.ai/new")

    if try_clipboard(last_block):
        print("[ok] last batch copied to clipboard (pyperclip)")
    else:
        print("[note] pyperclip unavailable — open the staged files manually")
    return 0


if __name__ == "__main__":
    sys.exit(main())
