from flask import Flask, request, jsonify
from services.auth_service import is_username_taken, mark_username_taken
from validations.user_validation import validate_user_data, validate_username
from models.user import users_collection
import bcrypt

app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    is_valid, error = validate_user_data(data)
    if not is_valid:
        return jsonify({'error': error}), 400

    username = data['username']

    if is_username_taken(username):
        return jsonify({'error': 'Username already taken'}), 409

    hashed_pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()

    user = {
        'username': username,
        'name': data['name'],
        'email': data['email'],
        'password': hashed_pw,
        'department': data['department']
    }
    result = users_collection.insert_one(user)

    mark_username_taken(username)

    return jsonify({'message': 'User registered', 'user_id': str(result.inserted_id)}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json

    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400

    if not validate_username(username):
        return jsonify({'error': 'Invalid username format.'}), 400

    user = users_collection.find_one({'username': username})

    if not user:
        return jsonify({'error': 'Invalid credentials.'}), 401

    if not bcrypt.checkpw(password.encode(), user['password'].encode()):
        return jsonify({'error': 'Invalid credentials.'}), 401

    return jsonify({
        'message': 'Login successful',
        'user_id': str(user['_id'])
    }), 200
