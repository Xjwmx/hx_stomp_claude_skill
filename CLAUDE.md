# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

A Claude AI skill that generates Line 6 HX Stomp guitar presets from natural-language tone descriptions. Users describe a tone (e.g., "Comfortably Numb Gilmour lead") and the skill outputs a `.hlx` file (loadable into HX Edit) and/or a Markdown preset map. Targets HX Stomp firmware 3.80.

## Build

```bash
# Package the skill into hx-preset-creator.zip for upload to Claude.ai
python3 setup.py
```

The zip is built from `claude skills/hx_preset_creator/` — the only artifact that matters.

## Running the Scripts

Both scripts have self-tests in their `__main__` blocks:

```bash
python3 "claude skills/hx_preset_creator/scripts/dsp_budget.py"
python3 "claude skills/hx_preset_creator/scripts/normalize_params.py"
```

No external dependencies — pure stdlib (`json`, `os`).

## Architecture

The skill runs entirely inside Claude's context window when invoked. There is no server, no runtime execution environment, and no state between conversations except what is written to `user_preferences.md`.

### Entry Point

`claude skills/hx_preset_creator/SKILL.md` — Claude reads this on every invocation. It defines the entire 7-step pipeline, block scoring model, `.hlx` file template, and all generation rules. This is the most important file in the project.

### 7-Step Pipeline

1. **Load Preferences** — Read `user_preferences.md` or run first-time setup interview
2. **Parse Intent** — Extract instrument, genre, reference artist/song, constraints
3. **Research Tone** — Look up real-world gear from web sources
4. **Select Blocks** — Score and rank from the 609-block catalog using a weighted model
5. **Check DSP Budget** — Verify blocks fit within 95% DSP ceiling (uses `dsp_budget.py`)
6. **Set Parameters** — Convert display values to normalized floats (uses `normalize_params.py`)
7. **Generate Output** — Write `.hlx` JSON and/or Markdown preset map

### Block Catalog

`claude skills/hx_preset_creator/references/master_blocks.json` — 609 blocks, ~3MB. Each block has:
- `symbolicID` — Line 6 internal ID, **always use this in `.hlx` files** (not the display name)
- `dsp.mono` / `dsp.stereo` — percentage load per chip
- `parameters[].hlx_key` — key used in `.hlx` files (not the display name)
- `parameters[].min`, `max`, `default` — raw range for normalization

Category-specific files (`amp_cab.json`, `distortion.json`, etc.) are merged into `master_blocks.json` for runtime — only `master_blocks.json` is read by the running skill.

### Scoring Model

Blocks are ranked by real-world gear match, subcategory alignment, rig compatibility (FRFR vs. real amp), DSP efficiency, and parameter range centering. Rig filtering runs first: Amp+Cab blocks only for FRFR/PA/headphone rigs; Preamp blocks for real amp outputs.

### Parameter Normalization

HX Stomp `.hlx` files store all parameter values as normalized floats (0.0–1.0). `normalize_params.py` converts between display values (e.g., `500 Hz`, `-3 dB`) and normalized floats. Claude calls this logic during Step 6.

### User Preferences

`claude skills/hx_preset_creator/user_preferences.md` — Template populated during first-time setup. Records signal chain type (FRFR, 4-Cable Method, etc.), amp details, output mode, and tone profile. Persists across conversations and drives rig-aware block filtering.

### Schemas

- `references/catalog.schema.json` — validates block catalog structure (JSON Schema Draft 2020-12)
- `references/hlx.schema.json` — validates `.hlx` preset file structure

### project_references/

Development source-of-truth (not part of the packaged skill):
- `CORE.hlx` — empty HX Stomp preset template
- `HX Files/` — raw Line 6 files from HX Edit (gitignored): `HelixControls.json` (parameter metadata), `.models` files (raw block definitions per category)

## Key Constraints the Skill Enforces

- **DSP**: 2 chips, 95% ceiling each; stereo blocks cost more than mono
- **Block slots**: 6 per signal path
- **Topologies**: `A` (serial), `AB` (dual serial), `Y` (Y-split), `ABCD` (dual parallel)
- **Input impedance**: Wah/fuzz must be first in chain (`@guitarinputZ: 6`)
- **4-Cable Method**: Send/Return inserted before amp's effects return
