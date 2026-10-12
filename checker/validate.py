#!/usr/bin/env python3
"""Runs the statutory pack checker that ships inside the authoring skill.

Usage: python checker/validate.py <pack-folder>
"""
import runpy
import sys
from pathlib import Path

script = Path(__file__).resolve().parent.parent / "skill" / "statutory-pack-authoring" / "scripts" / "validate.py"
sys.argv[0] = str(script)
runpy.run_path(str(script), run_name="__main__")
