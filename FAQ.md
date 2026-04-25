# FAQ

---

### Can I use this for non-video content (blog, podcast, newsletter)?

Partially. The SCRIPT WRITING SYSTEM section is reusable as-is for podcast scripts and longform blog narration. The IMAGE / SCENE JSON / LIGHTING / CAMERA sections are video-specific and can be ignored. For pure blog use, run Agent 03 (pattern engine) on a top-performing blog and skip Agents 04-05 — the structure model + retention mechanics output is enough on its own.

### Can I commercialize the output master prompts and the videos they produce?

Yes. MIT license, no royalty. Attribution to `waseemnasir2k26/reborn-history` appreciated, not required. The master prompts you generate are **your** artifact — sell, license, gatekeep, whatever.

### What if my reference YouTube video is private or removed?

The host LLM (Claude / GPT-5 / Gemini) tries to fetch the URL. If it can't, it will ask you to manually paste: title, channel, duration, the first 30s described frame-by-frame, transcript snippet, and 3-5 visual stills. Output quality drops ~20% versus a successful fetch but is still usable. See `TROUBLESHOOTING.md` for the manual-paste template.

### How do I know if my niche is generatable?

Three-rule test: (1) clear visual signature you can describe in 2 sentences, (2) repeatable section flow across at least 3 example videos, (3) a defined audio register. If any of those fail, run **Agent 01 standalone** first (`agents/01-niche-intelligence.md`) — if the failure-conditions row is short or generic, the niche is too broad. Narrow it.

### Can I flip the script mode after the master prompt is generated?

Yes. After receiving the master prompt, type `flip mode to {full-narration|minimal-narration|text-only|silent}`. The model regenerates only the SCRIPT WRITING SYSTEM section, leaves the other 33 sections locked.

### Does it work for non-English niches?

Yes. Pass `LANGUAGE: Hindi` (or Spanish, Arabic, French, etc.) in the INPUT block. For best results supply a reference video in the target language — Agent 02 picks up native pacing and register cues. The grimdark-history Hindi sample in `prompts/legacy/MASTER-PROMPT-REBORN-HINDI.md` shows what locked Hindi register output looks like.

### Can I run the agents out of order?

For diagnostics, yes. For full generation, no. The phases compound: 02 needs 01's audience profile, 04 needs 03's structure model, 05 needs 04's 9 decisions. Out-of-order runs produce incoherent locks.

### What does one generation cost?

Roughly **80K input tokens** for the META-PROMPT + agent context, **5-8K output** for the final prompt. On Claude Pro: $0 (within the plan). On API: ~$0.50 USD per generation at Claude Sonnet 4 rates, ~$1.50 at Opus. **Claude Pro is recommended** — you'll regenerate, tighten, variant, flip mode several times per niche.

### Do GPT-5 and Gemini 2.5 Pro work?

Yes, both. GPT-5 is faster, slightly weaker on niche register lock. Gemini 2.5 Pro has the longest context window (2M tokens) — best for batch generation of 20+ videos in one session. Claude Opus 4.7 is the gold standard for the META-PROMPT itself; Phase 4's 9 architectural decisions favor Claude's structured-reasoning bias.

### How do I handle Veo 3.1 vs Kling 2.5 vs Sora 2 differences?

Pass `TARGET_TOOL` in the INPUT block. The generator adapts the SCENE JSON SYSTEM section to that tool's schema:

- **Veo 3.1** — JSON-structured scenes, prompt + start_state + end_state + duration fields.
- **Kling 2.5 Master** — beat-marker prompts, motion intensity 0-10, camera-move tags.
- **Sora 2** — physics-narrative natural language, no rigid JSON.

See `RECIPE.md` for tool-specific paste recipes.
