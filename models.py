from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Enum, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pin: Mapped[str] = mapped_column(String(7), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

class Ticket(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    priority: Mapped[str] = mapped_column(Enum('Low', 'Medium', 'High', name='priority_levels'), nullable=False)
    status: Mapped[str] = mapped_column(Enum('Open', 'Closed', name='ticket_status'), default='Open')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tickets', lazy=True))

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
