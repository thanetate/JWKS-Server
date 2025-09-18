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

  jwks-server [main●●] % curl http://127.0.0.1:8080/jwks
  {
    "keys": [
      {
        "alg": "RS256",
        "e": "AQAB",
        "kid": "0f57cba1-b19a-4132-9616-b72c3def5295",
        "kty": "RSA",
        "n": "tTy8skuQMD1hiGzq3xCOH4DBfFKfM27er3_WFR2gn5mvUBB8xkCk_PAlpgLaMGEl2MLPUr8AX8BFyDx6K0BTdfVr22hG3PLHvhuGX57jQY0qE4Yq42bLXQlPXZdlcmFCxiletnQMTyR67Tw3gmBHA3WnNsviIkdc1nMS-EvjnDia5ZTymM7M4y3FvIl3FrPn46M7cDZieINqOErVhGojXHm5oPkn813uz7dlrNDsTr7It2iZaoKzjQbe8_TvsjTGzzOkrkqZTSHNT3jXto0P-9M3lGnRJAL_yFrKHqp2zWTh10HjEEvy6I-thcXVU148jb6bjpwOh1TLUw2c3DF6HQ",
        "use": "sig"
      }
    ]
  }

3. Sign JWTs:
  Use the private key to sign JWTs.
  Include the kid in the JWT header so the verifier knows which public key to use.
  Handle Expired Keys:
  If the expired query parameter is provided, issue a JWT signed with an expired key.

  }

  jwks-server [main●] % curl -X POST http://127.0.0.1:8080/auth
  {
    "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjBmNTdjYmExLWIxOWEtNDEzMi05NjE2LWI3MmMzZGVmNTI5NSIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwiaWF0IjoxNzU4MjMyOTQyLCJleHAiOjE3NTgyMzM4NDJ9.ayA-_6q1m2U8tBNURAf7B286wdhttPzIJQLWFxki4ojk_Yoh90tdNmSzaYo-REcWcrmbXB2kncabEb_cOlk-M0JwbqtpctKIJ5KVYrJbhiIKzdrlZfPHo8EtOZ5EgSr01XaQTLTEEUSSTjQUdcaa4cZDRN0Txx7r9aJ293yB7DJA4Ed6Sz356_a0NNowcl3GKPiSJJBuCG6w2OMU_5OlLXeBNtx8H8mcY3L0MgOEmBentf_OKiXj44A_qg-rebW-ttcB5_FGD8VJI4pm-KH-5b6lXdOo5FLTeoPtmYB66kPBrgfwi3mEkrv5kQoJYPPMCoqeS-ed2hT2uT9EuVp1Hg"
  }
  jwks-server [main●] % curl -X POST "http://127.0.0.1:8080/auth?expired=true"
  {
    "error": "No suitable key found"
  }