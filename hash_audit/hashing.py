from __future__ import annotations
import hashlib
from dataclasses import dataclass
from typing import Literal

Algo = Literal["md5", "sha1", "sha256"]
SaltMode = Literal["none", "prefix", "suffix"]

@dataclass(frozen=True)
class HashSpec:
    algo: Algo
    salt_mode: SaltMode = "none"
    salt: str = ""

    def apply_salt(self, password: str) -> str:
        if self.salt_mode == "none" or not self.salt:
            return password
        if self.salt_mode == "prefix":
            return f"{self.salt}{password}"
        if self.salt_mode == "suffix":
            return f"{password}{self.salt}"
        raise ValueError(f"Unknown salt_mode: {self.salt_mode}")

def hash_password(password: str, spec: HashSpec) -> str:
    material = spec.apply_salt(password).encode("utf-8")
    h = hashlib.new(spec.algo)
    h.update(material)
    return h.hexdigest()

def verify_password(password: str, expected_hash: str, spec: HashSpec) -> bool:
    return hash_password(password, spec) == expected_hash.lower()
