# Architecture

> How the master-prompt generator works under the hood, and when to break it apart.

---

## 5-phase pipeline (silent, in order)

The model runs all phases internally on a single META-PROMPT.md submission and emits only the final master prompt.

| # | Phase | Agent file | Output |
| - | ----- | ---------- | ------ |
| 0 | **Niche-Type Classifier** *(coming v2.2)* | (planned) `agents/00-niche-type.md` | One of: `transformation-visible` / `retention-driver` / `dialogue-ensemble` / `audio-primary` |
| 1 | Niche Intelligence | `agents/01-niche-intelligence.md` | 6-row niche profile (audience, hook archetype, retention drivers, pacing, failure conditions) |
| 2 | Video Analysis | `agents/02-video-analyzer.md` | Forensic breakdown of YOUTUBE_URL — shot length, camera grammar, color grade, audio bed, transformation logic |
| 3 | Pattern Engine | `agents/03-pattern-engine.md` | Reusable formula + 6–10 section structure model |
| 4 | Prompt Architect | `agents/04-prompt-architect.md` | 9 architectural decisions (priority, variation, stages, audio, lighting, anti-fail, JSON, image template, script) |
| 5 | Output Compiler | `agents/05-output-compiler.md` | Assembled 34-section master prompt + quality gate pass |

### Phase 0 — niche-type classifier (v2.2 preview)

Phase 0 will route the rest of the pipeline. Until it lands, the model auto-detects from NICHE + EXTRA_NOTES. Four buckets:

- `transformation-visible` — restoration, craft, build (the visual change *is* the retention driver). Mansion, watch, knife forging.
- `retention-driver` — narrative pull, escalation, named-subject loops. Grimdark history, true-crime, mystery.
- `dialogue-ensemble` — character-driven, multiple speakers, branching lines. Mythology retellings, lore comedy.
- `audio-primary` — voice/music carries the watch, visuals are aesthetic bed. ASMR, sleep stories, ambient.

Phase 4's DECISION 9 (script MODE) is downstream of this — `audio-primary` defaults to `minimal-narration`, `transformation-visible` often `text-only` or `silent`.

---

## Standalone agent use

Run any agent solo from `agents/{file}.md` when you need **diagnostic output**, not a master prompt:

- **Agent 01** — niche validation before committing. "Is grimdark mythology a generatable niche?" Run 01, read the failure-conditions row, decide.
- **Agent 02** — competitive teardown. Point at any URL, get shot length / color grade / audio bed map.
- **Agent 03** — refactor an existing prompt. Feed it the prompt, get back the implicit pattern + structure model.
- **Agent 04** — audit. Pass an existing master prompt, ask: "Are all 9 decisions fully specified?"
- **Agent 05** — assembly only. If you already have decisions 1-9 written, skip to compiler.

---

## Why 34 sections

Each section closes one ambiguity gap that downstream models otherwise hallucinate around: priority order resolves rule conflicts, variation engine kills repetition, JSON schema locks tool output shape, anti-fail rules cap failure modes, script MODE removes VO-style ambiguity. Drop any section and you reintroduce the gap.

## Why mode-based scripts

Niches range from full-narration grimdark history (170 wpm British-RP) to silent ASMR knife-forging (zero VO). One global script template fails both ends. The four MODEs (`full-narration` / `minimal-narration` / `text-only` / `silent`) cover every practical case while keeping the section *always present* — never omitted, never optional.

---

## Decision tree — fork vs extend vs use-as-is

```
Are you generating one-off prompts for personal use?
  → use-as-is. Paste META-PROMPT.md, fill INPUT, ship.

Are you generating 5+ master prompts in the same family (e.g. 5 history sub-niches)?
  → extend. Add EXTRA_NOTES presets. Save outputs to outputs/generated/.

Adding a new niche type the 4 buckets don't cover (e.g. interactive / branching)?
  → fork. Touch agents/04-prompt-architect.md DECISION 9, add a new MODE,
    raise the canonical section count, bump META-PROMPT.md major version.

Building a different output shape (TikTok 15s, longform podcast, blog)?
  → fork. Replace templates/MASTER-PROMPT-TEMPLATE.md, rewire Agent 05.
```

Default to **use-as-is**. Most "I need to fork" instincts are answered by EXTRA_NOTES + the post-generation commands (`tighten`, `loosen`, `variant`, `flip mode`, `script only`).
