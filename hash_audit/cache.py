from __future__ import annotations
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

DEFAULT_CACHE_DIR = Path(os.getenv("HASH_AUDIT_CACHE_DIR", Path.home() / ".cache" / "hash_audit"))
DEFAULT_CACHE_DIR.mkdir(parents=True, exist_ok=True)

@dataclass
class CacheKey:
    algo: str
    salt_mode: str
    salt_len: int
    seconds: float

def _key_to_filename(key: CacheKey) -> Path:
    safe = f"{key.algo}_{key.salt_mode}_{key.salt_len}_{int(key.seconds*1000)}.json"
    return DEFAULT_CACHE_DIR / safe

def load_cached_benchmark(key: CacheKey) -> Optional[dict[str, Any]]:
    path = _key_to_filename(key)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def save_cached_benchmark(key: CacheKey, payload: dict[str, Any]) -> None:
    path = _key_to_filename(key)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
