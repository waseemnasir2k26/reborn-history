---
name: Niche fidelity report
about: A generated prompt broke a niche rule (anachronism, genre convention, technical accuracy).
title: "[FIDELITY] Niche: <niche> — Broken rule: <what>"
labels: fidelity, accuracy
assignees: ''
---

## Niche

E.g. cinematic history, abandoned mansion restoration, vintage watch restoration, military aircraft history, ancient ruins exploration.

## What the prompt produced

Paste the offending image-prompt, scene JSON, or VO line.

## What rule broke

Specify the category and the violation:

- [ ] Anachronism (object / costume / language / architecture out of period)
- [ ] Genre convention (e.g. modern cuts in ASMR-craft, jokes in grimdark)
- [ ] Technical accuracy (wrong lens, impossible rig, physics break, brand error)
- [ ] Register / tone drift
- [ ] Other: ___

## Source for the correct rule

Cite the authority — Britannica, manufacturer manual, peer-reviewed paper, monograph, channel reference video timestamp, etc.

## Suggested addition to failsafe / kill list

```
| <Wrong thing> | <Correct rule / earliest year / valid range> | <Common error mode> |
```

## Locale (if relevant)

English / Hindi / Spanish / Arabic / other.

## Reproducibility

How often does it appear (1-of-N regens)? Any specific INPUT field that triggers it?
