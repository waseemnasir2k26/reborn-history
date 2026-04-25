# Security

---

## Prompt injection risks

The META-PROMPT and its INPUT block are passed verbatim to a host LLM (Claude / GPT-5 / Gemini). Anything you put in `NICHE`, `YOUTUBE_URL`, or `EXTRA_NOTES` becomes part of the prompt the model executes.

**Never paste into the INPUT block:**

- API keys, OAuth tokens, secrets
- Private credentials (database URLs, S3 access keys, signed URLs)
- PII you do not own (third-party emails, addresses, phone numbers)
- Internal-only documents from clients under NDA

If a YouTube URL points to a video with copyrighted commentary in the title or description, that copy will surface in the generated master prompt. Review before publishing.

## Output safety

The generated master prompts are downstream artifacts. They can in theory be used as carriers for jailbreak instructions if you feed an attacker-controlled `EXTRA_NOTES` into the INPUT block. This is a **known LLM weakness across all prompt-engineering systems**, not a bug specific to this generator. Mitigation: review the master prompt before pasting it into a production pipeline, and never accept third-party `EXTRA_NOTES` without diffing.

## Reference video fetching

This repo does not make remote calls. There is no fetcher, no scraper, no server. When you submit a `YOUTUBE_URL`, the **host LLM** fetches (or fails to fetch) the page — Claude / GPT-5 / Gemini handle the network. We never see your URL or your generated prompts.

## License + attribution

MIT. Free for commercial use. Attribution to `waseemnasir2k26/reborn-history` appreciated, not required. See `LICENSE` for full terms.

## Responsible disclosure

Found a prompt-injection escalation, an output-safety gap, or a quality-gate bypass that produces unsafe master prompts?

Email **waseembali2k26@gmail.com** with subject `[REBORN SECURITY]`. Include: repro steps, the exact INPUT block used, the host LLM + version, and the output excerpt that demonstrates the issue. Do not file public GitHub issues for security reports — disclose privately first.

Acknowledgement target: 72 hours. Patch target: 14 days for high-severity, 30 days for medium.
