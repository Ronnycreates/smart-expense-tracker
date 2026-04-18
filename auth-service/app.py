from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os, hashlib

app = Flask(__name__)
CORS(app)

USERS_FILE = 'users.json'

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    users = load_users()
    if data['email'] in users:
        return jsonify({'error': 'User already exists'}), 400
    users[data['email']] = {
        'name': data['name'],
        'password': hash_password(data['password']),
        'budget': data.get('budget', 5000)
    }
    save_users(users)
    return jsonify({'message': 'Registered successfully!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    users = load_users()
    user = users.get(data['email'])
    if not user or user['password'] != hash_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    return jsonify({
        'message': 'Login successful!',
        'name': user['name'],
        'email': data['email'],
        'budget': user['budget']
    })

@app.route('/user/<email>', methods=['GET'])
def get_user(email):
    users = load_users()
    user = users.get(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'name': user['name'], 'email': email, 'budget': user['budget']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5001)))