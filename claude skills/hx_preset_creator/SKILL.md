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

Read `user_preferences.md`. If any values are `*(not set)*`, run the Init Flow below before doing anything else. Do not proceed to Step 1 until all preferences are set.

If preferences are fully populated, load them and carry them through every step.

**Hard rules — do not break these:**
- Do NOT infer or assume any answer from the user's preset request. Even if the user says "build me a bass preset", still ask Round 1 in full.
- Do NOT skip or combine questions to save time.
- Do NOT proceed to Step 1 until `/create-skill` has been called and preferences are confirmed written.
- After Round 4, run this checklist before calling `/create-skill`. Every item must be confirmed:
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

### Init Flow

Collect preferences in four short rounds. Present options as a numbered list wherever possible — do not ask the user to type option names. Wait for answers before moving to the next round.

---

**Round 1 — Your Instrument**

Ask:
> "Before I build your first preset, I need to know about your setup. Let's start with your instrument.
>
> 1. Guitar
> 2. Bass
> 3. Both guitar and bass
> 4. Other (describe)
>
> What do you play, and what's the make and model?"

Follow up:
> "What type of pickups?
>
> 1. Single coils
> 2. Humbuckers
> 3. P-bass (split-coil)
> 4. J-bass (single coil)
> 5. PJ (split + single)
> 6. Active electronics
> 7. Mixed or other (describe)"

---

**Round 2 — Your Rig Connection**

Ask:
> "How is your HX Stomp connected in your rig?
>
> 1. Direct to FRFR speaker or PA (full-range output — cab sim on)
> 2. Direct to audio interface or recording setup (cab sim on)
> 3. Headphones only (cab sim on)
> 4. Into the front input of a guitar/bass amp (no effects loop integration)
> 5. 4-Cable Method — integrated into my amp's effects loop
> 6. In the amp's effects loop only (amp's own preamp feeds into it)
> 7. Into my amp's effects return, bypassing the amp's preamp
> 8. External preamp or amp sim in the HX Stomp's Send/Return loop, DI or line out to PA/interface
> 9. Something else (describe)"

Based on the answer, ask follow-ups:
- If **4, 5, 6, or 7**: "What amp are you using? Make and model?"
- If **5 or 6**: "Is your amp's effects loop series or parallel? (Series = one path, Parallel = wet/dry blend — write 'Unknown' if unsure)"
- If **8**: "What device is in your Send/Return loop?" (then proceed to the Send/Return deep-dive questions below)

Then ask everyone:
> "Do you have anything connected between the HX Stomp's Send and Return jacks?
>
> 1. No — the loop is empty
> 2. Yes — there's a device in the loop (describe it)"

If yes, follow up with:
> "Tell me more about that device:
> - What is it? (make and model)
> - What does it do? (e.g. amp sim, preamp, compressor, reverb)
> - Does it have multiple channels or modes? If so, list them and what each one sounds like.
> - Does it have its own DI or output that goes somewhere, or does it feed back into the HX Stomp Return?"

Then ask:
> "Do you have any pedals or devices in your signal chain that are outside the HX Stomp — either before the input or after the output?
>
> 1. No — the HX Stomp is the only device
> 2. Yes — before the HX Stomp input (describe each one and what it does)
> 3. Yes — after the HX Stomp output (describe each one and what it does)
> 4. Yes — both before and after (describe all of them)"

---

**Round 3 — Output & Control**

Ask:
> "What does your HX Stomp's output connect to? (Describe both outputs if you use both.)"

Then:
> "Mono or stereo?
>
> 1. Mono — I use one output
> 2. Stereo — I use both outputs"

Then:
> "How do you prefer to control the HX Stomp?
>
> 1. Stomp mode — footswitches toggle individual blocks on/off
> 2. Snapshot mode — footswitches recall complete preset states
> 3. Hybrid — mix of both"

Then:
> "Do you use an expression pedal?
>
> 1. No
> 2. Yes — typically for wah
> 3. Yes — typically for volume
> 4. Yes — assigned to something else (describe)"

Then:
> "How do you typically use presets?
>
> 1. One preset per song — each preset is dedicated to a single sound
> 2. Multiple sounds within one preset — I switch between tones mid-song"

---

**Round 4 — Tone Profile**

Ask:
> "What genres or styles do you mostly play? (List as many as apply — e.g. rock, blues, metal, jazz, funk, country, ambient)"

Then:
> "How would you describe your typical tone character? Pick all that apply:
>
> 1. Clean
> 2. Crunch / edge of breakup
> 3. High gain
> 4. Warm
> 5. Bright
> 6. Scooped mids
> 7. Mid-focused
> 8. Vintage character
> 9. Modern / hi-fi"

Then:
> "Are there any effects or blocks you always want in every preset?
>
> 1. No standing requirements
> 2. Yes — always include a tuner block
> 3. Yes — always include a noise gate
> 4. Yes — always start with a compressor
> 5. Yes — something else (describe)"

Then:
> "Are there any effects or block types you want to avoid entirely?
>
> 1. No restrictions
> 2. No pitch shifting or octave effects
> 3. No heavy modulation
> 4. Something specific (describe)"

---

**After Round 4**

Before proceeding, run through the checklist at the top of this Init Flow. If anything is missing, ask the user before continuing.

Once all items are checked off:

**1.** Display the complete filled-in `user_preferences.md` content as a code block so the user can review it. Use the exact field names and option values defined in `user_preferences.md`.

**2.** Ask the user to confirm the content is correct, then say:

> "To save your preferences, please invoke the `/create-skill` command now. Once it confirms the file has been updated, let me know and we'll get straight to building your preset."

**3.** Wait. Do not proceed to Step 1 until the user confirms `/create-skill` completed successfully.

**4.** Once confirmed, say:
> "Your setup is saved. What preset would you like to build?"

---

## Step 1 — Parse Intent

Extract the following from the user's request:

```
instrument:      guitar / bass / other (default: guitar)
genre:           [e.g. hard rock, country, jazz, metal]
reference_point: artist, song title, album, era, or adjective
                 (e.g. "Freewill by Rush", "80s hair metal", "warm clean Fender")
mode:            artist clone / song clone / vibe/style / custom description
known_gear:      any gear the user already specified (amp model, pedal name, etc.)
constraints:     anything the user said to avoid or require
```

**Mode rules:**
- `artist clone` → research the artist's most commonly used live/studio rig for the relevant era.
- `song clone` → research the specific recording. Album vs. live may differ significantly.
- `vibe/style` → identify 2–3 archetypal rigs for that genre/era and pick the most versatile.
- `custom description` → map tonal adjectives to amp/pedal character traits (e.g. "creamy" = smooth midrange, low-gain OD; "fizzy" = high-gain with aggressive high-mids).

If the request is ambiguous (e.g. "something like the Beatles") ask one clarifying question: *which era or album?*

Do not start researching until you have a clear reference point and mode.

---

## Step 2 — Research Tone

**Search goal:** Identify the specific amp, cab, and pedal chain for the reference point.

**Search in priority order — stop when confident:**

1. Check `references/master_blocks.json` `based_on` field first — if the exact gear is already modelled, no external research needed.
2. Search `helixhelp.com/models` for amp/pedal synopsis.
3. `"[artist name] rig rundown"` on YouTube or premierguitar.com.
4. `"[artist name] gear [album name OR year]"` web search.
5. `"[song name] [artist name] tone guitar gear"` web search.
6. r/Helix or r/guitar for community-sourced gear info.
7. Broad web search — last resort.

**Extract from results:**
- `amp` — make, model, channel (e.g. "Marshall JCM800 2203, lead channel")
- `cab` — size, speaker type (e.g. "4×12 with Celestion Greenbacks")
- `drive` — pedal name, usage (boost in front / standalone drive)
- `modulation` — type, placement (pre/post amp)
- `delay` — type (tape/digital/analog), sync, mix level
- `reverb` — type, size, mix level
- `order` — rough signal chain order
- `notes` — EQ, pickup, or technique specifics

**Rules:**
- Prioritise sources that specify album/era — artist rigs change over time.
- If two sources conflict on the amp, note both and prefer the more corroborated one.
- If the exact gear has no HX Stomp model, find the closest `based_on` match in `references/master_blocks.json` and note the substitution.

**Output of this step:** a confirmed signal chain with specific gear names:
```
[wah?] → [drive pedal?] → [amp + cab] → [mod?] → [delay?] → [reverb?]
```

---

## Step 3 — Select Blocks

### Rig Filter (apply first)

Evaluate the user's rig output type and eliminate entire block categories before any other scoring:

| Rig output type | Use Amp+Cab? | Use Preamp? | Use Cab separately? |
|---|---|---|---|
| FRFR / PA / headphones / studio DI | ✅ Yes | ❌ No | Only with Preamp |
| Real amp power section + real cab | ❌ No | ✅ Yes | ❌ No |
| 4-Cable Method (4CM) | ❌ No | ✅ Yes (before FX send) | ❌ No |
| Into clean amp, FX return | ❌ No | ✅ Yes | ❌ No |

### Block Scoring Model

After the rig filter, score remaining candidates. Select the highest scorer; break ties by lower DSP cost.

```
Score = 0

+ 100  if block.based_on exactly matches the identified real-world gear
+  60  if block.based_on partially matches (same brand/era/type)
+  20  if block.subcategory matches the gear type

+  15  if hx_subcategory is "Mono" or "Stereo"   (HX generation — prefer these)
-  10  if hx_subcategory is "Legacy"              (older models)

+  10  if user rig is stereo AND block supports stereo routing
-   5  if user rig is mono   AND block is stereo-only

-  (block.dsp.mono  * 0.1)  for mono routing    (DSP efficiency tiebreaker)
-  (block.dsp.stereo * 0.1) for stereo routing

+   5  if estimated target params fall between 20%–80% of their range
```

**Legacy exception:** prefer Legacy if the target tone is pre-2016, the user asks for vintage character, the Legacy block is the only model of that hardware, or the HX version has a notably different character.

### Stereo vs. Mono

Use a Stereo block only if **all three** are true:
1. User rig has stereo outputs.
2. The effect is inherently stereo (e.g. ping-pong delay, wide chorus, spread reverb).
3. DSP budget allows after all other blocks are accounted for.

Otherwise default to Mono. Never use a Stereo block for a mono rig.

### Amp + Cab Pairing

When using `Preamp` + `Cab` (rather than the combined `Amp+Cab`), match the cab to the amp era:

| Amp type | Typical cab match |
|---|---|
| British (Marshall, Vox) | 4×12 Greenback or Vintage 30 |
| American (Fender, Dumble) | 1×12 or 2×12 Alnico/Jensen |
| High gain (Mesa, EVH, Peavey) | 4×12 Vintage 30 or V30/G12T-75 mix |
| Bass amp | 8×10, 4×10, or 1×15 bass-specific |

### Block Order Rules

1. Wah or fuzz → always first in chain (input impedance).
2. Compression → before drive if enhancing dynamics; after drive if controlling output.
3. Drive blocks → before amp.
4. Amp+Cab or Preamp+Cab → after all pre-amp effects.
5. Modulation, delay, reverb → after amp, in that order.
6. If using 4CM: pre-amp effects → Send block (`@path: 0`) → [amp effects loop] → Return block (`@path: 0`) → post-amp effects.

### Stacking Logic

- High-gain amp + overdrive: prefer a low-gain boost (low drive, high level) over a heavy distortion.
- Clean or slightly breaking up amp: a heavier drive block is appropriate.

---

## Step 4 — Check DSP Budget

Run `scripts/dsp_budget.py` from the skill root directory:

```python
from scripts.dsp_budget import check_budget
result = check_budget(
    block_names=[...],   # list of catalog block names in chain order
    stereo=False,        # or True if user rig is stereo
)
print(result.summary())
```

If `result.passes` is False: drop the lowest-priority block (typically reverb first, then secondary mod/delay). Tell the user what was dropped and why.

If any block has `confidence = "unknown"`: add a note that the DSP estimate for that block is unverified.

---

## Step 5 — Set Parameters

For each block:

1. Start from catalog defaults (`param.default` in `references/master_blocks.json`).
2. Adjust for the researched tone:
   - Drive/gain blocks: transparent boost = low drive + high level.
   - Amp drive: start around 50–60% of max for boosted amps.
   - Amp EQ: start at catalog defaults, adjust mids to match the reference tone.
   - Delay time: if tempo-synced, set `TempoSync1: true` and `SyncSelect1` to the division (6 = quarter note, 9 = dotted eighth, 11 = half note).
   - Delay mix: 20–35% for rhythm/slapback, 40–60% for prominent lead delay.
   - Reverb mix: 15–25% for live tones, 30–50% for ambient/studio.
   - Primary tone blocks: `@enabled: true`. Optional/secondary effects: `@enabled: false`.
3. Convert every parameter value to a normalised float using `scripts/normalize_params.py`:
   ```python
   from scripts.normalize_params import to_normalized
   norm = to_normalized(display_value, param.min, param.max)
   ```
4. Use `param.hlx_key` (NOT the display name) as the key in the `.hlx` output.

---

## Step 6 — Ask Output Format

Before generating anything, ask:

> "Ready to build the preset. Would you like a **Markdown preset map** (readable summary), a **.hlx file** you can load into HX Edit, or **both**?"

Then generate what was requested.

---

## Step 7A — Generate Markdown Preset Map

Format:

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

Follow these steps exactly. Do not invent fields not shown here.

### 7B.1 — Start from the default template

Use this skeleton as the starting point:

```json
{
  "version": 6,
  "schema": "L6Preset",
  "data": {
    "meta": {
      "name": "[PRESET NAME — max 16 chars]",
      "application": "HX Edit"
    },
    "device": 2162694,
    "device_version": 43057152,
    "tone": {
      "dsp1": {},
      "global": {
        "@model": "@global_params",
        "@topology0": "A",
        "@tempo": 120,
        "@guitarinputZ": 0,
        "@current_snapshot": 0,
        "@pedalstate": 0,
        "@cursor_dsp": 0,
        "@cursor_path": 0,
        "@cursor_position": 0,
        "@cursor_group": ""
      },
      "snapshot0": { "@name": "SNAPSHOT 1", "@ledcolor": 0, "@tempo": 120, "@pedalstate": 0 },
      "snapshot1": { "@name": "SNAPSHOT 2", "@ledcolor": 0, "@tempo": 120, "@pedalstate": 0 },
      "snapshot2": { "@name": "SNAPSHOT 3", "@ledcolor": 0, "@tempo": 120, "@pedalstate": 0 },
      "dsp0": {
        "inputA":  { "@model": "HelixStomp_AppDSPFlowInput", "@input": 1, "noiseGate": false, "threshold": -48.0, "decay": 0.5 },
        "inputB":  { "@model": "HelixStomp_AppDSPFlowInput", "@input": 0, "noiseGate": false, "threshold": -48.0, "decay": 0.5 },
        "split":   { "@model": "HD2_AppDSPFlowSplitY", "@enabled": true, "bypass": false, "@position": 0, "BalanceA": 0.5, "BalanceB": 0.5 },
        "join":    { "@model": "HD2_AppDSPFlowJoin", "@enabled": true, "@position": 0, "Level": 0, "A Level": 0, "B Level": 0, "A Pan": 0.5, "B Pan": 0.5, "B Polarity": false },
        "outputA": { "@model": "HelixStomp_AppDSPFlowOutputMain", "@output": 1, "pan": 0.5, "gain": 0 },
        "outputB": { "@model": "HelixStomp_AppDSPFlowOutputSend", "@output": 0, "pan": 0.5, "gain": 0, "Type": true }
      }
    }
  }
}
```

> **Note:** `split` and `join` are always present in the file structure but are functionally unused for topology `"A"` (single serial path). Do not route blocks to Path B unless using a split topology.

### 7B.2 — Write each effect block

For each selected block, add a `blockN` entry to `dsp0` (N = position 0–5):

```json
"block0": {
  "@model":          "[block.symbolicID]",
  "@enabled":        true,
  "@position":       0,
  "@path":           0,
  "[param.hlx_key]": [normalised_float],
  "[param.hlx_key]": [normalised_float]
}
```

**Rules for writing block JSON:**
- `@model` = `block.symbolicID` from `references/master_blocks.json` (e.g. `"HD2_DistKinkyBoost"`).
- `@enabled` = `true` for primary tone blocks; `false` for optional/secondary effects.
- `@position` = slot index 0–5, in signal chain order.
- `@path` = `0` for Path A (single-path presets). Set to `1` for blocks on Path B.
- `@stereo` = include **only** if the block supports stereo (`hx_subcategory = "Stereo"` or `io.routing = "mono_or_stereo"`). Omit entirely otherwise.
- `@no_snapshot_bypass` = omit unless the user specifically asked for a block that snapshots cannot control.
- `@trails` = include on delay/reverb blocks if audio should tail off after bypass. Omit to accept device default (`false`).
- **Parameter keys**: use `param.hlx_key`, NOT the display name. E.g. use `"Ch1Drive"` not `"Ch 1 Drive"`.
- **Parameter values**: normalised floats (0.0–1.0). Use `scripts/normalize_params.py`.
- Include all parameters explicitly rather than relying on device defaults.

### 7B.3 — Configure snapshots (Snapshot mode only)

If `Mode preference = Snapshot mode` or `hybrid`:

For each snapshot (up to 3), add a `"blocks"` object specifying bypass state per block:

```json
"snapshot0": {
  "@name": "Clean",
  "@ledcolor": 0,
  "@tempo": 120,
  "@pedalstate": 0,
  "@valid": true,
  "blocks": {
    "dsp0": {
      "block0": true,
      "block1": false,
      "block2": true,
      "block3": true,
      "block4": false,
      "block5": true
    }
  }
}
```

`true` = block is active (not bypassed). `false` = block is bypassed in this snapshot.

Suggest 3 snapshots as a starting point: Clean / Rhythm / Lead (or equivalent for the tone context).

### 7B.4 — Set global settings

| Field | Value |
|---|---|
| `@tempo` | Reasonable for the genre (120 default; lower for ballads, higher for fast genres). Ask user if unsure. |
| `@guitarinputZ` | `0` (Auto) by default. Set to `6` (230kΩ) if wah or fuzz is first in chain. |
| `@topology0` | `"A"` = single serial path. `"AB"` = dual serial. `"Y"` = Y-split. `"ABCD"` = dual parallel. |

### 7B.5 — Write the file

Save the complete JSON to `[preset_name].hlx` in the user's workspace. Validate the structure against `references/hlx.schema.json`.

---

## Quick Reference

| Need | Where to look |
|---|---|
| Block symbolicID for `@model` | `block.symbolicID` in `references/master_blocks.json` |
| Parameter key for `.hlx` | `param.hlx_key` in `references/master_blocks.json` |
| Convert display value → float | `scripts/normalize_params.py` → `to_normalized(val, min, max)` |
| DSP budget check | `scripts/dsp_budget.py` → `check_budget([names], stereo=False)` |
| Amp+Cab vs. Preamp decision | Step 3 — Rig Filter table |
| Block ranking + scoring | Step 3 — Block Scoring Model |
| Mono vs. stereo decision | Step 3 — Stereo vs. Mono |
| Cab pairing for Preamp | Step 3 — Amp + Cab Pairing table |
| Full `.hlx` schema | `references/hlx.schema.json` |
| Default preset skeleton | Step 7B.1 |

### Critical reminders
- `@model` = `symbolicID` (e.g. `HD2_DistKinkyBoost`), never the catalog `id` field.
- Parameter keys in `.hlx` = `hlx_key` (e.g. `Ch1Drive`), never the display name.
- Parameter values = normalised floats 0.0–1.0, never display units.
- Max 6 blocks per path, max 3 snapshots, max ~95% DSP per chip.
- Amp+Cab blocks are mono-only — for stereo, use Preamp + Cab.
- No Looper or IR blocks in catalog — tell user to configure those manually in HX Edit.
