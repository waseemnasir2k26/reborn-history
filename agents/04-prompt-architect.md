# AGENT 04 — PROMPT ARCHITECT

> **Role:** Design the master prompt's section-by-section content using the niche profile, video analysis, and pattern model. This is where the rules, variants, stages, audio map, lighting map, and JSON schema are all decided.

> **Output is not yet the final master prompt** — it is the structured design that Agent 05 (Output Compiler) formats into the canonical layout.

---

## INPUT

```
NICHE_PROFILE: <Agent 01 output>
VIDEO_ANALYSIS: <Agent 02 output>
PATTERN_ENGINE: <Agent 03 output>
TARGET_TOOL: <VEO3 / Kling / Runway / Sora / Midjourney+Kling stack>
DURATION: <short / longform>
LANGUAGE: <EN / HI / ES / etc.>
```

---

## YOUR JOB

Make 8 architectural decisions. Each decision becomes a section in the final master prompt.

---

## OUTPUT FORMAT

```
PROMPT ARCHITECTURE — {NICHE}

DECISION 1 — PRIORITY ORDER
When rules conflict, this order resolves them:
1. {priority_1, e.g., Continuity}
2. {priority_2, e.g., Physical Realism}
3. {priority_3}
4. {priority_4}
5. {priority_5, e.g., Viewer Engagement}

Reasoning: {one line per priority — why it sits at that rank for this niche}

DECISION 2 — VARIATION ENGINE
Axes (4+ required):
- Axis 1: {name} — variants: {5+, named}
- Axis 2: {name} — variants: {5+, named}
- Axis 3: {name} — variants: {5+, named}
- Axis 4: {name} — variants: {5+, named}

No-repeat rule: {what cannot repeat across sections}

Combinatorial budget: {axes_count × variants_each = total combos} — should be ≥ 600 to prevent self-cannibalization across a channel.

DECISION 3 — STAGE PROGRESSION
{6–10 niche-specific stages, numbered 0 through N}
0 — {label}: {what defines stage 0 visually + audibly}
1 — {label}: {what changes from 0}
2 — {label}: ...
...
N — {label, final}: {payoff state}

DECISION 4 — AUDIO SYSTEM
Per-stage map:
Stage 0: SFX = {...}, music = {genre / key / BPM}, VO = {pace / register}
Stage 1–2: SFX = {...}, music = {...}, VO = {...}
Stage 3–5: SFX = {...}, music = {...}, VO = {...}
Stage 6: SFX = {...}, music = {...}, VO = {...}
Stage 7–9: SFX = {...}, music = {...}, VO = {...}
Stage 10 / final: SFX = {...}, music = {...}, VO = {...}

Silence rule: {when silence is allowed / required}
Music-to-VO LUFS gap: {-15 / -20 dB}

DECISION 5 — LIGHTING SYSTEM
Stage 0: {key direction, color temp K, contrast ratio}
Stage 1–5: {progression}
Stage 6: {if special — e.g., reflective surfaces revealed}
Stage 7–10: {warm, cinematic}
Final: {peak — fire / glow / golden hour / etc.}

DECISION 6 — ANTI-FAIL RULES (FAILSAFE list)
List 8+ niche-specific failures that trigger regeneration:
- {failure 1}
- {failure 2}
- ...
- {failure 8+}

Examples:
- For history: "any anachronism flagged in Phase 1 niche profile"
- For restoration: "regression of completed work"
- For ASMR: "VO pace > 145 wpm" or "cuts faster than 4 sec in longform"

DECISION 7 — SCENE JSON SCHEMA

Emit a valid JSON schema with angle-bracket placeholders showing the expected type for each field. Every field must be present in every per-scene JSON the downstream model emits. Numbers unquoted, strings double-quoted, booleans unquoted, no trailing commas, no inline comments.

Base schema (all niches MUST include these fields):

{
  "scene": <int>,
  "section": <int>,
  "stage": <int>,
  "duration_seconds": <int 5..10>,
  "start_state": "<one-sentence description of Image N>",
  "end_state": "<one-sentence description of Image N+1>",
  "camera": {
    "framing_class": "<niche-specific framing label>",
    "focal_length_mm": <int>,
    "movement": "<locked | slow_dolly_in | slow_dolly_out | parallax_2_5d | ken_burns>",
    "movement_seconds": <int>
  },
  "lighting": {
    "key_temp_K": <int>,
    "shadow_density_pct": <int 0..100>,
    "source_count": <int>
  },
  "audio": {
    "music_cue": "<MUSIC IN | MUSIC OUT | MUSIC SWELL | MUSIC DUCK | continue | silent>",
    "sfx": ["<sfx_1>", "<sfx_2>"],
    "vo_present": <true|false>,
    "silence_seconds": <int>
  },
  "character_lock": {
    "method": "<midjourney_cref | flux_lora | kling_first_last_frame | runway_references | sora_storyboard | veo_image_condition | none>",
    "reference_url_or_id": "<URL or LoRA name or 'none'>"
  },
  "rules": [
    "continuity",
    "single action",
    "real process",
    "no instant change"
  ]
}

Tool-specific extensions (add these to the base schema based on TARGET_TOOL):

- **VEO 3.1:** add `"veo_image_condition_url": "<URL>"`, `"audio_prompt_inline": "<full audio description for VEO native audio gen>"`
- **Kling 2.5 Master:** add `"kling_start_frame_url": "<URL>"`, `"kling_end_frame_url": "<URL or null>"`, `"motion_intensity": "<low|medium|high>"`
- **Runway Gen-4:** add `"runway_reference_ids": ["<ref_id_1>", "<ref_id_2>"]`, `"motion_brush_path": "<path_or_null>"`
- **Sora 2:** add `"sora_storyboard_card_id": "<id>"`, `"sora_aspect": "<16:9 | 9:16 | 1:1>"`
- **Midjourney v7 (still gen):** add `"mj_cref_url": "<URL>"`, `"mj_cw": <0..100>`, `"mj_sref_url": "<URL or null>"`, `"mj_aspect": "<16:9 | 9:16>"`

Niche-specific extensions (add based on niche profile):

- For history / period content: `"period_lock_check": "<passed | failed>"`, era-locked rules in `rules` array
- For restoration: `"completion_pct": <int 0..100>`, `"regression_check": "<passed | failed>"`
- For ASMR-craft: `"avg_shot_length_seconds": <number>`, `"audio_foreground_layer": "<sfx description>"`

DECISION 8 — MASTER IMAGE TEMPLATE
The canonical block every still-image prompt conforms to:

[SECTION NAME] — [STAGE NAME]
Camera: {fixed framing rule for this niche}
Lens: {focal length}
Environment: {continuation rule}
Global Condition: ~90–95% complete
Action: ONE clear action
Coverage: full frame
Subjects: {consistency rule for this niche — e.g., "1 worker = 1 task" / "named figure persists across sections"}
Character Lock: {tool-specific syntax from DECISION 10 — e.g. "--cref <URL_FROM_FIRST_APPEARANCE> --cw 100" for Midjourney; or "<lora:name_v1:0.85>" for Flux; or "@reference_name" for Runway}
Lighting: {stage-derived}
Audio: {stage-derived}
Color: {graded per Color Lock}
Quality: 8K ultra detailed, sharp, cinematic
Forbidden: {niche-specific anti-patterns}
Result: stage complete

DECISION 9 — SCRIPT SYSTEM

9a. NARRATION MODE
Pick exactly one based on the niche profile + reference video:
- full-narration → continuous VO across all sections (history, lore, mystery, educational)
- minimal-narration → short whispered VO, ≤30 wpm averaged, mostly silence (high-end ASMR-craft)
- text-only → on-screen text cards, zero VO (aesthetic / cinemagraph / pure-visual niches)
- silent → no VO, no text — pure visual + SFX + music (loops, abstract aesthetic)

9b. REGISTER LOCK
- Tone: {pick one — somber / mysterious / clinical / awe-struck / urgent / reverent / detached-academic}
- VO pace (wpm): {range — sleep-listen 125–140 / neutral 150–165 / energetic 170–190}
- Sentence length: {short staccato 5–9 / flowing 12–20 / mixed}
- Vocabulary: {era-locked / technical / accessible / poetic — give 6–10 register-defining words and 6–10 forbidden words}
- Direct address: {forbidden / minimal / encouraged} — be explicit about the words this means (e.g., "no 'you', 'guys', 'doston', 'friends'")
- Person: {3rd omniscient / 1st witness / 2nd guided}
- Reading level: {target — e.g., grade 8 for accessible, grade 12 for academic}

9c. HOOK FORMULA (first 8 seconds)
Lock the second-by-second behavior:
- 0:00–0:03: {what is on screen + audio state}
- 0:03–0:06: {first VO line trigger or text card}
- 0:06–0:08: {music in / SFX punctuation / pattern interrupt}
- Open loop planted: {the question that must hang in the viewer's mind}
- Forbidden in first 8 sec: {music / direct address / multiple cuts / payoff reveal — list everything banned}

9d. SECTION-LEVEL SCRIPT STRUCTURE
For each of the {N} sections, specify:
- Word count target
- Duration target (seconds)
- Tone (may shift section-to-section within the register)
- Mandatory content (e.g., "section 3 must introduce the named character", "section 5 must deliver the body-count reveal")

9e. RETENTION MECHANICS (4+ required, all enforceable)
- Open loop: planted in section {N}, resolved in section {M}
- Mini-payoff cadence: every {60–90s}
- Named subject (person / place / object) introduced by section {N}
- Curiosity gap pattern: planted every {N} sections, resolved within {M}
- Pattern interrupt: {device — single bell / silence / pull-back zoom} at every {Nth} section
- Number / scale reveal at section {N}
- Other niche-specific mechanics

9f. ON-SCREEN TEXT RULES
- Max chars per card
- Min hold seconds
- Font family (era / register appropriate)
- Position (lower-third / centered / split / corner)
- Use cases (dates, locations, death tolls, quotes, chapter titles)
- Forbidden (emojis, modern slang, clickbait phrasing)

9g. CUE NOTATION
Define the exact inline notation the script uses:
- [SFX: ...]
- [MUSIC IN: ...] / [MUSIC OUT] / [MUSIC SWELL: ...] / [MUSIC DUCK: ...]
- [PAUSE: Ns] / [BEAT] / ...
- [SOURCE: ...] (if niche requires citations — history, science, lore)
- [ON-SCREEN: ...]

9h. CLOSING LINE FORMULA
- Word count cap
- Required structure (e.g., "subject + verb + consequence")
- Must do (fade to silence / land on single image / open next-video loop)
- Forbidden (CTA, "subscribe", "let me know in the comments", direct address)

9i. SCRIPT ANTI-FAIL (6+ niche-specific failures)
List failures that trigger script regeneration. Examples:
- VO pace exceeds wpm cap
- Direct address words used in forbidden register
- Modern reference in period content
- Tonal break (joke, cheerful aside) in serious niche
- Info-dump > {N} consecutive sentences without visual support
- Music in first 8 seconds
- CTA in closing line
- Sentence length > {word cap} in forbidden register
- Etc.

9j. SCRIPT OUTPUT FORMAT (worked example)
Provide a 2-section example showing the exact shape the downstream model must emit:

[SECTION 1 — name]
Duration: Xs
Word count: N
Tone: register

[ON-SCREEN: text]
[SFX: cue]
[MUSIC IN: cue]

VO: line 1
VO: line 2
[BEAT]
VO: line 3

[SECTION 2 — name]
... (same structure)

[CLOSING]
VO: closing line
[MUSIC OUT]
[ON-SCREEN: final card]
```

DECISION 10 — CHARACTER / SUBJECT CONTINUITY METHOD

Pick the lock method based on TARGET_TOOL. The chosen method becomes a section in the master prompt called CHARACTER / SUBJECT CONTINUITY, and the Character Lock field in the MASTER IMAGE TEMPLATE references this method.

10a. WHEN A LOCK IS REQUIRED
- Niche features named figures (history, lore, mystery, biography)
- Niche features focal objects that recur (sword, manuscript, ship, watch, named building)
- Same human subject must appear across 3+ images

10b. WHEN A LOCK IS NOT REQUIRED
- No named/recurring subjects (abstract aesthetic, pure-architecture, satisfying-craft with anonymous hands)
- Each image is self-contained (cinemagraph loops, single-shot ASMR)
- In these cases, set `character_lock.method = "none"` in the JSON schema

10c. PRIMARY LOCK METHODS (pick one or compose)

Midjourney v7 (default for stills):
- Syntax: `--cref <URL_FROM_FIRST_APPEARANCE> --cw 100`
- `--cw 100` = full lock; `--cw 50` = face-only with pose flexibility
- Add `--sref <STYLE_REF_URL>` for video-wide visual consistency

Flux 1.1 Pro / Nano Banana:
- Train a 4–8 image LoRA from first-appearance generations
- Naming convention: `<subject_name>_v1.safetensors`
- Load syntax: `<lora:subject_name_v1:0.85>`

Kling 2.5 Master:
- First-frame pinning across scenes
- Generate stills with character lock (Midjourney/Flux), then feed as Kling start frames
- Optionally pin section N's last frame as section N+1's first frame

Runway Gen-4:
- Upload reference image to Gen-4 References library
- Tag in prompt: `@<reference_name>`
- Max 3 references per scene

Sora 2:
- Define character once at top of storyboard
- Reference by name in subsequent scene cards
- Sora maintains continuity within a single storyboard automatically

VEO 3.1:
- Pass image as `image_condition` parameter
- Use Vertex AI's image conditioning API for multi-shot consistency
- Audio prompt is separate (VEO handles native audio gen)

10d. LOCK FAILURE TRIGGERS (add to FAILSAFE list)
- Named figure's face shape changes between sections
- Named figure's dress / colors change without narrative cause
- Named figure's distinguishing marks (scar, beard, eye color) drift
- Focal object's shape / material changes across appearances
- Character lock URL/ID missing from any scene featuring a named subject

DECISION 11 — NUMBERING SCHEME

Pick ONE of:

Scheme A — Section-aligned (1-indexed):
- "Section 1 / Stage 1 — Cold Open" through "Section N / Stage N — Coda"
- Used when niche has fixed N-section narrative arc (history, lore, mystery, educational)

Scheme B — Process-aligned (0-indexed):
- "Stage 0 — Before / Abandoned / Inert" through "Stage N — Final Reveal"
- Used when niche tracks continuous transformation (restoration, craft, exploration)
- Stage 0 is the "before" state, Stage N is the payoff

ENFORCE: Every section of the master prompt that references stages or sections must use the same scheme. Audit the emitted master prompt for mixed numbering before passing to OUTPUT COMPILER (Agent 05).

---

## RULES

- **Every decision must be specific.** "Audio matches scene" fails. "Stage 0: wind 60 Hz drone -25 LUFS, distant church bell every 12s, no music" passes.
- **Tool-specificity matters.** VEO3 cares about prompt-level audio fields. Kling cares about start/end image fidelity. Sora handles longer durations natively. Tailor the JSON schema accordingly.
- **Variants must be visually distinguishable.** If two variants would render nearly identically, collapse them.
- **Anti-fail rules trump best-practice.** It's better to over-list failures than under-list.
- **Escalation must be encoded in stages.** If stage 7 isn't visibly more premium / intense / large-scale than stage 5, the progression is broken.
- **Numbering must be consistent.** If you pick Scheme A, never reference "Stage 0" anywhere in the prompt. If you pick Scheme B, never reference "Section 1" as a separate concept from "Stage 1".
- **Character lock is mandatory if named subjects exist.** Generic "consistency" rules are not enough — emit the actual tool-specific syntax.
