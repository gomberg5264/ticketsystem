import os
from flask import Flask
from models import init_db
import logging

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)
    
    init_db(app)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from tickets import tickets as tickets_blueprint
    app.register_blueprint(tickets_blueprint)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
