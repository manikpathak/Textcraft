#!/usr/bin/env python3
"""Entry point runner for Textcraft."""

import sys
import os

# Ensure package directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from textcraft.cli import run_cli

if __name__ == "__main__":
    run_cli()
