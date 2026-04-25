# Publish — How to push this skill to GitHub

> Internal Waseem note. Not part of the public skill. Add to `.gitignore` after first push if you want.

## One-time setup

```bash
cd "<repo-root>"   # the directory containing META-PROMPT.md

# Init repo
git init
git branch -M main

# Stage everything except gitignored
git add .
git status   # sanity check — confirm PDF/, _chrome_profile/, _html/ are NOT staged

# First commit
git commit -m "feat: initial public release of reborn-history skill v1.0.0

5-agent reverse-engineered cinematic AI history video generator.
Three-phase pipeline (Script -> Image Prompts -> Scene JSONs).
English (DEFAULT) + Hindi (Urdu-leaning) locales.
Reference: Tim Reborn History X-UgHOce2kk.

- prompts/ x4 master prompts
- reference/ x7 docs (5-agent outputs + Tim Reborn research + style guide)
- examples/ x4 INPUT blocks (plague, Baghdad, Pompeii, Great Fire)
- tools/_build.py (markdown -> PDF)
- .github/ (issue templates + PDF-build workflow)
- MIT license

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>"

# Create GitHub repo + push
gh repo create reborn-history --public \
  --description "Cinematic AI history video skill. 3-phase pipeline (Script -> Image Prompts -> Scene JSONs) reverse-engineered from Tim Reborn History. English DEFAULT + Hindi locale." \
  --homepage "https://www.skynetjoe.com" \
  --source=. \
  --remote=origin \
  --push

# Tag v1.0.0
git tag -a v1.0.0 -m "v1.0.0 — initial public release"
git push origin v1.0.0

# Set repo topics for discoverability
gh repo edit --add-topic ai-video,ai-history,midjourney,kling,elevenlabs,veo,prompt-engineering,claude-skill,faceless-youtube,grimdark,history-channel,reborn-history,hindi-content,cinematic-ai
```

## Post-publish

1. Add a 30-second demo GIF to README (record one Phase-1 → Phase-2 → Phase-3 cycle in Claude/GPT, screen-cap, convert to GIF, upload as `assets/demo.gif`).
2. Pin the repo on your GitHub profile.
3. LinkedIn announcement post (use [`content-template-jarvis-stack`](../../../../.claude/projects/C--Users-info/memory/content-template-jarvis-stack.md) format).
4. X drip — add to [`x-post-pack-apr22`](../../../../.claude/projects/C--Users-info/memory/x-post-pack-apr22.md) rotation.
5. Submit to [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) skill list (PR).

## Updating

```bash
# After edits
git add prompts/ reference/ examples/
git commit -m "<scope>: <change>"
git push

# Bump version when releasing
# 1. update CHANGELOG.md
# 2. git tag -a v1.x.x -m "vX.Y.Z — short summary"
# 3. git push origin v1.x.x
```
