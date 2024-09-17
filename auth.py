from flask import Blueprint, request, jsonify, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        pin = request.json.get('pin')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.pin, pin):
            return jsonify({'message': 'Invalid credentials'}), 401

        session['user_id'] = user.id
        return jsonify({'message': 'Logged in successfully', 'is_admin': user.is_admin}), 200
    
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.json.get('username')
        pin = request.json.get('pin')

        if not username or not pin or len(pin) != 4:
            return jsonify({'message': 'Invalid input'}), 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': 'Username already exists'}), 400

        new_user = User(username=username, pin=generate_password_hash(pin, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
    
    return render_template('register.html')

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200
