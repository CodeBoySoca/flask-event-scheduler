from flask import Flask, render_template, url_for, request, session
from flask_session import Session
from models import *
from passlib.hash import pbkdf2_sha256
import json
from dotenv import load_dotenv
from pymongo import MongoClient

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] =  'filesystem'
Session(app)

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
    pass

@app.route('/')
def login():
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


if __name__ == '__main__':
    app.run(debug=True, port=5111) 


