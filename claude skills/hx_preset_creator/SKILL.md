---
name: hx-preset-creator
description: >
  Build complete, ready-to-load HX Stomp presets (.hlx files) from natural-language
  tone requests. Use this skill whenever the user asks for an HX Stomp preset, wants
  to sound like a specific artist or song, describes a guitar or bass tone they want
  to recreate, mentions any Line 6 HX device or HX Edit, or wants help with block
  selection, DSP budgeting, signal chain design, or parameter values for the HX Stomp.
  Trigger even if the user just says "make me a preset" or "I want to sound like X" —
  this skill handles the full pipeline from tone research through .hlx file generation.
---

# HX Stomp Preset Builder

Accept a natural-language tone goal and produce a complete, ready-to-load HX Stomp preset — a `.hlx` file, a Markdown preset map, or both.

All catalog data lives in `references/` inside this skill folder. Scripts for DSP budgeting and parameter normalisation are in `scripts/`.

---

## Step 0 — Load User Preferences

Read `references/user_preferences.md`. If any values are `*(not set)*`:
→ **READ `references/init_protocol.md` NOW**, then run the Init Flow before doing anything else.

If preferences are fully populated, load them and carry them through every step.

**Hard rules — do not break these:**
- Do NOT infer or assume any answer from the user's preset request. Even if the user says "build me a bass preset", still ask Round 1 in full.
- Do NOT skip or combine questions to save time.
- Do NOT proceed to Step 1 until `/skill-creator` has been called and preferences are confirmed written.
- After Round 4, run this checklist before calling `/skill-creator`. Every item must be confirmed:
  - [ ] Instrument make, model, and string count recorded
  - [ ] Pickup type and output level recorded
  - [ ] Signal chain type confirmed (one of the defined options)
  - [ ] cab_simulation value determined (required / not_required)
  - [ ] Send/Return contents recorded — including channels/modes if a multi-channel device is present
  - [ ] All external pedals (before input AND after output) recorded
  - [ ] Output destination recorded
  - [ ] Mono/stereo confirmed
  - [ ] Control mode confirmed
  - [ ] Expression pedal status recorded
  - [ ] Preset style confirmed
  - [ ] Genres recorded
  - [ ] Tone character recorded
  - [ ] Always-include and always-exclude lists recorded

---

## Step 1 — Parse Intent

Extract from the user's request:

```
instrument:      guitar / bass / other (default: guitar)
genre:           [e.g. hard rock, country, jazz, metal]
reference_point: artist, song, album, era, or adjective
mode:            artist clone / song clone / vibe/style / custom description
known_gear:      any gear the user already specified
constraints:     anything to avoid or require
```

**Mode rules:**
- `artist clone` → research the artist's most commonly used live/studio rig for the relevant era.
- `song clone` → research the specific recording (album vs. live may differ).
- `vibe/style` → identify 2–3 archetypal rigs for that genre/era; pick the most versatile.
- `custom description` → map tonal adjectives to amp/pedal character traits (e.g. "creamy" = smooth midrange, low-gain OD).

If the request is ambiguous, ask one clarifying question before proceeding.

---

## Step 2 — Research Tone

**Goal:** Identify the specific amp, cab, and pedal chain. Stop when confident.

**Search priority:**
1. `references/master_blocks.json` `based_on` field — if exact gear is modelled, no external research needed.
2. `helixhelp.com/models` for amp/pedal synopsis.
3. `"[artist] rig rundown"` on YouTube or premierguitar.com.
4. `"[artist] gear [album OR year]"` web search.
5. `"[song] [artist] tone guitar gear"` web search.
6. r/Helix or r/guitar for community-sourced info.
7. Broad web search — last resort.

**Extract:** amp (make/model/channel), cab (size/speaker), drive pedals, modulation, delay, reverb, signal order, any EQ/pickup notes.

**Rules:** Prioritise sources that specify album/era. If sources conflict on amp, note both and prefer the more corroborated one. If exact gear has no HX model, find the closest `based_on` match and note the substitution.

**Output:** a confirmed signal chain — `[wah?] → [drive?] → [amp+cab] → [mod?] → [delay?] → [reverb?]`

---

## Step 3 — Select Blocks

→ **READ `references/block_selection.md` NOW** for the rig filter table, block scoring model, stereo/mono rules, amp+cab pairing table, block order rules, and stacking logic.

Apply the rig filter first (eliminates entire categories), then score remaining candidates, then order them per the block order rules.

---

## Step 4 — Check DSP Budget

Run `scripts/dsp_budget.py`:

```python
from scripts.dsp_budget import check_budget
result = check_budget(
    block_names=[...],   # list of catalog block names in chain order
    stereo=False,        # or True if user rig is stereo
)
print(result.summary())
```

If `result.passes` is False: drop the lowest-priority block (typically reverb first, then secondary mod/delay). Tell the user what was dropped and why.

If any block has `confidence = "unknown"`: note that the DSP estimate for that block is unverified.

---

## Step 5 — Set Parameters

For each block:

1. Start from catalog defaults (`param.default` in `references/master_blocks.json`).
2. Adjust for the researched tone:
   - Drive/gain blocks: transparent boost = low drive + high level.
   - Amp drive: start around 50–60% of max for boosted amps.
   - Amp EQ: start at catalog defaults, adjust mids to match the reference tone.
   - Delay time: if tempo-synced, set `TempoSync1: true` and `SyncSelect1` to the division (6 = quarter note, 9 = dotted eighth, 11 = half note).
   - Delay mix: 20–35% for rhythm/slapback; 40–60% for prominent lead delay.
   - Reverb mix: 15–25% for live tones; 30–50% for ambient/studio.
   - Primary tone blocks: `@enabled: true`. Optional effects: `@enabled: false`.
3. Normalise every value using `scripts/normalize_params.py`:
   ```python
   from scripts.normalize_params import to_normalized
   norm = to_normalized(display_value, param.min, param.max)
   ```
4. Use `param.hlx_key` (NOT the display name) as the key in `.hlx` output.

---

## Step 6 — Ask Output Format

> "Ready to build the preset. Would you like a **Markdown preset map** (readable summary), a **.hlx file** you can load into HX Edit, or **both**?"

Then generate what was requested.

---

## Step 7A — Generate Markdown Preset Map

```
# [Preset Name]
Reference: [artist / song / description]
Instrument: [guitar/bass]
Signal chain: [topology — A / Y-split / etc.]
Total DSP: [X]%

## Signal Chain
[position] [Block Name] ([dsp]%)
  [param display name]: [display value] [unit]
  ...

## Notes
- [What each block is doing in context of the tone]
- [Any substitutions made and why]
- [Suggested first tweaks]
```

---

## Step 7B — Generate .hlx File

Only generate this output if the user requested `.hlx`. If they did:
→ **READ `references/hlx_generation.md` NOW** for the complete JSON template skeleton, block format rules, snapshot configuration, and global settings.

---

## Quick Reference

| Need | Where to look |
|---|---|
| Block symbolicID for `@model` | `block.symbolicID` in `references/master_blocks.json` |
| Parameter key for `.hlx` | `param.hlx_key` in `references/master_blocks.json` |
| Convert display value → float | `scripts/normalize_params.py` → `to_normalized(val, min, max)` |
| DSP budget check | `scripts/dsp_budget.py` → `check_budget([names], stereo=False)` |
| Amp+Cab vs. Preamp, scoring, block order | `references/block_selection.md` |
| Full `.hlx` template and format rules | `references/hlx_generation.md` |
| Init Flow questionnaire | `references/init_protocol.md` |
| Full `.hlx` schema | `references/hlx.schema.json` |

### Critical reminders
- `@model` = `symbolicID` (e.g. `HD2_DistKinkyBoost`), never the catalog `id` field.
- Parameter keys in `.hlx` = `hlx_key` (e.g. `Ch1Drive`), never the display name.
- Parameter values = normalised floats 0.0–1.0, never display units.
- Max 6 blocks per path, max 3 snapshots, max ~95% DSP per chip.
- Amp+Cab blocks are mono-only — for stereo, use Preamp + Cab.
- No Looper or IR blocks in catalog — tell user to configure those manually in HX Edit.
