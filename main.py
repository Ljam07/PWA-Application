from flask import Flask, render_template, request, flash, redirect
import uuid
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

g_username = None
g_isSignedIn = False

@app.route("/")
def Home():
    return render_template("index.html", isSignedIn=g_isSignedIn)

@app.route("/logout")
def Logout():
    global g_isSignedIn, g_username
    g_isSignedIn = False
    g_username = None
    flash("You have been logged out.")
    return redirect("/login")

@app.route("/login", methods=("GET", "POST"))
def Login():
    global g_isSignedIn, g_username
    # Figure out later on
    if request.method == "POST":
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
                g_isSignedIn = True
                g_username = existing_user[1]
                flash("Found user!")
                db.close()
                return redirect("/")

            db.close()

    return render_template("login.html", isSignedIn=g_isSignedIn)

@app.route("/signup", methods=("GET", "POST"))
def Signup():
    global g_isSignedIn, g_username
    if request.method == "POST":
            email = request.form['email']
            username = request.form['username']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            password = request.form['password']

            db = sqlite3.connect("database/users.db")
            cursor = db.cursor()

            # Check if email already exists
            cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
            email_exists = cursor.fetchone()

            # Check if username already exists
            cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
            username_exists = cursor.fetchone()


            if email_exists or username_exists:
                flash(f"Email or username already in use.")

            if not email_exists and not username_exists:
                cursor.execute("INSERT INTO Users('email', 'username', 'firstname', \
'lastname', 'password', 'permission') VALUES (?, ?, ?, ?, ?, ?)", 
                               (email, username, firstname, lastname, password, 2))
                db.commit()
                flash(f"User {firstname} {lastname} added successfully.")
                print(f"User {firstname} {lastname} added successfully.")
                db.close()
                g_isSignedIn = True
                g_username = username
                return redirect("/")


            db.close()

    return render_template("signup.html", isSignedIn=g_isSignedIn)

@app.route("/rating", methods=("GET", "POST"))
def Rating():
    if not g_isSignedIn:
        flash("You must login to use the rating system.")
        return redirect("/login")

    db = sqlite3.connect("database/games.db")
    cursor = db.cursor()

    cursor.execute("SELECT * FROM Games")
    games = cursor.fetchall()
    db.close()
    return render_template("rating.html", games=games, isSignedIn=g_isSignedIn)

@app.route("/rating/<game_id>", methods=("GET", "POST"))
def RatingSelect(game_id):
    if not g_isSignedIn:
        flash("You must login to use the rating system.")
        return redirect("/login")
    
    db = sqlite3.connect("database/games.db")
    cursor = db.cursor()

    cursor.execute("SELECT * FROM Games WHERE game_id = ?", game_id)
    game_data = cursor.fetchone()

    if game_data == None:
        flash("No game could be found.")
        return redirect("/rating")
    
    cursor.execute("SELECT * FROM Reviews WHERE game_id = ?", game_id)
    review_data = cursor.fetchall()

    if review_data:
        sum_rating = 0
        rating_count = 0
        for rows in review_data:
            sum_rating += rows[4]
            rating_count += 1

        average_rating = round(sum_rating / rating_count, 1)
    else:
        average_rating = 0

    # To make sure there isnt already a review
    cursor.execute("SELECT * FROM Reviews WHERE game_id = ? AND reviewer_name = ?", (game_id, g_username))
    existing_review = cursor.fetchone()

    hasReviewed = False
    if not existing_review == None:
        hasReviewed = True


    if request.method == "POST":
        if "remove_review" in request.form:
            # Remove the user's review
            cursor.execute(
                "DELETE FROM Reviews WHERE game_id = ? AND reviewer_name = ?", 
                (game_id, g_username)
            )
            db.commit()
            # flash("Your review has been removed.")
            return redirect(f"/rating/{game_id}")
        
        elif "add_review" in request.form:
            # Add a new review
            rating = int(request.form["rating"])
            review_text = request.form["review_text"]
            review_date = datetime.now().strftime("%Y-%m-%d")

            cursor.execute(
                "INSERT INTO Reviews (game_id, reviewer_name, review_date, rating, review_text) VALUES (?, ?, ?, ?, ?)",
                (game_id, g_username, review_date, rating, review_text)
            )
            db.commit()
            # flash("Your review has been added.")
            return redirect(f"/rating/{game_id}")


    db.close()
    return render_template("rating_select.html", game_data=game_data, isSignedIn=g_isSignedIn, 
                           review_data=review_data, average_rating=average_rating, hasReviewed=hasReviewed)


app.run(debug=True, port=5000)