# Reborn — Master Prompt Generator

> **A meta-skill that turns any niche + reference YouTube video into a reusable master prompt for AI video generation.** Paste your NICHE and a YOUTUBE_URL. Get back a complete, niche-locked master prompt — ready to use for every topic in that niche, forever.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skill format: SKILL.md](https://img.shields.io/badge/format-SKILL.md-blue)](SKILL.md)
[![Output: Master Prompt](https://img.shields.io/badge/output-Master%20Prompt-green)](META-PROMPT.md)

---

## What this is

A **niche-agnostic prompt-generation system**. Where the original `reborn-history` repo produced one hardcoded master prompt for grimdark history videos, this repo produces a **new master prompt for any niche you point it at**.

You give it:

```
NICHE: abandoned mansion restoration
YOUTUBE_URL: https://youtube.com/watch?v=xxxxx
```

It runs a 5-agent reverse-engineering pipeline internally and returns:

- A complete master prompt with 33 sections — priority order, variation engine, stage progression, audio system, lighting system, scene JSON schema, anti-fail rules, style lock — all niche-locked.
- That single master prompt then works for **every topic within that niche**. You never need to regenerate it for a new video — just feed it new TITLEs.

---

## Quick start

### 1. Open `META-PROMPT.md`. Copy the whole file.

### 2. Paste it into Claude / GPT-5 / Gemini 2.5 Pro.

### 3. At the bottom of the meta-prompt, fill in your INPUT block:

```
NICHE: luxury watch restoration
YOUTUBE_URL: https://youtube.com/watch?v=xxxxx
TARGET_TOOL: VEO3
DURATION: longform
LANGUAGE: English
EXTRA_NOTES: ASMR-tier, no narration first 8s
```

### 4. Send. Receive your master prompt.

The model will silently run all 5 phases (Niche Intelligence → Video Analysis → Pattern Engine → Prompt Architect → Output Compiler) and emit the final master prompt only.

### 5. Save the master prompt. Use it for every topic in that niche.

For each new video, just paste the master prompt + a TITLE + (optional) reference image. The master prompt does the rest.

---

## How it works — the 5-agent pipeline

| Agent | File | Job |
| --- | --- | --- |
| 1 — Niche Intelligence | [`agents/01-niche-intelligence.md`](agents/01-niche-intelligence.md) | Decode the niche: audience, hook archetype, retention drivers, pacing register, failure conditions |
| 2 — Video Analyzer | [`agents/02-video-analyzer.md`](agents/02-video-analyzer.md) | Reverse-engineer the reference video: shot length, camera grammar, color grade, audio bed, transformation logic |
| 3 — Pattern Engine | [`agents/03-pattern-engine.md`](agents/03-pattern-engine.md) | Distill into a reusable formula and structure model that works for any topic |
| 4 — Prompt Architect | [`agents/04-prompt-architect.md`](agents/04-prompt-architect.md) | Make 8 architectural decisions: priority order, variation engine, stages, audio map, lighting map, anti-fail rules, JSON schema, image template |
| 5 — Output Compiler | [`agents/05-output-compiler.md`](agents/05-output-compiler.md) | Assemble decisions into the canonical 33-section master-prompt format. Strip reasoning. Emit. |

You can run any agent standalone for diagnostics — useful for niche validation, competitive analysis, or auditing existing prompts.

---

## What the output looks like

Every generated master prompt conforms to the structure in [`templates/MASTER-PROMPT-TEMPLATE.md`](templates/MASTER-PROMPT-TEMPLATE.md):

- **PRIMARY OBJECTIVE (PRIORITY ORDER)** — conflict resolution
- **INPUT SYSTEM** — `[TITLE]` + `[REFERENCE IMAGE]`
- **DESIGN AUTONOMY RULE** — what the system never asks the user
- **HIGH RETENTION SYSTEM** — section-level engagement map
- **VISUAL HOOK RULE** — contrast moments
- **VARIATION ENGINE** — 4+ axes × 5+ variants
- **SECTION GENERATION SYSTEM** — order and logic
- **STRUCTURE CONSISTENCY** — what is locked
- **SPATIAL / TEMPORAL CONTINUITY**
- **CAMERA SYSTEM**
- **CONTINUITY RULE / NO REGRESSION RULE / OBJECT PERSISTENCE**
- **{NICHE_PROCESS} STAGES** — 6–10 niche-specific stages
- **MICRO-STAGE DETAIL SYSTEM**
- **STAGE RULES / PROGRESS RULE / SYMMETRY RULE**
- **{NICHE_KEY_MOMENT} RULE** — signature rule (e.g., "epoxy only at stage 6")
- **TRANSITION SYSTEM / PACING**
- **AUDIO SYSTEM** — per-stage SFX + music + VO
- **SCRIPT WRITING SYSTEM** — narration mode + register lock + hook formula + retention mechanics + cue notation + closing formula + script anti-fails + worked output example
- **LIGHTING SYSTEM** — per-stage progression
- **COLOR GRADING LOCK**
- **IMAGE QUALITY SYSTEM**
- **MASTER IMAGE TEMPLATE** — includes `Character Lock:` field
- **CHARACTER / SUBJECT CONTINUITY** — tool-specific lock method (Midjourney `--cref`, Flux LoRA, Kling first-frame, Runway `@ref`, Sora storyboard cards, VEO `image_condition`)
- **SCENE JSON SYSTEM** — valid placeholder schema + worked example
- **OUTPUT CONTROL / FAILSAFE / STYLE LOCK**

### About the Script Writing System

The Script section is **always present**, but its `MODE` adapts to the niche:

- **`full-narration`** — continuous VO, locked register, paced wpm. Used for history, lore, mystery, educational, "what happened to" niches.
- **`minimal-narration`** — short whispered VO under 30 wpm averaged, mostly silence. Used for high-end ASMR-craft.
- **`text-only`** — on-screen text cards, zero VO. Used for aesthetic / cinemagraph / pure-visual niches.
- **`silent`** — no VO, no text — pure SFX + music. Used for loops and abstract aesthetic niches.

Even in `silent` mode the section is still emitted (with VO explicitly forbidden), so the downstream model never has ambiguity about what is and isn't allowed.

### About Character / Subject Continuity

The Character Continuity section is **always present**, but its `method` adapts to the niche and target tool:

- **History / lore / mystery** with named figures → `midjourney_cref` (default) or `flux_lora` (for high-volume channels)
- **Restoration / craft** with anonymous hands → `none`
- **Documentary** with reference photos available → `runway_references`
- **Long-form storytelling** with consistent characters → `sora_storyboard`
- **Pure motion / cinemagraph** → `none`

When `method ≠ none`, every still-image prompt's `Character Lock:` field carries the actual tool syntax (e.g. `--cref https://cdn.midjourney.com/<hash>/0_0.png --cw 100`), so downstream models can paste-and-go.

### About Numbering Consistency

Every master prompt picks ONE numbering scheme and applies it everywhere:

- **Scheme A — Section-aligned (1-indexed):** "Section 1 / Stage 1 — Cold Open" through "Section 8 / Stage 8 — Coda". Used for fixed-arc niches (history, lore).
- **Scheme B — Process-aligned (0-indexed):** "Stage 0 — Abandoned" through "Stage 10 — Final Reveal". Used for transformation niches (restoration, craft).

The HIGH RETENTION SYSTEM, STAGES, PACING, AUDIO SYSTEM, LIGHTING SYSTEM, and SCRIPT WRITING SYSTEM all use the same numbering. No mixed indexing — this was a v2.1.0 bug, fixed in v2.2.0.

See [`examples/`](examples/) for sample inputs and the master prompts they produced.

---

## Repository layout

```
reborn-master-prompt-generator/
├── README.md                                   ← you are here
├── SKILL.md                                    ← Claude skill manifest
├── META-PROMPT.md                              ← THE generator (paste-and-use)
├── LICENSE                                     ← MIT
├── CHANGELOG.md
├── CONTRIBUTING.md
├── MIGRATION-GUIDE.md                          ← how to upgrade from reborn-history v1
├── agents/                                     ← 5-agent pipeline (modular)
│   ├── 01-niche-intelligence.md
│   ├── 02-video-analyzer.md
│   ├── 03-pattern-engine.md
│   ├── 04-prompt-architect.md
│   └── 05-output-compiler.md
├── templates/
│   └── MASTER-PROMPT-TEMPLATE.md               ← canonical output skeleton
├── examples/
│   ├── input-mansion-restoration.md
│   ├── input-grimdark-history.md
│   └── input-luxury-watch-restoration.md
├── prompts/
│   └── legacy/                                 ← original reborn-history master prompts
│       ├── MASTER-PROMPT-REBORN-ENGLISH.md
│       ├── MASTER-PROMPT-REBORN-HINDI.md
│       ├── MASTER-PROMPT-LONG-HINDI.md
│       └── MASTER-PROMPT-SHORT-HINDI.md
├── reference/                                  ← original 5-agent outputs (history niche)
│   ├── 01-niche-intelligence.md
│   ├── 02-video-analysis.md
│   ├── 03-pattern-engine.md
│   ├── 04-prompt-architect.md
│   ├── 05-output-compiler.md
│   ├── tim-reborn-research.md
│   └── style-guide.md
├── tools/
│   └── _build.py                               ← markdown → PDF builder
└── .github/
```

---

## Two-step workflow

**Step 1 — Generate (do this once per niche):**
META-PROMPT + NICHE + YOUTUBE_URL → master prompt for that niche.

**Step 2 — Produce (do this for every video):**
master prompt + TITLE + (optional) REFERENCE IMAGE → script + image prompts + scene JSONs.

The master prompt produced in Step 1 is reusable. You only run the generator once per niche, then feed it to your image/video model with new topics for every video you make.

---

## Example niches this works for

- Abandoned mansion / hotel / castle restoration
- Cinematic AI history (grimdark, golden-hour, mystery, war)
- Ancient ruins exploration / civilization reconstruction
- Luxury car / watch / jewelry detailing and restoration
- Satisfying ASMR-craft (knife forging, leather work, woodworking)
- Mythology and folklore retellings
- "What happened to" mystery / lore breakdowns
- Disaster cinematics (volcanoes, tsunamis, fires)
- Aircraft / ship / weapon technical history
- Travel "what it's like to live in" cultural cinematics

If your niche has a clear visual + audio signature and a repeatable section flow, the generator will produce a good master prompt for it.

---

## Languages

The generator supports any language. Just pass `LANGUAGE: <language>` in the INPUT block. The output master prompt will lock register, vocabulary, and pacing to that language.

For non-English niches, supply a reference video in that language for best results — the Video Analyzer agent will pick up native pacing and register cues.

---

## Stack assumed by generated prompts

The generated master prompts default to the **Midjourney v7 + Kling 2.5 + ElevenLabs v3 + VEO 3.1** stack, but you can override per niche with `TARGET_TOOL` in the INPUT block. Supported targets:

| Layer | Default | Alternatives |
| --- | --- | --- |
| Stills | Midjourney v7 | Flux 1.1 Pro, Nano Banana, Sora 2 (still) |
| Motion | Kling 2.5 Master | Runway Gen-4, VEO 3.1, Sora 2, Wan 2.5, Hailuo |
| Voice | ElevenLabs Multilingual v3 | PlayHT, Cartesia |
| Music | Suno v4 | Epidemic Sound, Artlist |
| Edit | CapCut Pro | Premiere, DaVinci Resolve |
| Upscale | Topaz Video AI | Runway upscaler |

---

## Contributing

PRs welcome — especially:

- New example niches (input + the master prompt it produced)
- Locale-specific register notes (vocabulary tables, pacing rules)
- Tool-specific JSON schema additions (Sora 2, Wan 2.5, Hailuo)
- Improvements to the agent prompts (better failure detection, sharper variants)

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Migration from reborn-history v1

If you were using the original `reborn-history` (history-niche-only) version, see [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md). The 4 original master prompts (English, Hindi long, Hindi short, Hindi grimdark) are preserved in `prompts/legacy/` and continue to work standalone — they are now examples of what the generator produces.

---

## Credits

- **Architecture parent:** `reborn-history` (the history-niche-specific predecessor)
- **Reference channel for the original:** [Tim - Reborn History](https://www.youtube.com/@Tim_Reborn_History)
- **Built by:** [Waseem Nasir](https://www.waseemnasir.com) / [SkynetLabs](https://www.skynetjoe.com)

---

## License

MIT — free for commercial use. Attribution appreciated, not required.
