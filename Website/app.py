'''
from flask import Flask
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return render_template('%s.html' % page_name)
    return """
    <h1>Hello Heroku</h1>
    <p>It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400">
    """.format(time=the_time)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
'''
from flask import Flask, render_template, url_for
 
app = Flask(__name__)
 
@app.route('/')
def render_static():
    #url_for('static', filename='main.css')5
    return render_template("index.html")
 
if __name__ == '__main__':
    app.run()
