# .hlx File Generation Reference

Follow these steps exactly. Do not invent fields not shown here.

---

## 7B.1 — Start from the default template

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

---

## 7B.2 — Write each effect block

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

---

## 7B.3 — Configure snapshots (Snapshot mode only)

If `control_mode = snapshot` or `hybrid`:

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

---

## 7B.4 — Set global settings

| Field | Value |
|---|---|
| `@tempo` | Reasonable for the genre (120 default; lower for ballads, higher for fast genres). Ask user if unsure. |
| `@guitarinputZ` | `0` (Auto) by default. Set to `6` (230kΩ) if wah or fuzz is first in chain. |
| `@topology0` | `"A"` = single serial path. `"AB"` = dual serial. `"Y"` = Y-split. `"ABCD"` = dual parallel. |

---

## 7B.5 — Write the file

Save the complete JSON to `[preset_name].hlx` in the user's workspace. Validate the structure against `references/hlx.schema.json`.
