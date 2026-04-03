"""Load and expose config.json. All paths resolved to absolute."""
import json
from pathlib import Path

_CFG_PATH = Path(__file__).parent.parent / 'config.json'


def load() -> dict:
    raw = json.loads(_CFG_PATH.read_text())
    root = Path(raw['serve_root'])
    # Resolve relative paths against serve_root
    raw['_root'] = root
    raw['_posts_dir'] = root / raw['source']['posts_dir']
    raw['_assets_dir'] = root / raw['source']['assets_dir']
    raw['_md_dir']     = root / raw['output']['md_dir']
    return raw


def save(cfg: dict):
    # Strip internal _keys before writing
    clean = {k: v for k, v in cfg.items() if not k.startswith('_')}
    _CFG_PATH.write_text(json.dumps(clean, indent=2))


# Module-level singleton loaded once on import
cfg = load()
