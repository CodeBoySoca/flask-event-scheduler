from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/event/search')
def index():
    return render_template('index.html', page_title='Event Search')

@app.route('/<city>/<category>', methods=['GET', 'POST'])
def locale():
    return render_template('search-results.html', page_title='Event Search Results')

@app.route('/add/event')
def add_event():
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

@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True, port=5111) 


