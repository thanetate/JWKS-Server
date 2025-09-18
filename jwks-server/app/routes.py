from flask import Blueprint, jsonify, request
from app.keys import generate_rsa_key, get_valid_public_keys, keys
import jwt
import datetime

# Blueprint for routes
bp = Blueprint("routes", __name__)

def register_routes(app):
    """
    Register all routes with the Flask app.
    """
    app.register_blueprint(bp)

# JWKS endpoint
@bp.route("/jwks", methods=["GET"])
def jwks():
    """
    JWKS endpoint to serve public keys.
    """
    try:
        # Get valid public keys in JWKS format
        public_keys = get_valid_public_keys()
        return jsonify({"keys": public_keys}), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve JWKS", "details": str(e)}), 500

# Auth endpoint
@bp.route("/auth", methods=["POST"])
def auth():
    """
    Auth endpoint to issue JWTs.
    """
    try:
        # Validate the 'expired' query parameter
        expired_param = request.args.get("expired", "false").lower()
        if expired_param not in ["true", "false"]:
            return jsonify({"error": "Invalid 'expired' query parameter. Must be 'true' or 'false'."}), 400

        expired = expired_param == "true"

        # Select the appropriate key
        now = datetime.datetime.utcnow()
        selected_key = None

        if expired:
       # Find an expired key
            for key in keys:
                if key["expiration"] <= now:
                    selected_key = key
                    break
        else:
            # Find an unexpired key
            for key in keys:
                if key["expiration"] > now:
                    selected_key = key
                    break

        # If no key is found, return an error
        if not selected_key:
            return jsonify({"error": "No suitable key found"}), 500

        # Create the JWT
        private_key = selected_key["private_key"]
        kid = selected_key["kid"]
        payload = {
            "sub": "user123",  # Example subject claim
            "iat": int(now.timestamp()),  # Issued at
            "exp": int((now + datetime.timedelta(minutes=15)).timestamp()),  # Expires in 15 minutes
        }
        token = jwt.encode(
            payload,
            private_key,
            algorithm="RS256",
            headers={"kid": kid},
        )

        return jsonify({"token": token}), 200

    except Exception as e:
        return jsonify({"error": "Failed to issue JWT", "details": str(e)}), 500

# Global error handler
@bp.app_errorhandler(500)
def handle_internal_server_error(e):
    """
    Handle unexpected server errors.
    """
    return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500