from flask import Flask, render_template, url_for, request, session, redirect, url_for
from flask_session import Session
from models import *
from passlib.hash import pbkdf2_sha256
import json
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit




app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] =  'filesystem'
Session(app)
socketio = SocketIO(app)

@app.route('/event/search')
def index():
    return render_template('index.html', page_title='Event Search')

@app.route('/<city>/<category>', methods=['GET', 'POST'])
def locale():
    return render_template('search-results.html', page_title='Event Search Results')

@app.route('/add/event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        form = request.form.to_dict()
        Event.add_event(**form)
    return render_template('event.html', page_title='Add Event')

@app.route('/events')
def events():
    return render_template('events.html', page_title='Events')

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
            session['user'] = { 
                'name' : result[0]['name'], 
                'email' : result[0]['email']
            }
            return render_template('index.html', user=session['user'])
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

@socketio.on('notifications')
def notifications():
    notification_data = Notification.get(session['user']['email'])
    if not notifications:
        notification_data = {'message' : 'You have no notifications'}
    emit('notification', notification_data)
    return 200, 'ok'


if __name__ == '__main__':
    socketio.run(app) 


