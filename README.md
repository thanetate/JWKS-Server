# JWKS Server

## Objective
This project implements a basic JSON Web Key Set (JWKS) server that:
- Provides public keys with unique identifiers (`kid`) for verifying JSON Web Tokens (JWTs).
- Implements key expiry for enhanced security.
- Includes an authentication endpoint to issue JWTs.
- Handles the issuance of JWTs signed with expired keys based on a query parameter.

This project is for educational purposes. In a real-world scenario, you’d want to integrate with a proper authentication system and ensure security best practices.

---

## Features
- **Key Rotation**: Automatically generates new RSA key pairs at regular intervals and removes expired keys.
- **JWKS Endpoint**: Serves public keys in JWKS format for verifying JWTs.
- **Auth Endpoint**: Issues JWTs signed with valid keys and supports issuing tokens with expired keys.
- **Error Handling**: Provides meaningful error messages and proper HTTP status codes for invalid requests.

---

## Requirements
- Python 3.8 or higher
- Libraries:
  - Flask
  - cryptography
  - PyJWT
  - pytest (for testing)

---

## Installation
1. Clone the repository:

   git clone <repository-url>
   cd jwks-server

2. Create a VM

    python3 -m venv venv
    source venv/bin/activate

3. Install Dependencies 

    pip install -r requirements.txt

## Usage
1. Start the server:

    python3 run.py

2. The server will run on http://127.0.0.1:8080
3. Test the endpoints using curl or Postman

## Endpoints
1. /jwks (GET)

    Description - Returns the public keys in JWKS format.
    Example - curl http://127.0.0.1:8080/jwks

    Response - 
    {
    "keys": [
        {
        "kty": "RSA",
        "kid": "unique-key-id",
        "use": "sig",
        "alg": "RS256",
        "n": "base64-modulus",
        "e": "base64-exponent"
        }
    ]
    }
2. /auth (POST)

    Description - Issues a JWT signed with a valid key. Supports issuing tokens with expired keys using the expired query parameter.
    Parameters - expired (optional): true or false. Default is false. 
    Example - curl -X POST http://127.0.0.1:8080/auth

    Response -
    {
        "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6..."
    }

## Testing
1. Run the test suite

    pytest --cov=app

2. Ensure test coverage is over 80%

## Example Workflow
1. Start the Server

    python3 run.py

2. Generate a valid JWT

    curl -X POST http://127.0.0.1:8080/auth

3. Verify the JWT using the public key from /jwks

4. Request a JWT signed with an expired key

    curl -X POST "http://127.0.0.1:8080/auth?expired=true"

## Notes
The kid in the JWT header matches the kid in the JWKS response, allowing verifiers to identify the correct public key.

This server is for educational purposes and should not be used in production without additional security measures.

## Acknowledgment of AI Usage
This project was developed with the assistance of AI tools to help with code generation, debugging, and documentation. Specifically, AI was used to:
- Scaffold the project structure.
- Implement key functionality such as RSA key generation, JWT issuance, and key rotation.
- Write and refine the `/jwks` and `/auth` endpoints.
- Improve error handling and validation.
- Draft the `README.md` documentation.

Throughout the development process, I used AI in small, incremental steps. I prompted the AI to generate code in manageable chunks, tested each piece of functionality as it was implemented, and iteratively refined the code based on the results. Additionally, I asked the AI to explain key concepts (e.g., JWKS, JWT, RSA key generation, and key rotation) to deepen my understanding of the underlying principles and ensure I could apply them correctly.

The following prompts were used to guide the AI:
- "Scaffold a basic JWKS server in Python."
- "Implement RSA key generation and key rotation."
- "Write a `/jwks` endpoint to serve public keys in JWKS format."
- "Write a `/auth` endpoint to issue JWTs."
- "Improve error handling and validation for the endpoints."
- "Draft a README file for the JWKS server project."
- "Explain how JWKS works and how it relates to JWT verification."
- "Explain how RSA key pairs are generated and used in signing JWTs."

This acknowledgment is provided in compliance with academic honesty policies.

## Screenshots
1. The test client running against the server.
<img width="1686" height="736" alt="image" src="https://github.com/user-attachments/assets/dd8ef055-33d1-4afa-a4a0-c296c3647944" />
<img width="1692" height="836" alt="image" src="https://github.com/user-attachments/assets/7d371387-ae80-44a3-923d-8282e4940f3d" />

2. The test suite showing coverage percentage.
<img width="1654" height="650" alt="image" src="https://github.com/user-attachments/assets/fe01da53-786b-4a4a-9e8b-06c02dad4ee2" />
