from app import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(80), unique=True, nullable=False)
    user_email = Column(String(120), unique=True, nullable=False)
    user_password = Column(String(60), nullable=False)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    image_file = Column(String(20), nullable=False, default='default.jpg')
    # Define a relationship to link User to Event
    events = relationship('Event', back_populates='user')

    def __repr__(self):
        return f"User('{self.user_name}', '{self.user_email}', '{self.image_file}')"


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    description = Column(String(120), nullable=False)

    # Establish a relationship with the User table
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Define a relationship to link Event to User
    user = relationship('User', back_populates='events')

    def __repr__(self):
        return f"Event('{self.id}', '{self.title}', '{self.start}', '{self.end}', '{self.description}')"


Base.metadata.create_all(engine)  # Create the table if it doesn't exist
