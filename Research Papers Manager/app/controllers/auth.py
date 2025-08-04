from flask import Blueprint, request, jsonify
from ..services.user_service import (
    register_user, authenticate_user,
    UserAlreadyExists, InvalidCredentials
)
from ..utils.validators import (
    validate_signup_input, validate_login_input
)

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    payload = request.get_json() or {}
    errors = validate_signup_input(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        uid = register_user(payload)
        return jsonify({
            "message": "User registered",
            "user_id": str(uid)
        }), 201

    except UserAlreadyExists:
        return jsonify({"message": "Username taken"}), 409

@auth_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json() or {}
    errors = validate_login_input(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        uid = authenticate_user(payload)
        return jsonify({
            "message": "Login successful",
            "user_id": str(uid)
        }), 200

    except InvalidCredentials:
        return jsonify({"message": "Invalid username or password"}), 401

