from hash_audit.hashing import HashSpec, hash_password, verify_password

def test_known_md5():
    spec = HashSpec(algo="md5")
    assert hash_password("hello", spec) == "5d41402abc4b2a76b9719d911017c592"

def test_salt_prefix_roundtrip():
    spec = HashSpec(algo="sha256", salt_mode="prefix", salt="SALT")
    h = hash_password("pw", spec)
    assert verify_password("pw", h, spec) is True
    assert verify_password("pw2", h, spec) is False
