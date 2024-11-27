from flask import Flask, render_template, request, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex


@app.route("/")
def Home():
    session['isSignedIn'] = session.get('isSignedIn', False)
    return render_template("index.html", isSignedIn=session['isSignedIn'])


@app.route("/logout")
def Logout():
    session.clear()
    flash("You have been logged out.")
    return redirect("/login")


@app.route("/login", methods=("GET", "POST"))
def Login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        db = sqlite3.connect("database/users.db")
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                stored_password_hash = existing_user[4]
                if check_password_hash(stored_password_hash, password):
                    session['isSignedIn'] = True
                    session['username'] = existing_user[1]
                    flash("Logged in successfully!")
                    return redirect("/")
                else:
                    flash("Invalid email or password.")
            else:
                flash("Invalid email or password.")
        finally:
            db.close()

    return render_template("login.html", isSignedIn=session.get('isSignedIn', False))



@app.route("/signup", methods=("GET", "POST"))
def Signup():
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']

        db = sqlite3.connect("database/users.db")
        try:
            cursor = db.cursor()

            # Check if email already exists
            cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
            email_exists = cursor.fetchone()

            # Check if username already exists
            cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
            username_exists = cursor.fetchone()

            if email_exists or username_exists:
                flash("Email or username already in use.")
            else:
                cursor.execute(
                    "INSERT INTO Users (email, username, firstname, lastname, password, permission) VALUES (?, ?, ?, ?, ?, ?)",
                    (email, username, firstname, lastname, generate_password_hash(password), 2)
                )
                db.commit()
                flash(f"User {firstname} {lastname} added successfully.")
                session['isSignedIn'] = True
                session['username'] = username
                return redirect("/")
        finally:
            db.close()

    return render_template("signup.html", isSignedIn=session.get('isSignedIn', False))


@app.route("/rating", methods=("GET", "POST"))
def Rating():
    if not session.get('isSignedIn', False):
        flash("You must log in to use the rating system.")
        return redirect("/login")

    db = sqlite3.connect("database/games.db")
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Games")
        games = cursor.fetchall()
    finally:
        db.close()

    return render_template("rating.html", games=games, isSignedIn=session.get('isSignedIn', False))


@app.route("/rating/<game_id>", methods=("GET", "POST"))
def RatingSelect(game_id):
    if not session.get('isSignedIn', False):
        flash("You must log in to use the rating system.")
        return redirect("/login")

    db = sqlite3.connect("database/games.db")
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Games WHERE game_id = ?", (game_id,))
        game_data = cursor.fetchone()

        if game_data is None:
            flash("No game could be found.")
            return redirect("/rating")

        cursor.execute("SELECT * FROM Reviews WHERE game_id = ?", (game_id,))
        review_data = cursor.fetchall()

        # Calculate average rating
        if review_data:
            sum_rating = sum(row[4] for row in review_data) 
            average_rating = round(sum_rating / len(review_data), 1)
        else:
            average_rating = 0

        # Check if user already reviewed
        cursor.execute(
            "SELECT * FROM Reviews WHERE game_id = ? AND reviewer_name = ?",
            (game_id, session['username'])
        )
        existing_review = cursor.fetchone()

        hasReviewed = existing_review is not None

        if request.method == "POST":
            if "remove_review" in request.form:
                # Remove the user's review
                cursor.execute(
                    "DELETE FROM Reviews WHERE game_id = ? AND reviewer_name = ?",
                    (game_id, session['username'])
                )
                db.commit()
                flash("Your review has been removed.")
                return redirect(f"/rating/{game_id}")

            elif "add_review" in request.form:
                # Add a new review
                rating = int(request.form["rating"])
                review_text = request.form["review_text"]
                review_date = datetime.now().strftime("%Y-%m-%d")

                cursor.execute(
                    "INSERT INTO Reviews (game_id, reviewer_name, review_date, rating, review_text) VALUES (?, ?, ?, ?, ?)",
                    (game_id, session['username'], review_date, rating, review_text)
                )
                db.commit()
                flash("Your review has been added.")
                return redirect(f"/rating/{game_id}")
    finally:
        db.close()

    return render_template(
        "rating_select.html",
        game_data=game_data,
        isSignedIn=session.get('isSignedIn', False),
        review_data=review_data,
        average_rating=average_rating,
        hasReviewed=hasReviewed
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
