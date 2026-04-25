# Recipe — From Master Prompt to 20 Videos

> You generated a master prompt. Now you want to ship 20 videos in that niche. Here is the exact path.

---

## 1. Save the master prompt

Convention: `outputs/generated/{niche}-v{N}.md`

Examples:
- `outputs/generated/mansion-restoration-v1.md`
- `outputs/generated/grimdark-history-v2.md`
- `outputs/generated/luxury-watch-v1.md`

Bump `v{N}` on every regeneration. Never overwrite a deployed prompt — diff lineage matters when downstream videos drift.

Each generated file must carry YAML frontmatter (see `outputs/generated/README.md`) and be registered in `NICHE-REGISTRY.md`.

---

## 2. Per-video TITLE block format

Once the master prompt exists, every new video is just a TITLE block. Paste the master prompt + this block into a fresh chat:

```
[TITLE]
TOPIC: The Fall of Constantinople, 1453
ERA: Late Byzantine
GEOGRAPHY: Constantinople, Bosphorus, Theodosian Walls
DURATION: 12 min
NARRATOR_VOICE: British-RP somber (ElevenLabs Daniel)
KEY_NAMED_FIGURES: Constantine XI, Mehmed II, Giustiniani

[REFERENCE IMAGE] (optional)
<image URL or description>
```

The master prompt's INPUT SYSTEM section defines exactly what fields it expects — read it once, then standardize on that shape for the whole batch.

---

## 3. Tool-specific paste recipes

### Veo 3.1 (JSON-structured scenes)
1. Run master prompt → get script + image prompts + scene JSONs.
2. Generate stills for each scene in **Midjourney v7** (use the MASTER IMAGE TEMPLATE block verbatim, swap `[STAGE]` per scene).
3. Feed each scene JSON to Veo 3.1 directly. Veo expects: `prompt`, `start_state`, `end_state`, `duration_seconds`, `motion_intensity`. The master prompt's SCENE JSON SYSTEM is already in this shape.
4. Stitch in CapCut / Premiere. Audio bed from ElevenLabs (VO) + Suno v4 (music) per AUDIO SYSTEM section.

### Kling 2.5 Master (beat-marker prompts)
1. Get image prompts + scene JSONs.
2. Generate Midjourney stills as start frames.
3. Convert scene JSON to Kling beat-marker format: `[Frame 1 → Frame 2] camera: dolly_in_3s, motion: 6/10, beat at 1.5s`. The master prompt's SCENE JSON already contains the beat data — manually flatten to one prompt line per scene.
4. Kling generates 5s clips. Concatenate.

### Sora 2 (physics-narrative)
1. Skip the JSON schema — Sora prefers natural language with physics cues.
2. From each scene JSON, write a 2-3 sentence narrative: "Camera slowly dollies into a candlelit Byzantine throne room. Shadows lengthen as a single oil lamp flickers. The emperor's hand grips the carved armrest." Embed motion + lighting + duration inline.
3. Sora handles continuity better than Kling — feed previous-scene description as context for the next.

### Midjourney v7 (image prompts only)
1. Use master prompt's `MASTER IMAGE TEMPLATE` block as the structural skeleton.
2. Per-scene: paste TITLE block first, then template, then `--ar 16:9 --style raw --v 7`.
3. Generate 4 variants per scene. Pick the one matching the LIGHTING SYSTEM stage and COLOR GRADING LOCK.

---

## 4. The "next" command flow

Master prompts include `OUTPUT CONTROL` that limits each model response to 2 sections. To get more:

1. Submit master prompt + TITLE.
2. Model emits Section 1 + Section 2 (transitions, image prompts, scene JSONs).
3. Type `next` → model emits Section 3 + Section 4.
4. Repeat until the model emits `[CLOSING]`.

Why: keeps each response under context limits, forces the model to honor CONTINUITY RULE between batches (Image N+1 = Image N + ONE change only).

---

## 5. Where each artifact goes in the tool stack

| Artifact | Where it goes | Tool |
| -------- | ------------- | ---- |
| Image prompts | Stills generator | Midjourney v7 / Flux 1.1 / Nano Banana |
| Scene JSONs | Motion engine | Veo 3.1 / Kling 2.5 / Sora 2 / Runway Gen-4 |
| Script (VO) | Voice synth | ElevenLabs v3 (per NARRATOR_VOICE) |
| MUSIC cues | Music gen | Suno v4 (paste cue: genre + key + BPM + LUFS) |
| SFX cues | Library lookup | Epidemic Sound, Artlist, freesound |
| ON-SCREEN text | Editor titles | CapCut / Premiere lower-thirds |
| Closing line | Final VO + fade | ElevenLabs + CapCut audio fade |

Master prompt → script + images + scene JSONs is one click. Image gen → motion gen → audio is the manual production loop.
