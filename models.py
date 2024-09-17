from main import db
from sqlalchemy import Integer, String, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    pin: Mapped[str] = mapped_column(String(4), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

class Ticket(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    priority: Mapped[str] = mapped_column(Enum('Low', 'Medium', 'High', name='priority_levels'), nullable=False)
    status: Mapped[str] = mapped_column(Enum('Open', 'Closed', name='ticket_status'), default='Open')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tickets', lazy=True))
