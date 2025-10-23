import pytest
import sqlite3
import requests
from http.server import HTTPServer
from threading import Thread
from main import db_file, hostName, serverPort, MyServer

# Start the server in a separate thread
@pytest.fixture(scope="module")
def start_server():
    server = HTTPServer((hostName, serverPort), MyServer)
    thread = Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield
    server.shutdown()
    thread.join()

# Test database initialization
def test_database():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='keys';")
    table = cursor.fetchone()
    conn.close()
    assert table is not None, "The 'keys' table should exist in the database."

# Test /auth endpoint for valid JWT
def test_auth_valid_key(start_server):
    response = requests.post(f"http://{hostName}:{serverPort}/auth")
    assert response.status_code == 200, "The /auth endpoint should return 200 for valid keys."
    data = response.json()
    assert "token" in data, "The response should contain a 'token'."

# Test /jwks.json endpoint for valid keys
def test_jwks_valid_keys(start_server):
    response = requests.get(f"http://{hostName}:{serverPort}/.well-known/jwks.json")
    assert response.status_code == 200, "The /jwks.json endpoint should return 200."
    data = response.json()
    assert "keys" in data, "The response should contain a 'keys' field."
    assert len(data["keys"]) > 0, "The 'keys' field should contain at least one valid key."