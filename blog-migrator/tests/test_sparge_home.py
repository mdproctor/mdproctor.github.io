"""Unit tests for sparge_home.py — ~/.sparge config reading."""
import json
import sys
from pathlib import Path

import pytest

MIGRATOR = Path(__file__).parent.parent
sys.path.insert(0, str(MIGRATOR / 'scripts'))


def test_default_projects_dir_when_no_config(tmp_path, monkeypatch):
    """When ~/.sparge/config.json absent, defaults to ~/sparge-projects."""
    monkeypatch.setenv('HOME', str(tmp_path))
    import importlib, sparge_home
    importlib.reload(sparge_home)
    result = sparge_home.get_projects_dir()
    assert result == tmp_path / 'sparge-projects'


def test_reads_projects_dir_from_config(tmp_path, monkeypatch):
    """When config exists, returns configured path."""
    monkeypatch.setenv('HOME', str(tmp_path))
    custom = tmp_path / 'my-projects'
    sparge_cfg = tmp_path / '.sparge'
    sparge_cfg.mkdir()
    (sparge_cfg / 'config.json').write_text(
        json.dumps({'projects_dir': str(custom)})
    )
    import importlib, sparge_home
    importlib.reload(sparge_home)
    result = sparge_home.get_projects_dir()
    assert result == custom


def test_tilde_expansion_in_projects_dir(tmp_path, monkeypatch):
    """~/path in config.json is expanded relative to HOME."""
    monkeypatch.setenv('HOME', str(tmp_path))
    sparge_cfg = tmp_path / '.sparge'
    sparge_cfg.mkdir()
    (sparge_cfg / 'config.json').write_text(
        json.dumps({'projects_dir': '~/custom-projects'})
    )
    import importlib, sparge_home
    importlib.reload(sparge_home)
    result = sparge_home.get_projects_dir()
    assert result == tmp_path / 'custom-projects'


def test_creates_sparge_dir_and_default_config(tmp_path, monkeypatch):
    """First call creates ~/.sparge/config.json with defaults."""
    monkeypatch.setenv('HOME', str(tmp_path))
    import importlib, sparge_home
    importlib.reload(sparge_home)
    sparge_home.get_projects_dir()
    cfg_path = tmp_path / '.sparge' / 'config.json'
    assert cfg_path.exists()
    data = json.loads(cfg_path.read_text())
    assert 'projects_dir' in data


import shutil


def test_migration_copies_projects_json(tmp_path, monkeypatch):
    """projects.json is copied from old location to new on first run."""
    monkeypatch.setenv('HOME', str(tmp_path))
    old_projects = tmp_path / 'blog-migrator' / 'projects'
    old_projects.mkdir(parents=True)
    (old_projects.parent / 'projects.json').write_text(
        json.dumps([{'id': 'test-proj', 'name': 'Test'}])
    )

    import importlib, sparge_home
    importlib.reload(sparge_home)
    new_dir = tmp_path / 'sparge-projects'
    sparge_home.maybe_migrate(
        old_root=old_projects.parent,
        projects_dir=new_dir,
    )

    assert (new_dir / 'projects.json').exists()
    data = json.loads((new_dir / 'projects.json').read_text())
    assert data[0]['id'] == 'test-proj'


def test_migration_copies_project_dirs(tmp_path, monkeypatch):
    """Project subdirectories are copied with their contents."""
    monkeypatch.setenv('HOME', str(tmp_path))
    old_root = tmp_path / 'blog-migrator'
    old_proj = old_root / 'projects' / 'my-blog'
    old_proj.mkdir(parents=True)
    (old_proj / 'config.json').write_text('{"project_name": "My Blog"}')
    (old_proj / 'state.json').write_text('{}')
    (old_root / 'projects.json').write_text(
        json.dumps([{'id': 'my-blog', 'name': 'My Blog'}])
    )

    new_dir = tmp_path / 'sparge-projects'
    import importlib, sparge_home
    importlib.reload(sparge_home)
    sparge_home.maybe_migrate(old_root=old_root, projects_dir=new_dir)

    assert (new_dir / 'my-blog' / 'config.json').exists()
    assert (new_dir / 'my-blog' / 'state.json').exists()


def test_migration_skipped_if_already_done(tmp_path, monkeypatch):
    """Migration does not overwrite if new projects.json already exists."""
    monkeypatch.setenv('HOME', str(tmp_path))
    old_root = tmp_path / 'blog-migrator'
    (old_root / 'projects').mkdir(parents=True)
    (old_root / 'projects.json').write_text(json.dumps([{'id': 'old'}]))

    new_dir = tmp_path / 'sparge-projects'
    new_dir.mkdir()
    (new_dir / 'projects.json').write_text(json.dumps([{'id': 'new'}]))

    import importlib, sparge_home
    importlib.reload(sparge_home)
    sparge_home.maybe_migrate(old_root=old_root, projects_dir=new_dir)

    data = json.loads((new_dir / 'projects.json').read_text())
    assert data[0]['id'] == 'new'  # not overwritten


def test_migration_no_op_when_old_dir_absent(tmp_path, monkeypatch):
    """maybe_migrate is a no-op when old location doesn't exist."""
    monkeypatch.setenv('HOME', str(tmp_path))
    new_dir = tmp_path / 'sparge-projects'
    import importlib, sparge_home
    importlib.reload(sparge_home)
    sparge_home.maybe_migrate(
        old_root=tmp_path / 'nonexistent',
        projects_dir=new_dir,
    )
    assert not new_dir.exists()
