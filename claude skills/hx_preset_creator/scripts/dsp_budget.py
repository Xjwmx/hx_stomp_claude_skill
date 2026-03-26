"""
dsp_budget.py
-------------
DSP budget calculator for HX Stomp presets.

Given a list of block names and a stereo flag, returns the total DSP
percentage per chip and whether the preset fits within the ~95% ceiling.

Usage
-----
    from dsp_budget import check_budget, BudgetResult

    result = check_budget(
        block_names=["Kinky Boost", "A30 Fawn Nrm", "Adriatic Delay", "63 Spring"],
        stereo=False,
    )
    print(result.total_dsp)     # e.g. 47.3
    print(result.passes)        # True / False
    print(result.warnings)      # list of warning strings

DSP Ceiling
-----------
The HX Stomp has two DSP chips (DSP 0 and DSP 1). In practice, the preset
builder uses DSP 0 as the primary path. The ceiling is ~95% per chip; a 5%
safety margin is reserved for firmware overhead.

For blocks with `dsp.confidence = "unknown"`, the calculator uses a
conservative 15% estimate and flags it as a warning.
"""

from __future__ import annotations
import json
import os
from dataclasses import dataclass, field
from typing import Optional

MASTER_JSON_PATH = os.path.join(
    os.path.dirname(__file__), "..", "references", "master_blocks.json"
)

DSP_CEILING = 95.0          # % per chip
UNKNOWN_DSP_ESTIMATE = 15.0  # conservative fallback for blocks with unknown DSP


@dataclass
class BlockDSP:
    name: str
    symbolicID: str
    dsp_value: float          # the value used in the budget (mono or stereo)
    confidence: str           # "measured" | "estimated" | "unknown"
    was_estimated: bool = False  # True if fallback estimate was applied


@dataclass
class BudgetResult:
    blocks: list[BlockDSP]
    total_dsp: float
    ceiling: float
    passes: bool
    warnings: list[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = [
            f"DSP Budget: {self.total_dsp:.1f}% / {self.ceiling:.0f}% ceiling "
            f"({'✅ OK' if self.passes else '❌ OVER BUDGET'})"
        ]
        for b in self.blocks:
            est_flag = " [estimated]" if b.was_estimated else ""
            lines.append(f"  {b.dsp_value:5.1f}%  {b.name}{est_flag}")
        if self.warnings:
            lines.append("\nWarnings:")
            for w in self.warnings:
                lines.append(f"  ⚠️  {w}")
        return "\n".join(lines)


def check_budget(
    block_names: list[str],
    stereo: bool = False,
    master_json_path: str = MASTER_JSON_PATH,
    ceiling: float = DSP_CEILING,
) -> BudgetResult:
    """Calculate the DSP budget for a list of block names.

    Args:
        block_names: List of block `name` values as they appear in master_blocks.json.
        stereo: If True, use `dsp.stereo` values; otherwise use `dsp.mono`.
        master_json_path: Path to master_blocks.json.
        ceiling: DSP ceiling percentage (default 95%).

    Returns:
        A BudgetResult with totals, pass/fail, and per-block breakdown.

    Raises:
        KeyError: If a block name is not found in the catalog.
    """
    with open(master_json_path) as f:
        catalog = json.load(f)

    catalog_by_name = {b["name"]: b for b in catalog["blocks"]}
    dsp_mode = "stereo" if stereo else "mono"

    blocks: list[BlockDSP] = []
    warnings: list[str] = []
    total = 0.0

    for name in block_names:
        if name not in catalog_by_name:
            raise KeyError(f"Block '{name}' not found in catalog")

        block = catalog_by_name[name]
        dsp_section = block.get("dsp", {})
        confidence = dsp_section.get("confidence", "unknown")
        raw_value: Optional[float] = dsp_section.get(dsp_mode)

        was_estimated = False

        if raw_value is None:
            # Fall back: try the other mode if the requested mode isn't available
            other_mode = "mono" if dsp_mode == "stereo" else "stereo"
            fallback: Optional[float] = dsp_section.get(other_mode)
            if fallback is not None:
                raw_value = fallback
                warnings.append(
                    f"'{name}': no {dsp_mode} DSP value; using {other_mode} "
                    f"value ({fallback:.1f}%) as approximation."
                )
            else:
                raw_value = UNKNOWN_DSP_ESTIMATE
                was_estimated = True
                warnings.append(
                    f"'{name}': DSP cost unknown; using conservative estimate "
                    f"of {UNKNOWN_DSP_ESTIMATE:.0f}%."
                )

        if confidence == "unknown" and not was_estimated:
            warnings.append(
                f"'{name}': DSP confidence is 'unknown' — actual cost may differ."
            )

        blocks.append(BlockDSP(
            name=name,
            symbolicID=block.get("symbolicID", ""),
            dsp_value=raw_value,
            confidence=confidence,
            was_estimated=was_estimated,
        ))
        total += raw_value

    passes = total <= ceiling

    if not passes:
        warnings.append(
            f"Total DSP ({total:.1f}%) exceeds the {ceiling:.0f}% ceiling by "
            f"{total - ceiling:.1f}%. Remove or swap a block."
        )
    elif total > ceiling * 0.9:
        warnings.append(
            f"Total DSP ({total:.1f}%) is above 90% of ceiling — "
            "little headroom remains for additional effects."
        )

    return BudgetResult(
        blocks=blocks,
        total_dsp=round(total, 2),
        ceiling=ceiling,
        passes=passes,
        warnings=warnings,
    )


if __name__ == "__main__":
    # Quick self-test using real catalog data
    result = check_budget(
        block_names=["Kinky Boost", "Adriatic Delay"],
        stereo=False,
    )
    print(result.summary())
    assert result.passes, "Expected budget to pass for a two-block preset"
    print("\ndsp_budget: self-test passed.")
