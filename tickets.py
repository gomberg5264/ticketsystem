from flask import Blueprint, request, jsonify, session, render_template
from models import Ticket, User, db

tickets = Blueprint('tickets', __name__)

@tickets.route('/create_ticket', methods=['POST'])
def create_ticket():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    title = request.json.get('title')
    description = request.json.get('description')
    priority = request.json.get('priority')

    if not title or not description or priority not in ['Low', 'Medium', 'High']:
        return jsonify({'message': 'Invalid input'}), 400

    new_ticket = Ticket(title=title, description=description, priority=priority, user_id=session['user_id'])
    db.session.add(new_ticket)
    db.session.commit()

    return jsonify({'message': 'Ticket created successfully'}), 201

@tickets.route('/tickets', methods=['GET'])
def get_tickets():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    tickets = Ticket.query.all()
    return jsonify([{
        'id': ticket.id,
        'title': ticket.title,
        'description': ticket.description,
        'priority': ticket.priority,
        'status': ticket.status,
        'created_at': ticket.created_at.isoformat(),
        'user': ticket.user.username
    } for ticket in tickets]), 200

@tickets.route('/close_ticket/<int:ticket_id>', methods=['PUT'])
def close_ticket(ticket_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({'message': 'Ticket not found'}), 404

    ticket.status = 'Closed'
    db.session.commit()

    return jsonify({'message': 'Ticket closed successfully'}), 200

@tickets.route('/clear_tickets', methods=['DELETE'])
def clear_tickets():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    user = User.query.get(session['user_id'])
    if not user.is_admin:
        return jsonify({'message': 'Admin privileges required'}), 403

    Ticket.query.delete()
    db.session.commit()

    return jsonify({'message': 'All tickets cleared successfully'}), 200

@tickets.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    return render_template('dashboard.html')
