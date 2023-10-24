from app import db, login_manager
from flask_login import UserMixin


"""Function to get user by id"""
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_password = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    # Define a relationship to link User to Event
    events = db.relationship('Event', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.user_name}', '{self.user_email}', '{self.image_file}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Event('{self.title}', '{self.start}', '{self.end}', '{self.description}')"
