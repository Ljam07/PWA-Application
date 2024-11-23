from flask import Flask, render_template, request, flash
import uuid
import sqlite3

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
    return Login()

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
                return Home()

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
                return Home()


            db.close()

    return render_template("signup.html", isSignedIn=g_isSignedIn)

@app.route("/rating", methods=("GET", "POST"))
def Rating():
    if not g_isSignedIn:
        flash("You must login to use the rating system.")
        return Login()

    db = sqlite3.connect("database/games.db")
    cursor = db.cursor()


    cursor.execute("SELECT * FROM Games")
    games = cursor.fetchall()
    for game in games:
        print(f"{game[1]}")
    db.close()
    return render_template("rating.html", games=games, isSignedIn=g_isSignedIn)

@app.route("/rating/<game_id>", methods=("GET", "POST"))
def RatingSelect(game_id):
    if not g_isSignedIn:
        flash("You must login to use the rating system.")
        return Login()
    
    db = sqlite3.connect("database/games.db")
    cursor = db.cursor()

    cursor.execute("SELECT * FROM Games WHERE game_id = ?", game_id)
    data = cursor.fetchone()

    if data == None:
        flash("No game could be found.")
        return Rating()
    
    title = data[1]

    #This needs to be replaced
    """
    if request.method == "POST":
            game_id = request.form['game_id']
            rating = float(request.form['rating'])
            cursor.execute("UPDATE Games SET rating = ? WHERE game_id = ?", (rating, game_id))
            db.commit()
            flash("Rating submitted successfully.")
    """

    db.close()
    return render_template("rating_select.html", title=title, isSignedIn=g_isSignedIn)


app.run(debug=True, port=5000)