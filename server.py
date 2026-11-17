from werkzeug.security import generate_password_hash , check_password_hash

from flask import Flask, render_template, request, session , redirect, flash 

import mysql.connector

app = Flask(__name__)
app.secret_key = "my_college"

def get_conn():
    conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="1234",
            database="college_db()"
            )

def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                 id INT AUTO_INCREMENT PRIMARY KEY,
                 email VARCHAR(254) UNIQUE NOT NULL,
                 password VARCHAR(255) NOT NULL
                 )
                 """)
    conn.commit()
    cursor.close()
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

        conn = get_conn()
        cursor = conn.cursor()

        
        try:
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email,hashed_password))

            conn.commit()
            cursor.close()
            conn.close()

            return "Register Succesful!"
            
        except mysql.IntegrityError:

            cursor.close()
            conn.close()
            return "Email Already Exists!"

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = %s" , (email,))

        user = cursor.fetchone()

        if not user:
            return "Email Not Registered!"

        if check_password_hash(user[2], password):
            session['user'] = email
            return "Login Succesful!"

        else:
            return "Incorrect Email or Password!"

        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)



