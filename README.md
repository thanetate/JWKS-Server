# SQLite-Backed JWKS Server

## Overview
This project implements a RESTful JWKS (JSON Web Key Set) server that:
- Provides public keys with unique identifiers (`kid`) for verifying JSON Web Tokens (JWTs).
- Issues JWTs signed with RSA private keys stored in a SQLite database.
- Supports key expiry for enhanced security.
- Includes an `/auth` endpoint to issue JWTs and a `/jwks.json` endpoint to serve public keys.
- Handles the issuance of JWTs signed with expired keys when requested.

The server is backed by a SQLite database to persist private keys, ensuring availability even after server restarts.

This project is for educational purposes and should not be used in production without additional security measures.

## Features
1. **SQLite-Backed Key Storage**:
   - RSA private keys are stored in a SQLite database (`totally_not_my_privateKeys.db`).
   - Keys are associated with a unique `kid` and an expiry timestamp (`exp`).

2. **Endpoints**:
   - **`POST /auth`**:
     - Issues a JWT signed with a valid (non-expired) private key.
     - If the `expired` query parameter is provided, issues a JWT signed with an expired private key.
   - **`GET /.well-known/jwks.json`**:
     - Returns all valid (non-expired) public keys in JWKS format.

3. **JWT and JWKS**:
   - JWTs include the `kid` in their headers to identify the signing key.
   - The `kid` in the JWT header matches the `kid` in the JWKS response, allowing verifiers to identify the correct public key.

4. **Key Expiry**:
   - Keys are automatically filtered based on their expiry timestamps.


## Requirements
- Python 3.8+
- SQLite (pre-installed on most systems)

## Usage
1. Start the server:

    python3 main.py

2. Generate a valid jwt:

    curl -X POST http://127.0.0.1:8080/auth

3. Verify the JWT is using the public key:

    curl -X GET http://127.0.0.1:8080/.well-known/jwks.json

4. Request a JWT signed with an expired key:

    curl -X POST "http://127.0.0.1:8080/auth?expired=true"

## Testing
pip install pytest pytest-cov

pytest --cov=main

## Acknowledgment of AI Usage
This project was developed with the assistance of AI tools to help with code generation, debugging, and documentation. Specifically, AI was used to:

- Scaffold the project structure.
- Implement SQLite-backed key storage and database queries.
- Write and refine the /jwks.json and /auth endpoints.
- Improve error handling and validation.
- Draft the README.md documentation.
- Write unit tests for the /jwks.json and /auth endpoints, as well as for database functionality.

Throughout the development process, I used AI in small, incremental steps. I prompted the AI to generate code in manageable chunks, tested each piece of functionality as it was implemented, and iteratively refined the code based on the results. Additionally, I asked the AI to explain key concepts (e.g., SQLite, JWKS, JWT, RSA key generation, and key rotation) to deepen my understanding of the underlying principles and ensure I could apply them correctly.

The following prompts were used to guide the AI:
- "Scaffold a JWKS server with SQLite-backed key storage."
- "Write a /jwks.json endpoint to serve public keys from a database."
- "Implement a /auth endpoint to issue JWTs signed with RSA keys stored in SQLite."
- "Explain how to securely store and retrieve RSA keys in SQLite."
- "Write unit tests for the /auth and /jwks.json endpoints."

This acknowledgment is provided in compliance with academic honesty policies.

## Screenshots
