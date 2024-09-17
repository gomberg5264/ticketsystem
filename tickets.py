from flask import Blueprint, request, session, jsonify, render_template
from models import Ticket, db
from sqlalchemy.exc import SQLAlchemyError

tickets = Blueprint('tickets', __name__)

@tickets.route('/tickets', methods=['GET', 'POST'])
def handle_tickets():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    if request.method == 'GET':
        try:
            tickets = Ticket.query.all()
            return render_template('tickets.html', tickets=[{
                'id': ticket.id,
                'title': ticket.title,
                'description': ticket.description,
                'priority': ticket.priority,
                'status': ticket.status,
                'created_at': ticket.created_at.isoformat(),
                'user_id': ticket.user_id
            } for ticket in tickets])
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': 'Database error', 'details': str(e)}), 500

    elif request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        title = data.get('title')
        description = data.get('description')
        priority = data.get('priority')

        if not title or not description or priority not in ['Low', 'Medium', 'High']:
            return jsonify({'error': 'Invalid input data'}), 400

        try:
            new_ticket = Ticket(title=title, description=description, priority=priority, user_id=session['user_id'])
            db.session.add(new_ticket)
            db.session.commit()
            return jsonify({'message': 'Ticket created successfully', 'ticket_id': new_ticket.id}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': 'Database error', 'details': str(e)}), 500

@tickets.route('/close_ticket/<int:ticket_id>', methods=['POST'])
def close_ticket(ticket_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return jsonify({'error': 'Ticket not found'}), 404
        
        ticket.status = 'Closed'
        db.session.commit()
        return jsonify({'message': 'Ticket closed successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500

@tickets.route('/clear_tickets', methods=['POST'])
def clear_tickets():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized access'}), 403

    try:
        Ticket.query.delete()
        db.session.commit()
        return jsonify({'message': 'All tickets cleared'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
