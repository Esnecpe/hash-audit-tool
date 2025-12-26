# Hash Cracker (Cybersecurity Project) — Defensive Edition: **Hash Audit Lab**

> This repository is intentionally **defensive**: it helps you **generate**, **verify**, and **benchmark**
> password hashing approaches so you can explain *why* salts + slow KDFs matter.
> It **does not** provide password recovery / hash-cracking features.

## Origin's Attribution
California State University Fullerton (CSUF), **CPSC 253 (Cybersecurity Foundations and Principles)**: Security goals, security systems, access controls, networks and security, integrity, cryptography fundamentals, authentication. Attacks: software, network, website; management considerations, security standards in government and industry; security issues in requirements, architecture, design, implementation, testing, operation, maintenance, acquisition and services.

## Features
- ✅ Hash generation: `md5`, `sha1`, `sha256`
- ✅ Salted hashing (prefix or suffix)
- ✅ Hash verification (check a candidate password against a hash + salt parameters)
- ✅ Benchmarking (hashes/sec + attacker-cost estimates)
- ✅ Output reports: `--output json` and `--output html`
- ✅ Caching of benchmark results
- ✅ `pytest` tests + GitHub Actions CI

## Quickstart
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -e ".[dev]"
hash-audit --help
```

### Generate a hash
```bash
hash-audit generate --algo sha256 --password "MyP@ssw0rd!" --salt-mode prefix --salt "SALT123"
```

### Verify a password against a stored hash
```bash
hash-audit verify --algo sha256 --password "MyP@ssw0rd!" --hash <HASH> --salt-mode prefix --salt "SALT123"
```

### Benchmark and create JSON + HTML reports
```bash
hash-audit benchmark --algo sha256 --seconds 2 --output json --out report.json
hash-audit benchmark --algo sha256 --seconds 2 --output html --out report.html
```

## Ethical use
Designed for learning and defensive auditing only. Do not use for unauthorized access.
