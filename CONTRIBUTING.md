# Contributing

Thanks for considering a contribution. This skill is designed to be forked, extended, and improved by anyone shipping AI-history videos.

## What we want

### High-value PRs

1. **New locales.** Fork the Hindi master prompt as a template (`prompts/legacy/MASTER-PROMPT-REBORN-HINDI.md`). Build a register-lock vocabulary table for your language (e.g. Spanish: archaic register vs. modern; Arabic: Fusha vs. dialectal; Mandarin: 文言 vs. 白话). File new compilations under `prompts/legacy/MASTER-PROMPT-REBORN-<LANG>.md` or — preferred — regenerate via `META-PROMPT.md` with LANGUAGE = your locale.
2. **New variant axes.** Current engine = 6×7×5×5 = 1,050 combos. Propose a 5th axis (SCALE, EMOTIONAL VALENCE, NARRATOR-AGE) and how it interacts with the existing four.
3. **New image-engine sub-prompts.** Add Sora 2 / Wan 2.5 / Hailuo / Pika 2 syntax variations to Phase 2. File a separate `prompts/sub-prompts/PHASE2-<engine>.md`.
4. **More example INPUT blocks.** One per major historical era — antiquity, classical, medieval, early modern, industrial, 20th-century. Especially welcome: non-Western events (Saqoot-e-Granada 1492, Tenochtitlan 1521, Beijing 1900, Bengal Famine 1943).
5. **Anachronism catches.** Found a scene the prompt failed to flag? File an issue with the era, the artifact, and the correct period name/object. We add it to the kill list.

### Lower-value but welcome

- README typos / grammar.
- Better diagrams (drawio / Excalidraw exports OK).
- Cost-tier updates as model pricing changes.
- Workflow improvements to `tools/_build.py`.

## What we don't want

- AI-slop generated PRs (no actual ship-tested videos behind the change). If you're adding a locale, link a published video using your prompt.
- "Refactor for refactor's sake" PRs to the master prompts. They're load-bearing — small re-wordings can break the model's downstream behavior. Bring evidence (5+ regen runs comparing old vs. new prompt) before shipping.
- Removing the anachronism kill list. It's the genre's edge.
- Adding moral commentary or "viewer takeaway" lines. Genre rule: imagery carries the meaning, not narration.

## How to PR

1. Fork the repo.
2. Branch: `feat/<locale-or-feature>` or `fix/<bug>`.
3. If editing a master prompt: include 2 sample Phase-1 outputs (old prompt vs. new prompt) on the same INPUT, in the PR description.
4. If adding a locale: include 1 full Phase-1 output in the new locale, plus your register-lock vocabulary table.
5. Update `CHANGELOG.md` under `[Unreleased]`.
6. Open PR. Tag `@waseemnasir2k26` for review.

## Issue templates

Use the templates under `.github/ISSUE_TEMPLATE/`:

- **Anachronism report** — found a scene the prompt didn't catch.
- **Locale request** — language you want next.
- **Bug** — `_build.py` crash, broken Phase-3 JSON field, etc.
- **Feature request** — new variant axis, new continuation command, etc.

## Code of conduct

Be useful. Don't be a dick. Ship work, not vibes.

## License

By contributing, you agree your contribution will be licensed under MIT, same as the rest of the repo.
