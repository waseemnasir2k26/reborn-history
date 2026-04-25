# Troubleshooting

> Common failures and exact fixes. Match your symptom in the heading, apply the fix, re-run.

---

## "Claude timed out at Phase 3"

**Symptom:** Generation stalls partway, output truncates mid-section, or the model returns "I'm having trouble with this request."

**Cause:** META-PROMPT.md + agent context + reference-video transcript exceeds Claude's reasoning budget for a single response.

**Fix:**
- Switch host LLM to **GPT-5** (faster reasoning, slightly weaker register lock — acceptable trade) or **Gemini 2.5 Pro** (2M context, handles longest reference videos).
- Or split: run Agents 01-03 in one session, copy outputs, paste into a fresh session, run 04-05. Lossier but always works.

---

## "YouTube URL won't fetch"

**Symptom:** Model says "I cannot access that URL" or "The video appears to be unavailable."

**Cause:** Video is private, age-gated, region-locked, removed, or behind a login wall.

**Fix — manual paste workaround:**

```
TITLE: <copy from YouTube>
CHANNEL: <channel name>
DURATION: <e.g., 14:32>
FIRST 30 SECONDS — frame by frame:
  0:00–0:03: <describe what is on screen>
  0:03–0:08: <describe>
  0:08–0:15: ...
  0:15–0:30: ...
TRANSCRIPT (first 60s): <paste from YouTube transcript or auto-captions>
3 STILLS: <describe 3 representative frames from middle + end>
```

Quality drops ~20% but the niche profile + structure model still locks correctly.

---

## "Generated prompt is generic / hollow"

**Symptom:** Master prompt has phrases like "various lighting", "appropriate music", "realistic textures" — placeholder language that should never ship.

**Causes (check in this order):**
1. Niche too broad — "history videos" is generic; "grimdark cinematic AI history of medieval plagues" locks. Narrow, regenerate.
2. EXTRA_NOTES too sparse — add at least 3 specific anchors (narrator voice, color grade, LUFS target, register example).
3. Reference video is **<5 minutes** — Agent 02 cannot extract a stable shot-length / pacing profile. Use a longer reference (8-18 min ideal).

---

## "Quality gate failed: variation engine 4×5"

**Symptom:** Compiler agent rejects the output: "Variation engine has only 3 axes / fewer than 5 variants per axis."

**Cause:** Niche too narrow for the canonical 4×5 variation requirement. ASMR knife-forging has limited variation axes (the action *is* the action).

**Fix:**
- Broaden axes: instead of `material × technique`, add `lighting time-of-day × ambient sound × stage of process × camera distance`.
- Or override in EXTRA_NOTES: `EXTRA_NOTES: variation engine target 3 axes × 4 variants — niche has limited natural axes`. The quality gate respects explicit overrides.

---

## "Master prompt is 1200 words, gate requires 1800"

**Symptom:** Output Compiler fails the length gate.

**Fix:** Re-run Agent 05 with `tighten=false` flag, or simply request `loosen` after the master prompt is delivered — the model expands examples and edge cases by 30-40% and pushes past 1800.

If the prompt stays short after `loosen`, the underlying decisions in Phase 4 are thin. Re-run Phase 4 with sharper EXTRA_NOTES.

---

## "Hindi register slipping into Sanskrit"

**Symptom:** Hindi master prompt produces VO with `तस्मात्`, `इदम्`, `तत्र` — Sanskrit drift.

**Cause:** Agent 04 DECISION 9b vocabulary lock allowed era-formal register. The model defaults to Sanskrit-adjacent for "grimdark + reverent + ancient."

**Fix:** Tighten DECISION 9b explicitly:

```
EXTRA_NOTES:
- Hindi register: modern conversational Hindustani (Khari Boli)
- FORBIDDEN vocabulary: Sanskrit-only words (तस्मात्, इदम्, तत्र, यत्र)
- ALLOWED: Urdu-Hindi blend, accessible to a 10th-grade reader
- Reference register: Tim Reborn History Hindi voiceovers
```

---

## "Model produces 8 stages but my niche needs 5"

**Symptom:** Master prompt has 8 stages where 5 would be tighter (e.g., simple 5-step craft).

**Fix:** Override stage count in EXTRA_NOTES:

```
EXTRA_NOTES:
- Stage count: 5 (not 6-10 default)
- Stages: 0=raw_material, 1=shaping, 2=detail, 3=finish, 4=reveal
```

The Prompt Architect respects explicit stage definitions over its niche-default count.

---

## "Different runs give different prompts for the same niche"

**Symptom:** You ran the same INPUT block twice and got materially different master prompts.

**Cause:** No determinism lock. Models sample.

**Fix (current):** Save the first usable output, version it (`niche-v1.md`), and never regenerate without bumping. Use the post-generation commands (`tighten`, `variant`, `flip mode`) to refine — these are deterministic-ish on a single chat.

**Fix (v2.2):** `MODEL_VERSION` + `INPUT_HASH` lock will be added — same hash + same model = same output. Until then, treat regeneration as a versioning event, not an idempotent operation.
