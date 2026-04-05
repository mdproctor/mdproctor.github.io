"""
Sparge home directory management.

Reads ~/.sparge/config.json to find where project data lives.
Creates the config with defaults on first use.

Public API
----------
get_projects_dir() -> Path   resolved path to the projects directory
"""
from __future__ import annotations

import json
import os
from pathlib import Path


_SPARGE_HOME = Path.home() / '.sparge'
_SPARGE_CFG  = _SPARGE_HOME / 'config.json'
_DEFAULT_PROJECTS_DIR = Path.home() / 'sparge-projects'


def get_projects_dir() -> Path:
    """
    Return the resolved projects directory path.
    Creates ~/.sparge/config.json with defaults if absent.
    """
    _SPARGE_HOME.mkdir(exist_ok=True)
    if not _SPARGE_CFG.exists():
        _SPARGE_CFG.write_text(json.dumps(
            {'projects_dir': str(_DEFAULT_PROJECTS_DIR)},
            indent=2,
        ))
    try:
        data = json.loads(_SPARGE_CFG.read_text())
        raw = data.get('projects_dir', str(_DEFAULT_PROJECTS_DIR))
    except Exception:
        raw = str(_DEFAULT_PROJECTS_DIR)
    return Path(os.path.expanduser(raw))


def maybe_migrate(old_root: Path, projects_dir: Path) -> bool:
    """
    Copy project data from old_root (blog-migrator/) to projects_dir
    if projects_dir/projects.json does not yet exist.

    Returns True if migration was performed, False otherwise.
    Never deletes the old location.
    """
    import shutil as _shutil

    old_projects_json = old_root / 'projects.json'
    old_projects_dir  = old_root / 'projects'
    new_projects_json = projects_dir / 'projects.json'

    # Skip if: nothing to migrate, or already migrated
    if not old_projects_json.exists() and not old_projects_dir.exists():
        return False
    if new_projects_json.exists():
        return False

    projects_dir.mkdir(parents=True, exist_ok=True)

    # Copy projects.json
    if old_projects_json.exists():
        _shutil.copy2(old_projects_json, new_projects_json)

    # Copy each project subdirectory
    if old_projects_dir.exists():
        for src in old_projects_dir.iterdir():
            if src.is_dir():
                _shutil.copytree(src, projects_dir / src.name, dirs_exist_ok=True)

    print(
        f'[Sparge] Migrated project data from {old_root} → {projects_dir}\n'
        f'         Old location kept intact. You may remove it manually.'
    )
    return True
