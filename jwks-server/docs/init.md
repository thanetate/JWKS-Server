1. Init 

we run the server using:
python3 run.py

then we can curl the endpoints to make sure they are working. 

curl http://127.0.0.1:8080/jwks
{
  "keys": []
}
curl -X POST http://127.0.0.1:8080/auth
{
  "token": "valid_token_placeholder"
}

2. JWKS endpoint
  Key Generation:
  The generate_rsa_key() function created an RSA key pair and stored it in memory with a unique kid and expiration timestamp.
  JWKS Response:

  The /jwks endpoint used get_valid_public_keys() to retrieve the public key in JWKS format, which includes:
  kty: Key type (RSA).
  kid: Unique key ID.
  use: Key usage (sig for signing).
  alg: Algorithm (RS256).
  n: Base64-encoded modulus.
  e: Base64-encoded exponent.
