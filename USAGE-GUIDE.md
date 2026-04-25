# Reborn Forge — Usage Guide

> **Niche-agnostic master-prompt generator for AI video.**
> Paste NICHE + YOUTUBE_URL → get a 34-section cinematic master prompt → reuse it for every topic in that niche.

**Repo:** https://github.com/waseemnasir2k26/reborn-forge
**Version:** v2.2.0 — 2026-04-25
**License:** MIT

---

## What it does

Generates a **niche-locked master prompt** that you reuse across an entire video channel. One run produces one master prompt for one niche. That master prompt then handles every TOPIC inside that niche — feed new TITLEs, get new videos.

The system runs Phase 0 (niche-type classifier) + 5 agents internally:
1. **Niche Intelligence** — audience, hook, retention, pacing, failure conditions
2. **Video Analyzer** — reverse-engineer reference video (shots, camera, color, audio)
3. **Pattern Engine** — extract reusable formula
4. **Prompt Architect** — 9 architectural decisions including SCRIPT WRITING SYSTEM
5. **Output Compiler** — assemble 34-section master prompt + apply 4 quality gates

---

## What you need

- **LLM with 200K context.** Claude Pro / GPT-5 / Gemini 2.5 Pro. (Free tiers time out mid-generation.)
- **Reference YouTube video.** Public, ≥ 5 minutes, voice + visuals.
- **A niche idea.** Concrete, not vague. "Luxury watch restoration" works. "Motivational content" does not.
- **Optional:** Veo 3.1 / Kling 2.5 / Sora 2 / Midjourney v7 account for downstream video production.

**Cost:** ~$0.50 per master prompt (~80K input tokens). ~$0.02 per video generation thereafter.

---

## MODE 1 — Generate ONE master prompt (most common)

### Step 1. Copy the kernel

Open https://github.com/waseemnasir2k26/reborn-forge/blob/main/META-PROMPT.md

Click **Raw**. Select all. Copy.

### Step 2. Paste into Claude

Open https://claude.ai/new. Paste the entire META-PROMPT.md content into the chat box.

### Step 3. Append your INPUT block

Below the pasted content, add:

```
NICHE: vintage luxury watch restoration
YOUTUBE_URL: https://youtube.com/watch?v=xxxxx
TARGET_TOOL: Kling 2.5
DURATION: longform
LANGUAGE: English
EXTRA_NOTES: ASMR-tier, hands only, macro 100mm + wide 35mm, ultrasonic SFX foreground
```

Field reference:
- **NICHE** (required) — concrete sub-niche
- **YOUTUBE_URL** (required) — one reference video
- **TARGET_TOOL** (optional, default VEO3) — Kling 2.5 / Sora 2 / Runway Gen-4 / Midjourney+Kling stack
- **DURATION** (optional, default longform) — short (45–60s) / longform (8–18 min)
- **LANGUAGE** (optional, default English) — any language
- **EXTRA_NOTES** (optional) — niche-specific constraints

### Step 4. Submit

Wait 45–90 seconds. Claude runs Phase 0 + 5 agents silently and returns one artifact: the 34-section master prompt (1800+ words).

### Step 5. Save it

Save to `outputs/generated/{niche-slug}-v1.md` with required YAML frontmatter:

```yaml
---
generated: 2026-04-25T16:18:00Z
model: Claude 3.5 Sonnet
meta_prompt_version: 2.2.0
niche: vintage-luxury-watch-restoration
youtube_url: https://youtube.com/watch?v=xxxxx
input_hash: <sha256 of INPUT block>
---
```

Then register it in `NICHE-REGISTRY.md` (one row per generated prompt).

---

## MODE 2 — Generate videos from saved master prompt

### Step 1. Load master prompt

Open your saved master prompt (e.g. `outputs/generated/watch-restoration-v1.md`). Copy it. Paste into a fresh Claude session.

### Step 2. Append TITLE

```
TITLE: Restoring 1968 Rolex Submariner 5513 from rust-locked junk find
REFERENCE IMAGE: https://example.com/sub-rust-still.jpg   (optional)
```

### Step 3. Submit

Claude emits the first 2 sections:
- Image prompts (one per stage)
- Scene JSON (camera, motion, audio, duration)
- Script block (VO + cues)

Type `next` for sections 3–4. Repeat until video complete.

### Step 4. Pipe to tools

| Artifact | Goes to |
|----------|---------|
| Image prompts | Midjourney v7 / Flux / Nano Banana |
| Scene JSONs | Kling 2.5 / Veo 3.1 / Sora 2 / Runway Gen-4 |
| Script + cue notation | ElevenLabs / your VO pipeline |
| On-screen text | After Effects / Premiere |

Per-tool paste recipes live in `RECIPE.md`.

---

## MODE 3 — Batch generate 5+ master prompts at once

### Step 1. Build niches.json

Copy `niches.example.json` to `niches.json`. Add 5+ entries:

```json
[
  {"niche": "abandoned mansion restoration", "youtube_url": "https://youtu.be/...", "target_tool": "VEO3", "duration": "longform", "language": "English", "extra_notes": "ASMR sleep-listen, no faces, teal-shadow grade"},
  {"niche": "vintage luxury watch restoration", "youtube_url": "https://youtu.be/...", "target_tool": "Kling 2.5", "duration": "longform", "language": "English", "extra_notes": "macro 100mm + wide 35mm, hands only"}
]
```

### Step 2. Run orchestrator

```bash
cd C:\Users\info\OneDrive\Desktop\GITHUB\AI-HISTORY-VIDEO-SYSTEM
python scripts/bulk-generate.py
```

Outputs `outputs/staged/{niche-slug}-INPUT.md` per entry — each ready to paste into a fresh Claude tab.

### Step 3. Parallel submit

Open 5 Claude tabs. Paste each staged file. Submit all in parallel. Save outputs.

---

## In-session commands (after master prompt loaded)

| Command | What it does |
|---------|--------------|
| `next` | Emit next 2 sections |
| `variant` | Regen VARIATION ENGINE with different axes |
| `tighten` | Cut output 30–40% (keep rules, drop examples) |
| `loosen` | Expand examples 30–40% |
| `script only` | Emit only SCRIPT WRITING SYSTEM section |
| `flip mode to silent` | Regen script in silent mode |
| `flip mode to full-narration` | Regen script with full VO |
| `niche type` | Show Phase 0 classification |
| `validate` | Run all v2.2 quality gates against output |
| `show phase 1` | Reveal niche intelligence (audience/hook/retention) |
| `show phase 2` | Reveal video analysis (shots/grammar/audio) |
| `rebuild scene N` | Regenerate scene N w/ same constraints |
| `part 2` | Continue script past current section |

---

## v2.2 Quality gates (auto-applied)

Every master prompt must pass:

**Structure:** 34 sections present · no unfilled `{placeholders}` · ≥ 1800 words · 8+ FAILSAFE rules

**Variant safety:** 4+ axes × 5+ variants · combinatorial budget ≥ 300 · independent axes (no correlation)

**Script:** explicit MODE · register lock w/ tone+wpm+sentences+vocabulary · hook formula 0:00–0:08 · 4+ retention mechanics · hook-to-open-loop traceable to a section number with closing VO · locale-native forbidden-word list

**Audio-visual coherence:** hook SFX permitted in Stage 0/1 · no orphan audio cues · music in/out aligned to section boundaries

Type `validate` after generation to re-run all gates.

---

## When things break

| Symptom | Fix |
|---------|-----|
| Claude times out at Phase 3 | Switch to GPT-5 or Gemini 2.5 Pro |
| YouTube URL won't fetch | Paste manual transcript (title + channel + first 30s + 3 stills) |
| Output is generic / hollow | Check niche-type, tighten EXTRA_NOTES, ensure reference video > 5 min |
| Quality gate fail (variation) | Niche too narrow — broaden axes |
| Length < 1800 words | Re-run Agent 05 with `loosen` |
| Hindi register slips into Sanskrit | Add specific forbidden words to Decision 9b |
| Wrong stage count | Override in EXTRA_NOTES: `STAGES: 5` |
| Different runs = different prompts | Lock MODEL_VERSION + INPUT_HASH (v2.2 fingerprint) |

Full coverage: `TROUBLESHOOTING.md`.

---

## Read order when overwhelmed

1. **README.md** — hero + 5-step quick start
2. **USAGE-GUIDE.md** — this file
3. **META-PROMPT.md** — the kernel itself
4. **RECIPE.md** — per-tool paste recipes (Veo / Kling / Sora / MJ)
5. **NICHE-REGISTRY.md** — track every generated prompt
6. **ARCHITECTURE.md** — how the 5 agents fit together
7. **FAQ.md** — cost, language, commercial use, rollback
8. **TROUBLESHOOTING.md** — when stuck
9. **SECURITY.md** — prompt injection, attribution, disclosure

---

## Brand + lineage

- **v1.0.0** — single-niche AI history skill (Tim Reborn-style grimdark)
- **v2.0.0** — kernel generalized into META-PROMPT.md
- **v2.1.0** — SCRIPT WRITING SYSTEM section added
- **v2.2.0** — Phase 0 classifier + 4 quality gates + reuse infrastructure
- **Repo renamed** 2026-04-25: `reborn-history` → `reborn-forge` (matches niche-agnostic scope)

Pairs with **Skyline Reborn** (Naeem Saleem persona Gumroad SKU) and **Naeem Timelapse Renovation** (VEO3 mansion-restoration product). Same imperative-prompt style, same MD→PDF pipeline. Reborn Forge is the **generator**; the Naeem products are videos built using prior versions of this system.

---

## Contact

- Bugs / feature requests: https://github.com/waseemnasir2k26/reborn-forge/issues
- Security disclosure: waseembali2k26@gmail.com — subject `[REBORN SECURITY]`
- License: MIT — free for commercial use, attribution appreciated not required
