# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.3.0] — 2026-04-25

Two-mode release. Master prompts now branch on whether the niche needs a written script (history, lore, mystery) or is purely visual (restoration, craft, ASMR). When a script is needed, an automatic math pipeline computes scene and image counts from voiceover length.

### Added
- **`INCLUDE_SCRIPT` field** in INPUT block — required, yes/no. Generator asks if missing; never silently defaults.
- **`SCRIPT-TO-SCENES PIPELINE` section** in canonical structure — emitted only when INCLUDE_SCRIPT=yes. 7 steps: emit script → ask user for VO length in minutes → compute TOTAL_SECONDS = MIN × 60 → SCENE_COUNT = floor(SECONDS / 8) → IMAGE_COUNT = SCENE_COUNT + 1 → pair scenes (Scene N = Image N + Image N+1) → distribute scenes across script sections proportionally → emit in 2-section batches.
- **Worked pipeline example** (8-min video → 480 sec → 60 scenes → 61 images) with full per-section distribution table.
- **`SCENE_DURATION_SECONDS` override** in INPUT block (default 8s; can be 5s / 6s / 8s / 10s).
- **Sora 2 special case**: IMAGE_COUNT = SCENE_COUNT (no end-frame needed; Sora generates from a single image).
- **DECISION 12** (INCLUDE_SCRIPT validation) and **DECISION 13** (Pipeline Math) added to Agent 04 prompt architect.
- **OUTPUT CONTROL section** now branches: script-first execution if INCLUDE_SCRIPT=yes; direct image+JSON emission if no.
- **New post-generation commands**: `flip include_script` (toggles mode and regenerates SCRIPT WRITING + PIPELINE).
- **Pipeline anti-fails** (5 new) added to FAILSAFE: emit prompts before VO length asked, forget +1 for image count, break chain rule, non-integer scene count, distribution mismatch.

### Changed
- Canonical structure now flexible: **35 sections** if INCLUDE_SCRIPT=no, **36 sections** if yes (PIPELINE inserted between CHARACTER CONTINUITY and SCENE JSON).
- `META-PROMPT.md` — INPUT block now requires INCLUDE_SCRIPT; PHASE 4 has 13 decisions (was 11); OUTPUT INSTRUCTION asks for missing INCLUDE_SCRIPT before generating.
- `templates/MASTER-PROMPT-TEMPLATE.md` — added SCRIPT-TO-SCENES PIPELINE skeleton and conditional OUTPUT CONTROL section.
- `agents/04-prompt-architect.md` — added DECISION 12 (validation) and DECISION 13 (math, 6 subsections covering steps, worked example, scene-duration override, Sora override, distribution rule, anti-fails).
- `agents/05-output-compiler.md` — assembly order now conditional (35 vs 36); 8 new quality gates for INCLUDE_SCRIPT logic and pipeline correctness.
- `SKILL.md` — version 2.2.0 → 2.3.0; description updated with pipeline math; new commands documented.

### Why this matters

Two real-world workflows were colliding inside one master prompt:

1. **Script-driven niches** (history, lore, mystery, "what happened to") — user writes the script first, times it, then needs to know exactly how many image generations and motion clips to budget. Without the math, users were over-generating images, under-generating clips, or hitting non-continuous scene cuts.

2. **Pure-visual niches** (mansion / hotel / castle restoration, watch / car detailing, ASMR-craft, aesthetic loops) — no script ever, scene count comes from stage progression × pacing. Asking these users to choose a narration mode wastes their time.

v2.3.0 splits cleanly: the master prompt itself adapts to which kind of channel the user is running, and when math is needed, it's exact (floor for scene count, +1 for chained-frame images, Sora override for single-image scenes).

### Backward compatibility
v2.2.0 master prompts continue to work — they implicitly assumed INCLUDE_SCRIPT=yes for narration niches and silent for visual niches. New users get the explicit toggle; existing users can re-generate with the toggle when they want the SCRIPT-TO-SCENES PIPELINE math.

---

## [2.2.0] — 2026-04-25

Production-readiness release. Three critical fixes from real-world testing of v2.1.0 (the historical-reconstructions test output revealed gaps that this release closes).

### Added
- **NUMBERING CONSISTENCY RULE** (META-PROMPT, Agent 04 Decision 11) — every emitted master prompt picks ONE numbering scheme (Section-aligned 1-indexed OR Process-aligned 0-indexed) and applies it to HIGH RETENTION SYSTEM, STAGES, PACING, AUDIO, LIGHTING, and SCRIPT. Eliminates the "Sections 1–8 vs Stages 0–8" inconsistency seen in v2.1.0 output.
- **CHARACTER / SUBJECT CONTINUITY** as section #30 of the canonical structure — always present (with `method: none` if no named subjects exist).
- **CHARACTER CONTINUITY METHODS** block in META-PROMPT covering Midjourney v7 (`--cref --cw`), Flux 1.1 Pro (LoRA), Kling 2.5 Master (first-frame pinning), Runway Gen-4 (`@reference` tags), Sora 2 (storyboard cards), VEO 3.1 (`image_condition`).
- **Character Lock field** in MASTER IMAGE TEMPLATE — every still-image prompt now carries the tool-specific lock syntax inline.
- **Character lock failure triggers** in FAILSAFE list (face shape change, dress change, distinguishing-mark drift, missing reference URL).
- **DECISION 10** (Character Continuity Method) and **DECISION 11** (Numbering Scheme) added to Agent 04 prompt architect.
- **Valid Scene JSON schema** — proper angle-bracket placeholders (`<int>`, `<string>`, `<true|false>`), no empty fields, parses as valid JSON when filled.
- **Worked Scene JSON example** with real values (Pliny the Younger / Misenum scene) so downstream models know the exact shape to emit.
- **Tool-specific Scene JSON extensions** for VEO 3.1, Kling 2.5, Runway Gen-4, Sora 2, Midjourney v7.
- **Niche-specific Scene JSON extensions** for history (period_lock_check), restoration (completion_pct, regression_check), ASMR-craft (avg_shot_length_seconds).
- New post-generation commands: `flip numbering`, `flip character lock to {method}`.

### Changed
- Canonical structure expanded from 34 to **35 sections** (CHARACTER / SUBJECT CONTINUITY inserted between MASTER IMAGE TEMPLATE and SCENE SYSTEM).
- `META-PROMPT.md` — PHASE 4 now has 11 decisions (was 9); added Decision 10 (character continuity) and Decision 11 (numbering scheme).
- `agents/04-prompt-architect.md` — DECISION 7 expanded with full schema + tool-specific + niche-specific extensions; DECISION 8 adds `Character Lock:` field; DECISION 10 + 11 added.
- `agents/05-output-compiler.md` — assembly order updated to 35 items; quality gates expanded with 4 new checks (numbering consistency, JSON validity, character lock presence, character lock syntax).
- `templates/MASTER-PROMPT-TEMPLATE.md` — Character Lock field in template skeleton; Scene JSON skeleton now uses valid placeholder syntax.
- `SKILL.md` — version bumped 2.1.0 → 2.2.0; section list updated to 35; numbering rule + character continuity rule documented; new commands listed.

### Fixed (root causes documented)
- **Stage numbering inconsistency** — v2.1.0 master prompts could mix "Section 1–N" with "Stage 0–N" in the same output. Now enforced by Decision 11 + quality gate.
- **Scene JSON malformed** — v2.1.0 emitted `"scene": ,` and `"focal_length_mm": ,` (empty values stripped during PDF rendering). Now uses `<int>` placeholders and includes a fully-emitted real-values example so the downstream model never produces empty fields.
- **Character continuity unspecified** — v2.1.0 said "named figure must have locked appearance" but gave no method. Now requires explicit tool-specific lock syntax in MASTER IMAGE TEMPLATE and a dedicated CHARACTER CONTINUITY section.

### Rationale
v2.1.0 was used to generate a real master prompt for the historical-reconstructions niche. That output was 95% production-ready but had three blockers: numbering ambiguity (downstream model would have been confused about which is "first"), invalid JSON (would have crashed VEO3 and Kling), and missing character lock method (would have caused face-drift across sections — Midjourney's well-known weak point). v2.2.0 closes all three. The historical test output's content quality stays — what changes is how reliably any user can take the output and run it through a real pipeline without manual patching.

---

## [2.1.0] — 2026-04-25

### Added
- `SCRIPT WRITING SYSTEM` section to the canonical master-prompt structure (now 34 sections, was 33)
- Section is **always present** with explicit `MODE`: `full-narration` / `minimal-narration` / `text-only` / `silent`
- Register lock: tone, wpm, sentence length, vocabulary, direct-address rules, person, reading level
- Hook formula: second-by-second breakdown of first 8 seconds + open-loop planting
- Section-level script structure: word count + duration + tone + mandatory content per section
- Retention mechanics: open loop, mini-payoff cadence, named-subject introduction, pattern interrupts, curiosity gaps
- On-screen text rules: char limits, hold times, fonts, positioning, use cases, forbidden patterns
- Cue notation reference: `[SFX: ...]`, `[MUSIC IN/OUT/SWELL/DUCK]`, `[PAUSE: Ns]`, `[BEAT]`, `[SOURCE: ...]`, `[ON-SCREEN: ...]`
- Closing-line formula with forbidden CTAs
- Script anti-fail list (6+ niche-specific failures per niche)
- Script output format example (worked 2-section + closing example)
- New post-generation commands: `script only`, `flip mode to {full|minimal|text-only|silent}`

### Changed
- `META-PROMPT.md` — PHASE 4 now has 9 architectural decisions (was 8); added DECISION 9 — Script System
- `agents/04-prompt-architect.md` — added DECISION 9 (subsections 9a–9j) covering the full script architecture
- `agents/05-output-compiler.md` — assembly order now 34 items (script slots between AUDIO and LIGHTING); quality gates updated
- `templates/MASTER-PROMPT-TEMPLATE.md` — added SCRIPT WRITING SYSTEM skeleton and updated Structural Contract to require it
- `SKILL.md` — section list bumped to 34, quality gates expanded, new commands documented
- Minimum master-prompt length raised from 1500 to 1800 words to account for new section

### Rationale
Some niches (history, lore, mystery, educational) require scripts to maximize clarity, engagement, and retention. Other niches (ASMR-craft, aesthetic loops) need minimal or zero narration. The previous version of the META-PROMPT had no script architecture at all, leaving downstream models to invent their own VO style. The new MODE-based system makes the niche's voice/text policy explicit and enforceable, while keeping the section flexible enough to span every niche from grimdark history (full-narration) to aesthetic mansion-restoration loops (silent).

---

## [2.0.0] — 2026-04-25

Major release. The repo evolves from a single-niche skill (cinematic AI history) into a niche-agnostic master-prompt generator.

### Added
- `META-PROMPT.md` — paste-and-use generator that takes `NICHE` + `YOUTUBE_URL` and produces a complete master prompt
- `agents/01-niche-intelligence.md` — niche profiling agent
- `agents/02-video-analyzer.md` — reference-video forensic analyzer
- `agents/03-pattern-engine.md` — formula extractor and structure model builder
- `agents/04-prompt-architect.md` — 8-decision architectural designer
- `agents/05-output-compiler.md` — final assembly + quality gates
- `templates/MASTER-PROMPT-TEMPLATE.md` — canonical 33-section output skeleton
- `examples/input-mansion-restoration.md` — non-history example
- `examples/input-luxury-watch-restoration.md` — non-history example
- `MIGRATION-GUIDE.md` — v1 → v2 upgrade path

### Changed
- `README.md` — rewritten for niche-agnostic workflow
- `SKILL.md` — `name` updated to `reborn-master-prompt-generator`, `version` bumped to 2.0.0
- Repo positioning shifted from "history video skill" to "master prompt generator"

### Moved
- `prompts/MASTER-PROMPT-REBORN-ENGLISH.md` → `prompts/legacy/`
- `prompts/MASTER-PROMPT-REBORN-HINDI.md` → `prompts/legacy/`
- `prompts/MASTER-PROMPT-LONG-HINDI.md` → `prompts/legacy/`
- `prompts/MASTER-PROMPT-SHORT-HINDI.md` → `prompts/legacy/`
- These are now examples of what the v2 generator produces, not the primary deliverable

### Preserved
- All 4 v1 master prompts continue to work standalone (zero breaking changes for v1 users)
- `reference/` Tim Reborn agent outputs preserved as a worked example
- MIT license, author credits, `tools/_build.py`

### Backward compatibility
Anyone using the v1 master prompts directly: nothing breaks. Tag `v1.0.0-final` is available for `git checkout` if needed.

---

## [1.0.0] — Initial Release

- 4 hardcoded master prompts for grimdark cinematic AI history (English default + 3 Hindi variants)
- 5-agent reverse-engineering pipeline outputs (one-time, hardcoded to Tim Reborn channel)
- 4 example INPUT blocks (Bubonic Plague, Fall of Baghdad, Pompeii, Great Fire of London)
- `_build.py` markdown → PDF tool
- MIT license
