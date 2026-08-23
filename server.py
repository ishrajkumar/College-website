from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/courses")
def courses():
    return render_template("courses.html")

@app.route("/application")
def application():
    return render_template("cation.html")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/notice")
def notice():
    return render_template("notice.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/ba")
def ba():
    return render_template("ba.html")

@app.route("/bsc")
def bsc():
    return render_template("bsc.html")

@app.route("/bca")
def bca():
    return render_template("bca.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("Name")
    email= request.form.get("Email")
    subject= request.form.get("Subject")
    message= request.form.get("Message")
    print(f" From Contact Inquiry")
    print(f"Received Details:")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Subject: {subject}")
    print(f"Message: {message}")
    return render_template ("submit.html")

app.run(debug=True)
