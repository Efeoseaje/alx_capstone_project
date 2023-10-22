from flask import render_template, request, url_for, redirect, flash, jsonify
from app import app, salt, bcrypt, session
from app.forms import SignupForm, LoginForm
from app.models import User, Event
from datetime import datetime


@app.route("/home/")
def home():
    return render_template('home.html')


@app.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter_by(user_email=form.user_email.data).first()
        if user and bcrypt.checkpw(form.user_password.data.encode('utf-8'), user.user_password.encode('utf-8')):
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Check your Email and Password!', 'success')
    return render_template('login.html', form=form)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.hashpw(form.user_password.data.encode('utf-8'), salt)
        new_user = User(user_name=form.user_name.data, user_email=form.user_email.data, user_password=hashed_password, first_name=form.first_name.data, last_name=form.last_name.data)
        session.add(new_user)
        session.commit()
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


@app.route('/create_event', methods=['POST'])
def create_event():
    data = request.get_json()
    title = data['title']
    start = data['start']
    end = data['end']
    description = data['description']

    # Format the date and time strings
    formatted_start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
    formatted_end = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')

    # Create a new Event object
    print('about to')
    new_event = Event(title=title, start=formatted_start, end=formatted_end, description=description, user_id=user_id)
    # Add the event to the session and commit it to the database
    session.add(new_event)
    session.commit()
    session.close()
    print('success')
    return jsonify({'message': 'Event created successfully'})
