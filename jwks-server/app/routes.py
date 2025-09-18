# app/routes.py
from flask import Blueprint, jsonify, request
from app.keys import generate_rsa_key, get_valid_public_keys

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
    # Get valid public keys in JWKS format
    public_keys = get_valid_public_keys()
    return jsonify({"keys": public_keys}), 200

# Auth endpoint
@bp.route("/auth", methods=["POST"])
def auth():
    """
    Auth endpoint to issue JWTs.
    """
    # Check for the 'expired' query parameter
    expired = request.args.get("expired", "false").lower() == "true"

    # Placeholder response
    if expired:
        return jsonify({"token": "expired_token_placeholder"}), 200
    else:
        return jsonify({"token": "valid_token_placeholder"}), 200