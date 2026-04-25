# SKILL.md

```yaml
name: reborn-master-prompt-generator
version: 2.2.0
description: |
  Meta-skill that generates a niche-locked master prompt for AI video creation
  given a NICHE and a reference YOUTUBE_URL. Runs Phase 0 (niche-type classifier)
  + 5-agent reverse-engineering pipeline (Niche Intelligence → Video Analysis →
  Pattern Engine → Prompt Architect → Output Compiler) and emits a single
  paste-and-run master prompt conforming to a 34-section canonical structure
  including a SCRIPT WRITING SYSTEM section with mode-based narration
  (full / minimal / text-only / silent), register lock, hook formula, retention
  mechanics, and cue notation. v2.2 adds 4 strict quality gates (variant safety,
  hook-resolution traceability, locale-native register completeness, audio-visual
  coherence). The output prompt is topic-agnostic within the niche and reusable
  across an entire channel.
inputs:
  - NICHE (required)
  - YOUTUBE_URL (required)
  - TARGET_TOOL (optional, default VEO3)
  - DURATION (optional, default longform)
  - LANGUAGE (optional, default English)
  - EXTRA_NOTES (optional)
outputs:
  - master_prompt (markdown, 1800+ words, 34 sections)
entrypoint: META-PROMPT.md
license: MIT
```

---

## How to invoke

1. Open `META-PROMPT.md`. Copy the entire file.
2. Paste into Claude / GPT-5 / Gemini.
3. Append your INPUT block at the bottom.
4. Submit. Receive the master prompt.

## Canonical output sections (34)

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
25. **SCRIPT WRITING SYSTEM** (always present; MODE = full-narration / minimal-narration / text-only / silent)
26. LIGHTING SYSTEM
27. COLOR GRADING LOCK
28. IMAGE QUALITY SYSTEM
29. MASTER IMAGE TEMPLATE
30. SCENE SYSTEM (JSON schema)
31. OUTPUT CONTROL
32. FAILSAFE
33. STYLE LOCK
34. END OF PROMPT marker

## Quality gates

- Variation engine: ≥ 4 axes × ≥ 5 variants
- Stage progression: ≥ 6 niche-specific stages
- Audio system: maps SFX + music + VO to every stage
- **Script Writing System: explicit MODE, full register lock, second-by-second hook formula, ≥ 4 retention mechanics, cue notation reference, closing formula, ≥ 6 anti-fail rules, worked output example**
- Lighting system: progresses across stages
- FAILSAFE: ≥ 8 niche-specific rules
- Style Lock: focal length + grade + tones specified
- Length: ≥ 1800 words (script section adds ~300 words to baseline)
- Zero unfilled `{placeholders}` in final output

## Special commands (post-generation)

- `show phase 1..5` — emit the internal agent output for that phase
- `variant` — regenerate only the VARIATION ENGINE section with different axes/values
- `tighten` — reduce output by 30–40% (keep rules, drop examples)
- `loosen` — expand examples and edge cases by 30–40%
- `script only` — emit only the SCRIPT WRITING SYSTEM section
- `flip mode to {full-narration|minimal-narration|text-only|silent}` — regenerate SCRIPT WRITING SYSTEM with that mode

## Safety / scope

- Does not generate scripts, images, or videos itself — only the master prompt.
- Does not fetch external URLs autonomously beyond what the host model supports. If URL fetch fails, will request manual paste of title + transcript + first-30s frame description.
- No fabricated observations: if the reference video cannot be analyzed, the agent halts and asks the user.
