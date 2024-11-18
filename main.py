from flask import Flask, render_template, request, flash
import uuid
import sqlite3

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

@app.route("/")
def Home():
    return render_template("index.html")

@app.route("/login")
def Login():
    # Figure out later on
    return render_template("login.html")

@app.route("/signup")
def Signup():
    if request.method == "POST":
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            dob = request.form['dob']

            db = sqlite3.connect("database/student_marks.db")
            cursor = db.cursor()

            cursor.execute("SELECT * FROM Students WHERE firstname = ? AND lastname = ? AND dob = ?", 
                           (firstname, lastname, dob))
            existing_student = cursor.fetchone()

            if existing_student:
                flash(f"Student {firstname} {lastname} with DOB {dob} already exists.")
            else:
                cursor.execute("INSERT INTO Students('firstname', 'lastname', 'dob') VALUES (?, ?, ?)", 
                               (firstname, lastname, dob))
                db.commit()
                flash(f"Student {firstname} {lastname} added successfully.")

            db.close()

    return render_template("signup.html")

app.run(debug=True, port=5000)