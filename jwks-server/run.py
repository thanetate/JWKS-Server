# run.py
from app import create_app
from app.keys import generate_rsa_key

# Create the Flask app instance
app = create_app()

# Generate a initial RSA key
generate_rsa_key()

if __name__ == "__main__":
    # Run the app on port 8080
    app.run(host="0.0.0.0", port=8080, debug=True)