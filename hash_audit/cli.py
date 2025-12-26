from __future__ import annotations
import argparse
from pathlib import Path

from .hashing import HashSpec, hash_password, verify_password
from .benchmark import run_benchmark
from .reporting import write_json, write_html

def _add_common_hash_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--algo", choices=["md5", "sha1", "sha256"], required=True, help="Hash algorithm.")
    p.add_argument("--salt-mode", choices=["none", "prefix", "suffix"], default="none", help="How to apply salt.")
    p.add_argument("--salt", default="", help="Salt value. Use with --salt-mode prefix|suffix.")

def cmd_generate(args: argparse.Namespace) -> int:
    spec = HashSpec(algo=args.algo, salt_mode=args.salt_mode, salt=args.salt)
    print(hash_password(args.password, spec))
    return 0

def cmd_verify(args: argparse.Namespace) -> int:
    spec = HashSpec(algo=args.algo, salt_mode=args.salt_mode, salt=args.salt)
    ok = verify_password(args.password, args.hash, spec)
    print("MATCH" if ok else "NO MATCH")
    return 0 if ok else 1

def cmd_benchmark(args: argparse.Namespace) -> int:
    payload = run_benchmark(
        algo=args.algo,
        seconds=args.seconds,
        salt_mode=args.salt_mode,
        salt_len=args.salt_len,
        use_cache=not args.no_cache,
    )
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if args.output == "json":
        write_json(out_path, payload)
    else:
        write_html(out_path, payload)
    print(str(out_path))
    return 0

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="hash-audit",
        description="Defensive password hashing lab: generate/verify hashes and benchmark hashing cost.",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="Generate a hash for a password (optionally salted).")
    _add_common_hash_args(g)
    g.add_argument("--password", required=True, help="Password to hash.")
    g.set_defaults(func=cmd_generate)

    v = sub.add_parser("verify", help="Verify a password against a hash (optionally salted).")
    _add_common_hash_args(v)
    v.add_argument("--password", required=True, help="Password to verify.")
    v.add_argument("--hash", required=True, help="Expected hex digest.")
    v.set_defaults(func=cmd_verify)

    b = sub.add_parser("benchmark", help="Benchmark hashes-per-second and estimate attacker cost.")
    b.add_argument("--algo", choices=["md5", "sha1", "sha256"], required=True)
    b.add_argument("--seconds", type=float, default=2.0, help="Benchmark duration.")
    b.add_argument("--salt-mode", choices=["none", "prefix", "suffix"], default="none")
    b.add_argument("--salt-len", type=int, default=0, help="Salt length to model salting overhead.")
    b.add_argument("--no-cache", action="store_true", help="Disable benchmark caching.")
    b.add_argument("--output", choices=["json", "html"], default="json", help="Report format.")
    b.add_argument("--out", default="report.json", help="Output path for the report.")
    b.set_defaults(func=cmd_benchmark)

    return p

def main() -> int:
    p = build_parser()
    args = p.parse_args()
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
