from flask import render_template, request, url_for, redirect, flash, jsonify, json
from app import app, db, bcrypt
from app.forms import SignupForm, LoginForm
from app.models import User, Event
from datetime import datetime
from flask_login import login_user, current_user, logout_user


@app.route("/home/")
def home():
    return render_template('home.html')


@app.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.user_email.data).first() # check if email is in database
        if user and bcrypt.check_password_hash(user.user_password, form.user_password.data):
            login_user(user)
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Check your Email and Password!', 'success')
    return render_template('login.html', form=form)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.user_password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, user_name=form.user_name.data, user_email=form.user_email.data, user_password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', form=form)


@app.route('/events')
def events():
    return render_template('events.html', title='Events', content_title="All Events")


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/create_event', methods=['POST'])
def create_event():
    data = request.get_json()
    title = data['title']
    start = data['start']
    end = data['end']
    description = data['description']

    # Format the date and time strings
    formatted_start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S.%fZ')
    formatted_end = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S.%fZ')

    user_id = current_user.id

    # Create a new Event object
    new_event = Event(title=title, start=formatted_start, end=formatted_end, description=description, user_id=user_id)
    # Add the event to the session and commit it to the database
    db.session.add(new_event)
    db.session.commit()
    return jsonify('Success')


@app.route('/get_events', methods=['GET'])
def get_events():
    user_id = current_user.id
    # Query the database to retrieve the events
    events = Event.query.filter(Event.user_id == user_id).all()

    # Convert the retrieved events to a JSON-serializable format
    event_data = [{
        'title': event.title,
        'start': event.start.isoformat(),
        'end': event.end.isoformat(),
        'description': event.description
    } for event in events]

    return jsonify(event_data)
