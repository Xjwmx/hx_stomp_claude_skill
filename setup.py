#!/usr/bin/env python3
"""
HX Stomp Preset Builder — Package Script
==========================================
Packages the skill as a .zip file ready to upload to Claude.
User preferences are collected by Claude during first use — no setup needed here.

Usage:
    python3 setup.py
"""

import os
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR  = os.path.join(SCRIPT_DIR, "claude skills", "hx_preset_creator")
ZIP_OUTPUT = os.path.join(SCRIPT_DIR, "hx-preset-creator.zip")


def package_skill():
    with zipfile.ZipFile(ZIP_OUTPUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(SKILL_DIR):
            dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d != "__pycache__")
            for filename in sorted(files):
                if filename.startswith(".") or filename.endswith(".pyc"):
                    continue
                file_path = os.path.join(root, filename)
                arcname = os.path.relpath(file_path, os.path.dirname(SKILL_DIR))
                zf.write(file_path, arcname)


def main():
    print("\n  HX Stomp Preset Builder — Package")
    print("  " + "-" * 36)

    package_skill()

    print(f"  ✓ Packaged: {os.path.basename(ZIP_OUTPUT)}")
    print(f"""
  Upload '{os.path.basename(ZIP_OUTPUT)}' to Claude to get started.
  Claude will ask about your rig on first use and save your preferences automatically.
""")


if __name__ == "__main__":
    main()
