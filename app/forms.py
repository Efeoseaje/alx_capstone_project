"""Application Forms"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, Event

# signup form
class SignupForm(FlaskForm):
    first_name = StringField(
        'First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField(
        'Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    user_name = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=50)])
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    user_password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Password', validators=[DataRequired(), EqualTo('user_password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

    """Check if Username and Email already exist"""
    def validate_user_name(self, user_name):
        user = User.query.filter_by(user_name=user_name.data).first()
        if user:
            raise ValidationError('Username already exist')

    def validate_user_email(self, user_email):
        user = User.query.filter_by(user_email=user_email.data).first()
        if user:
            raise ValidationError('Email already exist')


class LoginForm(FlaskForm):
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    user_password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')
