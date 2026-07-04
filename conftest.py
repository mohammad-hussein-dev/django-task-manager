"""
Pytest configuration file.

This file is automatically loaded by pytest and adds the `src/` directory
to Python's module search path, ensuring that the `apps` package and other
project modules can be imported correctly during testing.
"""

import sys
from pathlib import Path

# Get the absolute path to the project root.
project_root = Path(__file__).parent

# Add the `src/` directory to Python's module search path.
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
