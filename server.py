from werkzeug.security import generate_password_hash , check_password_hash

from flask import Flask, render_template, request, session , redirect 

import sqlite3

app = Flask(__name__)
app.secret_key = "my_college"

def init_db():
    conn = sqlite3.connect("user.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS users(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 email TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL
                 )
                 """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")

    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("user.db")
        
        try:
            conn.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email,hashed_password))
            conn.commit()
            conn.close()
            return redirect("/register")
            
        except sqlite3.IntegrityError:
            conn.close()
            return "Email Already Exists!"

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        conn = sqlite3.connect("user.db")

        user = conn.execute("SELECT * FROM users WHERE email = ?" , (email,)).fetchone()

        conn.close()

        if user and check_password_hash(user[2], password):
            session['user'] = email
            return "Login Succesful!"

        else:
            return "Data not Found"

@app.route("/change-password", methods=["GET", "POST"])
def change_password():

    if "user" not in session:
        return "Please Login First"

    if request.method == "GET":
        return render_template("change_password.html")

    if request.method == "POST":

        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")

        email = session["user"]

        conn = sqlite3.connect("user.db")

        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if user and check_password_hash(user[2], old_password):

            new_hashed_password = generate_password_hash(new_password)

            conn.execute(
                "UPDATE users SET password = ? WHERE email = ?",
                (new_hashed_password, email)
            )

            conn.commit()
            conn.close()

            return "Password Changed Successfully!"

        else:
            conn.close()
            return "Old Password is Wrong!"

if __name__ == "__main__":
    app.run(debug=True)



