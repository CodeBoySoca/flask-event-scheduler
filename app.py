from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
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


if __name__ == '__main__':
    app.run(debug=True) 


