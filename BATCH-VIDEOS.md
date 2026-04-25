# Batch Videos — One Session, 20 TITLEs

> Feed 20 topics through one master prompt in a single Claude / Gemini session. Saves context-load overhead, locks register across the whole batch.

---

## Single-session batch format

Paste the master prompt **once**, followed by 20 TITLE entries delimited by `---`:

```
<paste full master prompt here>

[BATCH MODE — 20 videos]

---
[TITLE 1]
TOPIC: The Fall of Constantinople, 1453
ERA: Late Byzantine
GEOGRAPHY: Constantinople, Bosphorus, Theodosian Walls
KEY_NAMED_FIGURES: Constantine XI, Mehmed II, Giustiniani
---
[TITLE 2]
TOPIC: The Antonine Plague, 165 AD
ERA: Roman Empire (Marcus Aurelius)
GEOGRAPHY: Roman provinces, Mesopotamia
KEY_NAMED_FIGURES: Marcus Aurelius, Galen, Lucius Verus
---
... 18 more ...
---

INSTRUCTION: For each TITLE block, emit Section 1 + Section 2 (transitions, image prompts, scene JSONs). Then stop. I will type `next batch` to get the next pair of sections for all 20 videos.
```

---

## Expected output structure

The model returns a 20-block response. Each block:

```
=== VIDEO 1 — The Fall of Constantinople ===
[Section 1 — Cold-Open Atrocity]
TRANSITION IMAGE: ...
IMAGE PROMPT: ...
SCENE JSON: { ... }

[Section 2 — Context Drop]
TRANSITION IMAGE: ...
IMAGE PROMPT: ...
SCENE JSON: { ... }

=== VIDEO 2 — The Antonine Plague ===
...
```

Type `next batch` → next pair of sections for all 20. Repeat until each video hits `[CLOSING]`.

---

## Token budget

| Item | Tokens |
| ---- | ------ |
| Master prompt | ~6K |
| 20 TITLE blocks | ~2K |
| Per-video output (one section pair) | ~3K |
| 20 videos × 1 pair | ~60K output |
| Full run (all 5 section pairs × 20 videos) | ~300K output |

**Requires Claude Pro 200K context** (or Gemini 2.5 Pro 2M context). Free tier will truncate.

---

## When to split sessions

- **>15 videos** — split into 2 sessions of 10. Context bloat past 15 starts degrading register lock (Hindi register slips into Sanskrit, British-RP slips into American neutral).
- **Different sub-niches** — never batch grimdark plagues + grimdark sieges in one run. Run them as separate batches; the variation engine starts repeating motifs across sub-niches.
- **Different LANGUAGES** — always separate. One language per batch.
- **Mid-batch drift detected** — if Video 12 starts feeling generic, stop, save outputs, start a fresh session for Videos 13-20 with the same master prompt.

Track every batch in `NICHE-REGISTRY.md` with the session date, model, and number of videos generated — drift patterns are easier to debug with the registry trail.
