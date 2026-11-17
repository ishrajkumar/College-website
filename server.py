from werkzeug.security import generate_password_hash, check_password_hash

from flask import Flask, render_template, request, session, redirect, flash

import sqlite3

app = Flask(__name__)
app.secret_key = "my_college"


# Database Connection
def get_conn():
    conn = sqlite3.connect("college_db.db")
    return conn


# Create Database Table
def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS college_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


init_db()


# Home Route
@app.route("/")
def home():
    return render_template("home.html")


# Registration Route
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return "Email and Password Required!"

        hashed_password = generate_password_hash(password)

        conn = get_conn()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO college_users (email, password) VALUES (?, ?)",
                (email, hashed_password)
            )

            conn.commit()

            return "Register Successful!"

        except sqlite3.IntegrityError:
            return "Email Already Exists!"

        finally:
            cursor.close()
            conn.close()


# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return "Email and Password Required!"

        conn = get_conn()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT * FROM college_users WHERE email = ?",
                (email,)
            )

            user = cursor.fetchone()

            if not user:
                return "Email Not Registered!"

            if check_password_hash(user[2], password):

                session["user"] = email

                return "Login Successful!"

            else:
                return "Incorrect Email or Password!"

        finally:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
