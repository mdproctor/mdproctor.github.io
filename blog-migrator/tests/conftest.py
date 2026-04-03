"""
Shared fixtures and path setup for blog-migrator tests.
"""
import sys
from pathlib import Path

# Make blog-migrator/scripts/ importable as 'scripts.*'
MIGRATOR_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(MIGRATOR_ROOT / 'scripts'))

# Also make the parent scripts/ available (md_validator, convert_post, etc.)
REPO_ROOT = MIGRATOR_ROOT.parent
sys.path.insert(0, str(REPO_ROOT / 'scripts'))
