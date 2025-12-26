from __future__ import annotations # Assuming annotations are important key for this file
import time
import math
import secrets
from typing import Dict, Any

from .hashing import HashSpec, hash_password
from .cache import CacheKey, load_cached_benchmark, save_cached_benchmark

def _random_password(n: int = 12) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+"
    return "".join(secrets.choice(alphabet) for _ in range(n))

def _estimate_space(charset_size: int, length: int) -> int:
    return int(charset_size ** length)

def _format_seconds(s: float) -> str:
    if s < 60:
        return f"{s:.2f}s"
    if s < 3600:
        return f"{s/60:.2f}m"
    if s < 86400:
        return f"{s/3600:.2f}h"
    return f"{s/86400:.2f}d"

def run_benchmark(algo: str, seconds: float, salt_mode: str = "none", salt_len: int = 0, use_cache: bool = True) -> Dict[str, Any]:
    key = CacheKey(algo=algo, salt_mode=salt_mode, salt_len=salt_len, seconds=seconds)
    if use_cache:
        cached = load_cached_benchmark(key)
        if cached:
            cached["cached"] = True
            return cached

    salt = ("S" * salt_len) if salt_len > 0 else ""
    spec = HashSpec(algo=algo, salt_mode=salt_mode, salt=salt)

    # Warmup
    hash_password(_random_password(), spec)

    start = time.perf_counter()
    end = start + seconds
    count = 0
    while time.perf_counter() < end:
        hash_password(_random_password(), spec)
        count += 1

    elapsed = time.perf_counter() - start
    hps = count / elapsed if elapsed > 0 else 0.0

    policies = [
        {"label": "lowercase(26) length=8", "charset": 26, "length": 8},
        {"label": "alnum(62) length=8", "charset": 62, "length": 8},
        {"label": "alnum+sym(72) length=10", "charset": 72, "length": 10},
    ]
    estimates = []
    for p in policies:
        space = _estimate_space(p["charset"], p["length"])
        seconds_full = space / hps if hps > 0 else float("inf")
        estimates.append({
            "policy": p["label"],
            "keyspace": space,
            "time_full_search_seconds": seconds_full,
            "time_full_search_human": _format_seconds(seconds_full) if math.isfinite(seconds_full) else "inf",
            "time_avg_search_human": _format_seconds(seconds_full/2) if math.isfinite(seconds_full) else "inf",
        })

    payload: Dict[str, Any] = {
        "tool": "hash-audit",
        "cached": False,
        "algo": algo,
        "salt_mode": salt_mode,
        "salt_len": salt_len,
        "benchmark_seconds": seconds,
        "hashes_computed": count,
        "elapsed_seconds": elapsed,
        "hashes_per_second": hps,
        "estimates": estimates,
    }

    if use_cache:
        save_cached_benchmark(key, payload)
    return payload
