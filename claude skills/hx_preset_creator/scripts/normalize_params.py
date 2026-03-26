"""
normalize_params.py
-------------------
Converts HX Stomp parameter values between display units (as stored in
master_blocks.json) and normalised floats (0.0–1.0 as required in .hlx files).

Usage
-----
    from normalize_params import to_normalized, to_display

    # Display → normalised (for writing .hlx files)
    norm = to_normalized(display_value=5.0, param_min=0.0, param_max=10.0)
    # → 0.5

    # Normalised → display (for reading .hlx files back to human values)
    display = to_display(normalised=0.5, param_min=0.0, param_max=10.0)
    # → 5.0

Notes
-----
- param_min and param_max come from the `parameters[]` list in master_blocks.json.
- Some parameters use non-linear (log/exponential) scaling on the device. The
  HelixControls.json (available from your HX Edit installation) carries
  `displayType` and `valueType` metadata that describes these cases. This
  utility handles only linear scaling; extend it with HelixControls lookups
  for parameters where linear approximation is insufficient.
- Toggle and enum parameters do not use this conversion — their .hlx values
  are integers indexing into the `options` list.
"""

from __future__ import annotations
import json
import os
from typing import Union

Number = Union[int, float]

MASTER_JSON_PATH = os.path.join(
    os.path.dirname(__file__), "..", "references", "master_blocks.json"
)


def to_normalized(display_value: Number, param_min: Number, param_max: Number) -> float:
    """Convert a display-unit value to a normalised 0.0–1.0 float.

    Args:
        display_value: The value in display units (e.g. 5.0 on a 0–10 knob).
        param_min: The parameter's minimum display value.
        param_max: The parameter's maximum display value.

    Returns:
        A float in the range [0.0, 1.0], clamped to that range.

    Raises:
        ValueError: If param_min == param_max (zero-range parameter).
    """
    if param_min == param_max:
        raise ValueError(
            f"param_min ({param_min}) == param_max ({param_max}): "
            "cannot normalise a zero-range parameter"
        )
    normalised = (display_value - param_min) / (param_max - param_min)
    return max(0.0, min(1.0, normalised))


def to_display(normalised: float, param_min: Number, param_max: Number) -> float:
    """Convert a normalised 0.0–1.0 float back to display units.

    Args:
        normalised: A float in [0.0, 1.0].
        param_min: The parameter's minimum display value.
        param_max: The parameter's maximum display value.

    Returns:
        The value in display units.
    """
    return param_min + normalised * (param_max - param_min)


def normalize_block_params(
    block_name: str,
    display_values: dict[str, Number],
    master_json_path: str = MASTER_JSON_PATH,
) -> dict[str, float]:
    """Normalise a dict of {param_name: display_value} for a named block.

    Looks up the block's parameter min/max from master_blocks.json and returns
    a dict of {param_name: normalised_float} ready to embed in a .hlx file.

    Args:
        block_name: The block's `name` field as it appears in master_blocks.json.
        display_values: Dict mapping parameter names to display-unit values.
        master_json_path: Path to master_blocks.json (defaults to project root).

    Returns:
        Dict of {param_name: normalised_float}.

    Raises:
        KeyError: If the block or parameter is not found in master_blocks.json.
    """
    with open(master_json_path) as f:
        catalog = json.load(f)

    # Find the block
    block = next(
        (b for b in catalog["blocks"] if b["name"] == block_name), None
    )
    if block is None:
        raise KeyError(f"Block '{block_name}' not found in catalog")

    # Build param name → {min, max} index
    param_map = {
        p["name"]: p for p in block.get("parameters", [])
        if p.get("type") == "continuous"
    }

    result = {}
    for param_name, display_val in display_values.items():
        if param_name not in param_map:
            raise KeyError(
                f"Parameter '{param_name}' not found on block '{block_name}'"
            )
        p = param_map[param_name]
        result[param_name] = to_normalized(display_val, p["min"], p["max"])

    return result


if __name__ == "__main__":
    # Quick self-test
    assert to_normalized(5.0, 0.0, 10.0) == 0.5
    assert to_normalized(0.0, 0.0, 10.0) == 0.0
    assert to_normalized(10.0, 0.0, 10.0) == 1.0
    assert to_normalized(-5.0, 0.0, 10.0) == 0.0   # clamped
    assert to_normalized(15.0, 0.0, 10.0) == 1.0   # clamped
    assert abs(to_display(0.5, 0.0, 10.0) - 5.0) < 1e-9
    print("normalize_params: all assertions passed.")
