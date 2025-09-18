# run.py
from app import create_app
from app.keys import generate_rsa_key, start_key_rotation

# Create the Flask app instance
app = create_app()

# Generate a initial RSA key
start_key_rotation()

if __name__ == "__main__":
    # Run the app on port 8080
    app.run(host="0.0.0.0", port=8080, debug=True)