from http.server import BaseHTTPRequestHandler, HTTPServer
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from urllib.parse import urlparse, parse_qs
import base64
import json
import jwt
import datetime
import sqlite3

db_file = "totally_not_my_privateKeys.db"
hostName = "localhost"
serverPort = 8080

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
expired_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)
expired_pem = expired_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

numbers = private_key.private_numbers()


def int_to_base64(value):
    """Convert an integer to a Base64URL-encoded string"""
    value_hex = format(value, 'x')
    # Ensure even length
    if len(value_hex) % 2 == 1:
        value_hex = '0' + value_hex
    value_bytes = bytes.fromhex(value_hex)
    encoded = base64.urlsafe_b64encode(value_bytes).rstrip(b'=')
    return encoded.decode('utf-8')


class MyServer(BaseHTTPRequestHandler):
    def do_PUT(self):
        self.send_response(405)
        self.end_headers()
        return

    def do_PATCH(self):
        self.send_response(405)
        self.end_headers()
        return

    def do_DELETE(self):
        self.send_response(405)
        self.end_headers()
        return

    def do_HEAD(self):
        self.send_response(405)
        self.end_headers()
        return
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/auth":
            conn = sqlite3.connect(db_file) 
            cursor = conn.cursor() 
            query_params = parse_qs(parsed_path.query)
            expired = "expired" in query_params
            current_time = int(datetime.datetime.now().timestamp())

            # query the db for keys
            if expired:
                cursor.execute("SELECT kid, key FROM keys WHERE exp <= ? ORDER BY exp DESC LIMIT 1", (current_time,))
            else:
                cursor.execute("SELECT kid, key FROM keys WHERE exp > ? ORDER BY exp ASC LIMIT 1", (current_time,))

            row = cursor.fetchone()
            if not row:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"No key found in the db")
                return

            kid, private_key_pem = row

            # deserialize the pk
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode('utf-8'),
                password=None,
            )

            # create a JWT
            payload = {
                "sub": "userABC",
                "iat": current_time,
                "exp": current_time + 3600,  # 1hr
            }
            token = jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": str(kid)})

            # send the response as a JWT
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"token": token}).encode('utf-8'))
            return
        
        self.send_response(405)
        self.end_headers()
    
    def do_GET(self):
        if self.path == "/.well-known/jwks.json":
            conn = sqlite3.connect(db_file) 
            cursor = conn.cursor() 
            current_time = int(datetime.datetime.now().timestamp())

            # query the db for keys
            cursor.execute("SELECT kid, key FROM keys WHERE exp > ?", (current_time,))
            rows = cursor.fetchall()

            # JWKS response
            keys = []
            for row in rows:
                kid, private_key_pem = row

                # deserialize the pk
                private_key = serialization.load_pem_private_key(
                    private_key_pem.encode('utf-8'),
                    password=None,
                )
                public_key = private_key.public_key()
                numbers = public_key.public_numbers()

                # add pk to response
                keys.append({
                    "alg": "RS256",
                    "kty": "RSA",
                    "use": "sig",
                    "kid": str(kid),
                    "n": int_to_base64(numbers.n),
                    "e": int_to_base64(numbers.e),
                })

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"keys": keys}).encode('utf-8'))
            return

        self.send_response(405)
        self.end_headers()


if __name__ == "__main__":
    # db init
    conn = sqlite3.connect(db_file)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS keys (
        kid INTEGER PRIMARY KEY AUTOINCREMENT,
        key BLOB NOT NULL,
        exp INTEGER NOT NULL
    );
    """
    cursor = conn.cursor()
    cursor.execute(create_table_query)  
    conn.commit()
    print(f"Database '{db_file}' initialized and ready.")

    # get expiry timestamp
    current_time = int(datetime.datetime.now().timestamp())
    one_hour_later = int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp())

    # insert both expired and valid keys into db
    # expired
    cursor.execute(
        "INSERT INTO keys (key, exp) VALUES (?, ?)",
        (expired_pem.decode('utf-8'), current_time)
    )
    # valid
    cursor.execute(
        "INSERT INTO keys (key, exp) VALUES (?, ?)",
        (pem.decode('utf-8'), one_hour_later)
    )
    conn.commit()
    print("Keys have been generated and stored in the database.")

    # start the web server
    webServer = HTTPServer((hostName, serverPort), MyServer)
    try:
        print(f"Server started at http://{hostName}:{serverPort}")
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    # close the db connection
    conn.close()
    print("Server Stopped.")