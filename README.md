# HX Stomp Preset Builder

A Claude skill that generates complete, ready-to-load Line 6 HX Stomp presets from a natural-language tone description.

> **Example:** *"Build me a bass preset that sounds like Freewill by Rush."*

Claude researches the real-world gear behind that sound, maps it to the blocks available on your HX Stomp, checks the DSP budget, and outputs a `.hlx` file you can load directly in HX Edit — or a readable Markdown preset map, or both.

---

## How It Works

Every request runs through a seven-step pipeline:

```
Step 0  Load User Preferences    → Read your saved rig config (or run init on first use)
Step 1  Parse Intent             → Extract instrument, genre, reference artist/song, constraints
Step 2  Research Tone            → Look up real-world amp, cab, and pedal chain
Step 3  Select Blocks            → Score and select HX Stomp blocks from the catalog
Step 4  Check DSP Budget         → Verify all blocks fit within the 95% DSP ceiling
Step 5  Set Parameters           → Dial in parameter values based on the reference tone
Step 6  Ask Output Format        → Markdown map, .hlx file, or both
Step 7  Generate Output          → Write the file(s)
```

Your rig configuration is captured on first use — instrument, signal chain type, output routing, control mode, tone profile — and saved inside the skill. Every subsequent preset is built around your setup.

---

## Prerequisites

- **Claude account** — [claude.ai](https://claude.ai) (free tier works; Pro recommended for longer sessions)
- **Line 6 HX Stomp** running firmware **3.80** (the block catalog targets this version)
- **HX Edit** — to transfer generated `.hlx` files to the device
- **Python 3.8+** — only needed if you want to run the DSP/parameter scripts locally

---

## Installation — Claude App (Recommended)

Skills are managed under **Customization** in the Claude app sidebar.

**1. Download or build the skill package**

Either grab the latest `hx-preset-creator.zip` from the [Releases](../../releases) page, or build it yourself:

```bash
git clone https://github.com/yourusername/hxstomp_dsp_automation.git
cd hxstomp_dsp_automation
python3 setup.py
# → produces hx-preset-creator.zip
```

**2. Upload to Claude**

1. Open [claude.ai](https://claude.ai) and click **Customization** in the left sidebar
2. Select **Skills** and click **Add skill**
3. Upload `hx-preset-creator.zip`
4. Claude will confirm the skill is active

**3. Use it**

In any Claude conversation:

```
/hx-preset-creator Build me a Gilmour lead tone
```

---

## Installation — Claude Code (Advanced)

If you use [Claude Code](https://claude.ai/code), you can install the skill directly into your skills directory so it's available in every Claude Code session.

```bash
git clone https://github.com/yourusername/hxstomp_dsp_automation.git
cd hxstomp_dsp_automation

# Copy skill to your global Claude Code skills directory
cp -r "claude skills/hx_preset_creator" ~/.claude/skills/hx-preset-creator
```

Verify it's visible in a Claude Code session:

```
/skills
```

`hx-preset-creator` should appear in the list.

---

## First Use — Rig Setup

The first time you invoke the skill, Claude runs a one-time setup interview before building any presets. You won't be asked again.

**Round 1 — Your instrument** (make, model, pickup type, output level)

**Round 2 — Your rig connection** — choose from:
- Direct to FRFR speaker, PA, or audio interface
- Into the front of a guitar/bass amp
- 4-Cable Method (integrated into amp effects loop)
- Amp effects loop only, or into the effects return
- External preamp/amp sim in the HX Stomp Send/Return

Includes follow-up questions about any devices in the effects loop and any external pedals before or after the HX Stomp.

**Round 3 — Output and control** (mono/stereo, Stomp/Snapshot/Hybrid mode, expression pedal)

**Round 4 — Tone profile** (genres, tone character, always-include/always-exclude blocks)

Once confirmed, your answers are written to `user_preferences.md` inside the skill and applied to every preset from then on.

---

## Using the Skill

```
/hx-preset-creator Build a Gilmour Comfortably Numb lead tone
/hx-preset-creator I want a JCM800 with a Tube Screamer in front
/hx-preset-creator Bass preset for reggaeton — modern, punchy, hi-fi
/hx-preset-creator 70s arena rock rhythm guitar, warm and crunchy
```

Claude will confirm the output format you want (Markdown map, `.hlx` file, or both) and generate it. `.hlx` files can be loaded directly into HX Edit via **File → Import Preset**.

To update your saved rig at any time:

```
/hx-preset-creator Update my rig — I switched to a FRFR setup
```

---

## Repository Structure

```
hxstomp_dsp_automation/
│
├── claude skills/
│   └── hx_preset_creator/             ← The skill (self-contained)
│       ├── SKILL.md                   ← Entry point: pipeline logic and instructions
│       ├── user_preferences.md        ← Rig config (populated by Claude on first use)
│       ├── references/
│       │   ├── master_blocks.json     ← All 609 HX Stomp blocks (merged catalog)
│       │   ├── amp_cab.json           ┐
│       │   ├── distortion.json        │ Per-category block files (14 total)
│       │   ├── ... (one per category) ┘
│       │   ├── hlx.schema.json        ← JSON Schema for .hlx preset files
│       │   ├── catalog.schema.json    ← JSON Schema for catalog files
│       │   ├── hx_edit_pilots_guide.pdf
│       │   └── hx_stomp_cheat_sheet_en.pdf
│       └── scripts/
│           ├── dsp_budget.py          ← DSP budget calculator
│           └── normalize_params.py    ← Display ↔ normalised float converter
│
├── project_references/                ← Source-of-record data for development
│   ├── master_blocks.json
│   ├── catalog.schema
│   ├── hlx.schema.json
│   └── hx_files/                      ← Raw files extracted from HX Edit
│       ├── default_preset_hxs.hlx     ← Empty HX Stomp preset template
│       ├── HelixControls.json         ← Parameter display scaling definitions
│       └── *.models                   ← Raw Line 6 model definitions per category
│
├── converstation_examples/            ← Annotated example sessions (development reference)
├── setup.py                           ← Packages the skill as hx-preset-creator.zip
└── README.md
```

**Why two copies of the catalog?**
The skill folder (`claude skills/hx_preset_creator/references/`) is self-contained — Claude reads only from within the skill at runtime. `project_references/` is the development source of record. When updating block data, edit there first, then sync to the skill folder.

---

## The Block Catalog

### Coverage

609 blocks across 14 categories, targeting firmware 3.80:

`amp_cab` · `preamp` · `cab` · `distortion` · `dynamics` · `eq` · `filter` · `modulation` · `delay` · `reverb` · `pitch_synth` · `volume_pan` · `wah` · `utility`

**Not in the catalog:** Looper and IR loader blocks — configure these manually in HX Edit after loading the preset.

### Key fields per block

| Field | Description |
|---|---|
| `id` | Unique snake_case identifier (`dist_kinky_boost`) |
| `name` | Display name as shown on the device |
| `symbolicID` | Internal Line 6 string used in `.hlx` files (`HD2_DistKinkyBoost`) |
| `category` | Top-level category (Distortion, Amp+Cab, etc.) |
| `hx_subcategory` | Block generation: `Mono`, `Stereo`, or `Legacy` |
| `subcategory` | Functional subcategory (Boost, Fuzz, Phaser, etc.) |
| `based_on` | Real-world hardware modelled (`null` for Line 6 Originals) |
| `description` | Character and use-case summary |
| `dsp.mono` / `dsp.stereo` | DSP load as a percentage; `null` if routing mode not supported |
| `dsp.confidence` | `measured` / `estimated` / `unknown` |
| `parameters[]` | Full parameter list: name, `hlx_key`, unit, min/max, default, type |

> When writing `.hlx` files, always use `symbolicID` for `@model` and `hlx_key` for parameter keys.

### Updating the catalog

1. Edit the relevant category file under `project_references/` (e.g. `distortion.json`)
2. Validate against `project_references/catalog.schema` (JSON Schema Draft 2020-12)
3. Merge all category files into `project_references/master_blocks.json`
4. Copy updated files into `claude skills/hx_preset_creator/references/`
5. Rebuild the zip with `python3 setup.py`

---

## HX Stomp Hardware Constraints

The skill enforces these automatically — useful to know when editing presets manually.

### DSP budget

Two DSP chips, each with a ~100% ceiling. The skill targets **95% per chip maximum**, leaving a margin for firmware overhead. Stereo blocks cost more DSP than their mono equivalents. DSP values in the catalog are community-measured estimates.

### Block slots

6 block slots per signal path (not counting input, output, split, and join nodes). Dual-path topology allows up to 8 blocks total.

### Signal path topologies

| Value | Routing |
|---|---|
| `"A"` | Single serial path (most common) |
| `"AB"` | Dual serial paths |
| `"Y"` | Y-split (signal splits and rejoins) |
| `"ABCD"` | Dual parallel paths |

### 4-Cable Method (4CM)

When your rig is configured as `4cm`, the skill includes Send/Return blocks at the correct position — pre-amp effects before the Send, post-amp effects after the Return.

### Input impedance

The first block in the chain sets `@guitarinputZ`. Wah and fuzz blocks should always be first. The skill handles this automatically.

---

## Scripts

Both scripts are used internally by the skill and can also be run standalone.

### `dsp_budget.py`

```python
from scripts.dsp_budget import check_budget

result = check_budget(
    block_names=["Kinky Boost", "A30 Fawn Nrm", "Adriatic Delay", "63 Spring"],
    stereo=False,
)
print(result.summary())
# DSP Budget: 47.3% / 95% ceiling ✅ OK
```

### `normalize_params.py`

All parameter values in `.hlx` files are normalised floats (0.0–1.0), not display units.

```python
from scripts.normalize_params import to_normalized, to_display

norm    = to_normalized(display_value=5.0, param_min=0.0, param_max=10.0)  # → 0.5
display = to_display(normalised=0.5, param_min=0.0, param_max=10.0)        # → 5.0
```

`normalize_block_params()` converts a full `{param_name: display_value}` dict for a named block, looking up min/max from `master_blocks.json` automatically.

> Note: these scripts handle linear parameter scaling only. Some parameters use non-linear scaling on the device — `HelixControls.json` in `project_references/hx_files/` has `displayType` metadata for those cases.

---

## Extending the Skill

**Change pipeline behaviour** — edit `claude skills/hx_preset_creator/SKILL.md`. The pipeline steps, block scoring logic, ordering rules, parameter defaults, and output templates are all written in plain language there.

**Add or correct block data** — edit the category JSON files in `project_references/`, validate against the schema, sync to the skill folder, and rebuild the zip.

**Update for a new firmware version** — check Line 6's release notes for added or changed models, update the affected category files, and note the firmware version in the catalog entries.

---

## Contributing

Pull requests are welcome. Useful contributions:

- Correcting or adding DSP values (especially `measured` confidence data)
- Adding missing parameter definitions to existing blocks
- Updating block descriptions or `based_on` references
- Bug reports for `.hlx` files that don't load correctly in HX Edit

Please validate catalog changes against `catalog.schema.json` before submitting.

---

## License

UNLICENSE — see `LICENSE` for details.

Line 6, HX Stomp, and HX Edit are trademarks of Line 6, Inc. This project is not affiliated with or endorsed by Line 6.
