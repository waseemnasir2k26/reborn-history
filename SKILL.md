# SKILL.md

```yaml
name: reborn-master-prompt-generator
version: 2.3.0
description: |
  Meta-skill that generates a niche-locked master prompt for AI video creation
  given a NICHE, YOUTUBE_URL, and INCLUDE_SCRIPT toggle (yes/no). Runs a 5-agent
  reverse-engineering pipeline (Niche Intelligence → Video Analysis → Pattern
  Engine → Prompt Architect → Output Compiler) and emits a single paste-and-run
  master prompt with 35 sections (or 36 if INCLUDE_SCRIPT=yes, adding the
  SCRIPT-TO-SCENES PIPELINE). The pipeline auto-converts script → seconds →
  scene count → image count using floor(seconds/8) for scenes and scenes+1 for
  chained-frame images. Output is topic-agnostic within the niche and reusable
  across an entire channel.
inputs:
  - NICHE (required)
  - YOUTUBE_URL (required)
  - TARGET_TOOL (optional, default VEO3)
  - DURATION (optional, default longform)
  - LANGUAGE (optional, default English)
  - EXTRA_NOTES (optional)
outputs:
  - master_prompt (markdown, 1500+ words, 33 sections)
entrypoint: META-PROMPT.md
license: MIT
```

---

## How to invoke

1. Open `META-PROMPT.md`. Copy the entire file.
2. Paste into Claude / GPT-5 / Gemini.
3. Append your INPUT block at the bottom.
4. Submit. Receive the master prompt.

## Canonical output sections (35 or 36)

Section count depends on INCLUDE_SCRIPT:
- **INCLUDE_SCRIPT = no** → 35 sections (no PIPELINE section)
- **INCLUDE_SCRIPT = yes** → 36 sections (PIPELINE inserted at #31)

The generated master prompt MUST contain, in order:

1. Header line (`You are an AI system specialized in...`)
2. PRIMARY OBJECTIVE (PRIORITY ORDER)
3. INPUT SYSTEM
4. DESIGN AUTONOMY RULE
5. HIGH RETENTION SYSTEM
6. VISUAL HOOK RULE
7. VARIATION ENGINE
8. SECTION GENERATION SYSTEM
9. STRUCTURE / WORLD CONSISTENCY
10. SPATIAL / TEMPORAL CONTINUITY
11. CAMERA SYSTEM
12. CONTINUITY RULE
13. NO REGRESSION RULE
14. OBJECT / ELEMENT PERSISTENCE
15. {NICHE_PROCESS} STAGES
16. MICRO-STAGE DETAIL SYSTEM
17. {KEY_COMPLETION} RULE
18. SYMMETRY / BALANCE RULE
19. STAGE RULES
20. PROGRESS RULE
21. {NICHE_KEY_MOMENT} RULE
22. TRANSITION SYSTEM
23. PACING
24. AUDIO SYSTEM
25. SCRIPT WRITING SYSTEM (always present; MODE matches INCLUDE_SCRIPT — full/minimal if yes, text-only/silent if no)
26. LIGHTING SYSTEM
27. COLOR GRADING LOCK
28. IMAGE QUALITY SYSTEM
29. MASTER IMAGE TEMPLATE (includes `Character Lock:` field)
30. CHARACTER / SUBJECT CONTINUITY (always present; method = midjourney_cref / flux_lora / kling_first_last_frame / runway_references / sora_storyboard / veo_image_condition / none)
31. **SCRIPT-TO-SCENES PIPELINE** (only if INCLUDE_SCRIPT = yes — 7-step math: script → seconds → scenes → images, chained-frame pairing, proportional section distribution)
32. SCENE SYSTEM (JSON schema with valid placeholder syntax + worked example)
33. OUTPUT CONTROL (script-first batched if INCLUDE_SCRIPT=yes; direct image+JSON emission if no)
34. FAILSAFE
35. STYLE LOCK
36. END OF PROMPT marker

If INCLUDE_SCRIPT = no, skip section 31 entirely (the count drops to 35 and #32 becomes the new #31).

## INCLUDE_SCRIPT toggle (CRITICAL — required input)

The user MUST specify whether the niche needs voiceover narration:

- **`yes`** — niche needs continuous narration (history, lore, mystery, educational, "what happened to", documentaries, biographies). The master prompt's downstream behavior is: write script first → ask user for VO length → compute scenes/images → emit batches.
- **`no`** — niche is purely visual (mansion / hotel restoration, watch / car detailing, ASMR-craft, aesthetic loops, satisfying transformations). The master prompt skips script entirely and emits image prompts + scene JSON directly.

If the user does not specify INCLUDE_SCRIPT, the generator ASKS before producing anything else. It never defaults silently.

Niche-family default suggestions (used only when user explicitly asks "what should I pick?"):
- History / lore / mystery / educational / mythology → **yes**
- Restoration / craft / ASMR / aesthetic loops → **no**
- Travel / food / fashion cinematic → either, ask user

## Script-to-scenes pipeline math (when INCLUDE_SCRIPT=yes)

The generated master prompt enforces this exact 7-step flow at runtime:

1. Emit script as text (no images, no JSON yet)
2. Ask user: "What is your target voiceover length in MINUTES?"
3. `TOTAL_SECONDS = VO_MINUTES × 60`
4. `SCENE_COUNT = floor(TOTAL_SECONDS / SCENE_DURATION)` — default SCENE_DURATION = 8s
5. `IMAGE_COUNT = SCENE_COUNT + 1` — chained-frame motion (Sora 2 override: IMAGE_COUNT = SCENE_COUNT)
6. Pair scenes: Scene N uses Image N (start) + Image N+1 (end). Image N+1 is also Image N+1 of the next scene — same image, no jump cuts.
7. Distribute scenes across script sections proportionally; emit prompts in 2-section batches with STOP between.

Worked example: 8-min history video → 480 sec → 60 scenes → 61 images.

## Numbering consistency rule (CRITICAL)

Every emitted master prompt picks ONE numbering scheme and applies it everywhere:
- **Scheme A (Section-aligned, 1-indexed):** Section 1 = cold open, Section N = coda. Used for fixed-arc niches.
- **Scheme B (Process-aligned, 0-indexed):** Stage 0 = before state, Stage N = final reveal. Used for transformation niches.
- HIGH RETENTION SYSTEM, STAGES, PACING, AUDIO, LIGHTING, SCRIPT, and PIPELINE all reference the same scheme.

## Character continuity (CRITICAL when named subjects exist)

If the niche features named figures or recurring focal objects, the master prompt MUST emit tool-specific lock syntax:
- Midjourney v7: `--cref <URL> --cw 100`
- Flux 1.1 Pro: `<lora:name_v1:0.85>`
- Kling 2.5: first-frame pinning
- Runway Gen-4: `@reference_name` tags
- Sora 2: storyboard character cards
- VEO 3.1: `image_condition` parameter

If no named subjects exist, the section still appears with `method: none`.

## Quality gates

- INCLUDE_SCRIPT confirmed by user (never silently defaulted)
- Numbering consistent across all sections (no mixed Section/Stage indexing)
- Variation engine: ≥ 4 axes × ≥ 5 variants
- Stage progression: ≥ 6 niche-specific stages
- Audio system: maps SFX + music + VO to every stage
- Script Writing System: explicit MODE, full register lock, second-by-second hook formula, ≥ 4 retention mechanics, cue notation reference, closing formula, ≥ 6 anti-fail rules, worked output example
- MODE matches INCLUDE_SCRIPT (full/minimal vs text-only/silent)
- Character / Subject Continuity: explicit method + tool-specific syntax in MASTER IMAGE TEMPLATE
- Scene JSON: valid syntax (parses as JSON), filled fields, worked example with real values
- Pipeline section emitted IFF INCLUDE_SCRIPT=yes (no stub if no)
- If pipeline emitted: all 7 steps, worked example, SCENE_DURATION + Sora overrides, ≥ 5 anti-fails
- OUTPUT CONTROL reflects mode (script-first vs direct-emission)
- Lighting system: progresses across stages
- FAILSAFE: ≥ 8 niche-specific rules + character lock failures + pipeline anti-fails (if applicable)
- Style Lock: focal length + grade + tones specified
- Length: ≥ 1800 words (≥ 2100 if INCLUDE_SCRIPT=yes)
- Zero unfilled `{placeholders}` in final output

## Special commands (post-generation)

- `show phase 1..5` — emit the internal agent output for that phase
- `variant` — regenerate only the VARIATION ENGINE section with different axes/values
- `tighten` — reduce output by 30–40% (keep rules, drop examples)
- `loosen` — expand examples and edge cases by 30–40%
- `script only` — emit only the SCRIPT WRITING SYSTEM section
- `flip mode to {full-narration|minimal-narration|text-only|silent}` — regenerate SCRIPT WRITING SYSTEM with that mode
- `flip include_script` — toggle INCLUDE_SCRIPT and regenerate SCRIPT WRITING + PIPELINE sections
- `flip numbering` — switch between Scheme A (Section-aligned) and Scheme B (Process-aligned)
- `flip character lock to {midjourney_cref|flux_lora|kling_first_last_frame|runway_references|sora_storyboard|veo_image_condition|none}` — regenerate CHARACTER CONTINUITY with that method

## Safety / scope

- Does not generate scripts, images, or videos itself — only the master prompt.
- Does not fetch external URLs autonomously beyond what the host model supports. If URL fetch fails, will request manual paste of title + transcript + first-30s frame description.
- No fabricated observations: if the reference video cannot be analyzed, the agent halts and asks the user.
