# app/keys.py
import uuid
import datetime
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# In-memory storage for keys
keys = []

# Key expiration duration (in seconds)
KEY_EXPIRATION_SECONDS = 3600  # 1 hour


def generate_rsa_key():
    """
    Generate a new RSA key pair and store it in memory with metadata.
    """
    # Generate RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Serialize the public key
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # Generate metadata
    kid = str(uuid.uuid4())  # Unique Key ID
    expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=KEY_EXPIRATION_SECONDS)

    # Store the key in memory
    keys.append({
        "kid": kid,
        "private_key": private_key,
        "public_key": public_pem.decode("utf-8"),
        "expiration": expiration,
    })


def get_valid_public_keys():
    """
    Return all unexpired public keys in JWKS format.
    """
    global keys

    # Remove expired keys
    now = datetime.datetime.utcnow()
    valid_keys = [key for key in keys if key["expiration"] > now]

    # Update the in-memory key list
    keys = valid_keys

    # Convert to JWKS format
    jwks_keys = []
    for key in valid_keys:
        jwks_keys.append({
            "kty": "RSA",
            "kid": key["kid"],
            "use": "sig",
            "alg": "RS256",
            "n": _get_modulus(key["public_key"]),
            "e": _get_exponent(key["public_key"]),
        })

    return jwks_keys


def _get_modulus(public_key_pem):
    """
    Extract the modulus (n) from the public key.
    """
    public_key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))
    numbers = public_key.public_numbers()
    return _int_to_base64(numbers.n)


def _get_exponent(public_key_pem):
    """
    Extract the exponent (e) from the public key.
    """
    public_key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"))
    numbers = public_key.public_numbers()
    return _int_to_base64(numbers.e)


def _int_to_base64(value):
    """
    Convert an integer to a base64-encoded string.
    """
    import base64
    return base64.urlsafe_b64encode(value.to_bytes((value.bit_length() + 7) // 8, "big")).decode("utf-8").rstrip("=")