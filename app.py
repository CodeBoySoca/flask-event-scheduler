from flask import Flask, render_template, url_for, request, session, redirect, url_for
from flask_session import Session
from models import *
from passlib.hash import pbkdf2_sha256
from dotenv import load_dotenv
from flask_htmx import HTMX
import json

app = Flask(__name__)
htmx = HTMX(app)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] =  'filesystem'
Session(app)


@app.route('/event/search')
def index():
    user=session['user']
    return render_template('index.html', page_title='Event Search', notification_count = user['notification_count'])

@app.route('/<city>/<category>', methods=['GET', 'POST'])
def locale():
    return render_template('search-results.html', page_title='Event Search Results')

@app.route('/add/event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        form = request.form.to_dict()
        Event.add_event(**form)
    return render_template('event.html', page_title='Add Event', notification_count = session['user']['notification_count'])

@app.route('/events')
def events():
    return render_template('events.html', page_title='Events', notification_count = session['user']['notification_count'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.to_dict()
        result = User.check_account(user)
        password_result = pbkdf2_sha256.verify(user['password'], result[0]['password'])
        if password_result is not None and password_result is not False:
            events = Notification.get(user['email'])[0]['events']
            notification_count = len([notification for notification in events])
            session['user'] = { 
                'name' : result[0]['name'], 
                'email' : result[0]['email'],
                'notification_count' : notification_count
            }
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = request.form.to_dict()
        check_email_result = User.check_email(form['email'])
        if form['password'] == form['confirm-password'] and not check_email_result :
            form['password'] = pbkdf2_sha256.hash(request.form.get('password'))
            del form['confirm-password']
            session['user'] = {'email' : form['email'], 'name' : form['name']}
            User.create(form)
    return render_template('register.html')

@app.route('/notifications', methods=['GET'])
def notifications():
    events = Notification.get(session['user']['email'])[0]['events']
    event_data = [event for event in events]
    notification_data = []
    for i in range(len(event_data)):
        notification_data.append(
          event_data[i]['notifications']
        )
    return render_template('notifications.html', notification=notification_data, notification_count = session['user']['notification_count'])
    

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', page_title='404 - Page not found', notification_count = 0)


if __name__ == '__main__':
    app.run() 


