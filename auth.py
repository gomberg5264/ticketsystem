from flask import Blueprint, request, session, jsonify, redirect, url_for, render_template, current_app
from models import User, db
import logging

auth = Blueprint('auth', __name__)

ADMIN_PIN = "5264062"

@auth.route('/login', methods=['GET', 'POST'])
def login():
    current_app.logger.info("Login route accessed")
    if request.method == 'GET':
        current_app.logger.info("GET request to login page")
        return render_template('login.html')
    
    if request.method == 'POST':
        current_app.logger.info("POST request to login")
        data = request.json
        pin = data.get('pin')
        current_app.logger.info(f"Received PIN: {pin}")
        
        if pin == ADMIN_PIN:
            current_app.logger.info("Valid PIN entered")
            user = User.query.filter_by(pin=pin).first()
            if not user:
                current_app.logger.info("Creating new admin user")
                user = User(pin=pin, is_admin=True)
                db.session.add(user)
                db.session.commit()
            
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            current_app.logger.info(f"User logged in: ID={user.id}, Is Admin={user.is_admin}")
            return jsonify({'message': 'Logged in successfully', 'is_admin': user.is_admin}), 200
        else:
            current_app.logger.warning("Invalid PIN entered")
            return jsonify({'error': 'Invalid PIN'}), 401

@auth.route('/logout')
def logout():
    current_app.logger.info("Logout route accessed")
    session.pop('user_id', None)
    session.pop('is_admin', None)
    return redirect(url_for('auth.login'))

@auth.route('/')
def index():
    current_app.logger.info("Index route accessed, redirecting to login")
    return redirect(url_for('auth.login'))
