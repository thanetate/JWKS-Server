from app.keys import generate_rsa_key, remove_expired_keys, keys
import datetime


def test_generate_rsa_key():
    """
    Test RSA key generation.
    """
    # Generate a key
    generate_rsa_key()
    assert len(keys) == 1
    assert "kid" in keys[0]
    assert "private_key" in keys[0]
    assert "public_key" in keys[0]
    assert "expiration" in keys[0]


def test_remove_expired_keys():
    """
    Test removal of expired keys.
    """
    # Clear the keys list to ensure a clean test environment
    keys.clear()

    # Add an expired key
    now = datetime.datetime.utcnow()
    expired_key = {
        "kid": "expired-key",
        "private_key": None,
        "public_key": None,
        "expiration": now - datetime.timedelta(seconds=1),
    }
    keys.append(expired_key)

    # Add a valid key
    generate_rsa_key()

    # Remove expired keys
    remove_expired_keys()
    assert len(keys) == 1
    assert keys[0]["kid"] != "expired-key"