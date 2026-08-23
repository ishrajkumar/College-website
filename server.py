import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route("/application")
def application():
    return render_template("cation.html")

@app.route("/courses")
def courses():
    return render_template("courses.html")

@app.route("/notice")
def notice():
    return render_template("notice.html")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
