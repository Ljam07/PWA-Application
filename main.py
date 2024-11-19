from flask import Flask, render_template, request, flash
import uuid
import sqlite3

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

username = None
isSignedIn = False

@app.route("/")
def Home():
    return render_template("index.html")

@app.route("/login", methods=("GET", "POST"))
def Login():
    global isSignedIn, username
    # Figure out later on
    if request.method == "POST":
            print("Completed this part")
            email = request.form['email']
            password = request.form['password']


            db = sqlite3.connect("database/users.db")
            cursor = db.cursor()

            cursor.execute("SELECT * FROM Users WHERE email = ? AND password = ?", 
                           (email, password))
            existing_user = cursor.fetchone()

            if not existing_user:
                flash("Email or password does not exist.")
            else:
                isSignedIn = True
                username = existing_user[1]
                flash("Found user!")

            db.close()

    return render_template("login.html")

@app.route("/signup", methods=("GET", "POST"))
def Signup():
    if request.method == "POST":
            email = request.form['email']
            username = request.form['username']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            password = request.form['password']

            db = sqlite3.connect("database/users.db")
            cursor = db.cursor()

            cursor.execute("SELECT * FROM Users WHERE email = ? AND username = ?", 
                           (email, username))
            existing_user = cursor.fetchone()

            if existing_user:
                if existing_user[0]:
                    flash(f"Email already in use.")
                if existing_user[1]:
                    flash(f"Username already in use.")
            else:
                cursor.execute("INSERT INTO Users('email', 'username', 'firstname', \
'lastname', 'password', 'permission') VALUES (?, ?, ?, ?, ?, ?)", 
                               (email, username, firstname, lastname, password, 2))
                db.commit()
                flash(f"User {firstname} {lastname} added successfully.")
                print(f"User {firstname} {lastname} added successfully.")

            db.close()

    return render_template("signup.html")

app.run(debug=True, port=5000)