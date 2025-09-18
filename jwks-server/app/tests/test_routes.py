import pytest
from app import create_app
from app.keys import generate_rsa_key, keys, remove_expired_keys
import datetime
import jwt

@pytest.fixture
def client():
    """
    Create a test client for the Flask app.
    """
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

def test_jwks_endpoint(client):
    """
    Test the /jwks endpoint to ensure it returns valid public keys.
    """
    # Clear the keys list to ensure a clean test environment
    keys.clear()

    # Generate a key
    generate_rsa_key()

    # Call the /jwks endpoint
    response = client.get("/jwks")
    assert response.status_code == 200

    data = response.get_json()
    assert "keys" in data
    assert len(data["keys"]) == 1
    assert "kid" in data["keys"][0]
    assert "n" in data["keys"][0]
    assert "e" in data["keys"][0]

def test_auth_endpoint_valid_key(client):
    """
    Test the /auth endpoint to ensure it issues a valid JWT.
    """
    # Clear the keys list to ensure a clean test environment
    keys.clear()

    # Generate a key
    generate_rsa_key()

    # Call the /auth endpoint
    response = client.post("/auth")
    assert response.status_code == 200

    data = response.get_json()
    assert "token" in data

    # Decode the JWT
    token = data["token"]
    decoded = jwt.decode(token, options={"verify_signature": False})
    assert "sub" in decoded
    assert "iat" in decoded
    assert "exp" in decoded

def test_auth_endpoint_expired_key(client):
    """
    Test the /auth endpoint with expired=true to ensure it issues a JWT with an expired key.
    """
    # Clear the keys list to ensure a clean test environment
    keys.clear()

    # Generate an expired key
    now = datetime.datetime.utcnow()
    expired_key = {
        "kid": "expired-key",
        "private_key": generate_rsa_key(),
        "public_key": "expired-public-key",
        "expiration": now - datetime.timedelta(seconds=1),
    }
    keys.append(expired_key)

    # Call the /auth endpoint with expired=true
    response = client.post("/auth?expired=true")
    assert response.status_code == 200

    data = response.get_json()
    assert "token" in data

    # Decode the JWT
    token = data["token"]
    decoded = jwt.decode(token, options={"verify_signature": False})
    assert "sub" in decoded
    assert "iat" in decoded
    assert "exp" in decoded

def test_auth_endpoint_invalid_query_param(client):
    """
    Test the /auth endpoint with an invalid 'expired' query parameter.
    """
    # Call the /auth endpoint with an invalid query parameter
    response = client.post("/auth?expired=invalid")
    assert response.status_code == 400

    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Invalid 'expired' query parameter. Must be 'true' or 'false'."