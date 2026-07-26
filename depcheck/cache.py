import json
import os
import time
from pathlib import Path
from typing import Any, Optional

DEFAULT_CACHE_DIR = Path(os.environ.get("DEPCHECK_CACHE_DIR", Path.home() / ".cache" / "depcheck"))
DEFAULT_TTL = 86400  # 24 hours in seconds
_CACHE_ENABLED = True


def set_cache_enabled(enabled: bool) -> None:
    global _CACHE_ENABLED
    _CACHE_ENABLED = enabled


def is_cache_enabled() -> bool:
    return _CACHE_ENABLED


def get_cache_dir() -> Path:
    cache_dir_str = os.environ.get("DEPCHECK_CACHE_DIR")
    if cache_dir_str:
        return Path(cache_dir_str)
    return DEFAULT_CACHE_DIR


def _get_cache_path(key: str) -> Path:
    # sanitize key for filename
    safe_key = "".join(c if c.isalnum() or c in "-_." else "_" for c in key)
    return get_cache_dir() / f"{safe_key}.json"


def get_from_cache(key: str) -> Optional[Any]:
    if not _CACHE_ENABLED:
        return None
    path = _get_cache_path(key)
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            entry = json.load(f)
        timestamp = entry.get("timestamp", 0)
        ttl = entry.get("ttl", DEFAULT_TTL)
        if time.time() - timestamp > ttl:
            return None
        return entry.get("data")
    except Exception:
        return None


def save_to_cache(key: str, data: Any, ttl: int = DEFAULT_TTL) -> None:
    if not _CACHE_ENABLED:
        return
    try:
        path = _get_cache_path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": time.time(),
            "ttl": ttl,
            "data": data,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(entry, f)
    except Exception:
        # Never crash on cache write failure
        pass


def clear_cache() -> None:
    try:
        cache_dir = get_cache_dir()
        if cache_dir.exists():
            for f in cache_dir.glob("*.json"):
                try:
                    f.unlink()
                except OSError:
                    pass
    except Exception:
        pass
