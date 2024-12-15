from flask import Flask, render_template, request,\
flash, redirect, session, url_for, make_response, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid # Custom secret key <- note as custom technique
import sqlite3
from datetime import datetime
import os

#########################
##########SETUP##########
#########################
app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() \
        in ALLOWED_EXTENSIONS

#########################
#######Functions#########
#########################
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
    # if not session.get('isSignedIn', False):
    #     flash("You must logged in to use the rating system.")
    #     return redirect("/login")

    db = sqlite3.connect("database/games.db")
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Games")
        games = cursor.fetchall()
    finally:
        db.close()

    return render_template("rating.html", games=games, isSignedIn=session.get('isSignedIn'))

@app.route("/rating/<game_id>", methods=("GET", "POST"))
def RatingSelect(game_id):
    db = sqlite3.connect("database/games.db")
    try:
        cursor = db.cursor()

        # Fetch game data
        cursor.execute("SELECT * FROM Games WHERE game_id = ?", (game_id,))
        game_data = cursor.fetchone()

        if game_data is None:
            flash("No game could be found.")
            return redirect("/rating")

        # Handle sorting option
        sort_order = request.args.get('sort_order', 'newest')

        if sort_order == 'highest':
            cursor.execute(
                "SELECT * FROM Reviews WHERE game_id = ? ORDER BY rating DESC, review_date DESC",
                (game_id,)
            )
        elif sort_order == 'lowest':
            cursor.execute(
                "SELECT * FROM Reviews WHERE game_id = ? ORDER BY rating ASC, review_date DESC",
                (game_id,)
            )
        else:  # Default is 'newest'
            cursor.execute(
                "SELECT * FROM Reviews WHERE game_id = ? ORDER BY review_date DESC",
                (game_id,)
            )

        review_data = cursor.fetchall()

        # Calculate average rating
        if review_data:
            sum_rating = sum(row[4] for row in review_data)
            average_rating = round(sum_rating / len(review_data), 1)
        else:
            average_rating = 0

        # Check if user has already reviewed
        cursor.execute(
            "SELECT * FROM Reviews WHERE game_id = ? AND reviewer_name = ?",
            (game_id, session.get('username', ''))
        )
        existing_review = cursor.fetchone()

        hasReviewed = existing_review is not None

        if request.method == "POST":
            if "remove_review" in request.form:
                cursor.execute(
                    "DELETE FROM Reviews WHERE game_id = ? AND reviewer_name = ?",
                    (game_id, session.get('username', ''))
                )
                db.commit()
                flash("Your review has been removed.")
                return redirect(f"/rating/{game_id}")

            elif "add_review" in request.form:
                try:
                    rating = int(request.form["rating"])
                    review_text = request.form["review_text"]
                    review_date = datetime.now().strftime("%Y-%m-%d")

                    cursor.execute(
                        "INSERT INTO Reviews (game_id, reviewer_name, review_date, rating, review_text) VALUES (?, ?, ?, ?, ?)",
                        (game_id, session.get('username', ''), review_date, rating, review_text)
                    )
                    db.commit()
                    flash("Your review has been added.")
                    return redirect(f"/rating/{game_id}")
                except ValueError:
                    flash("Invalid rating value. Please try again.")
    except sqlite3.Error as e:
        flash(f"Database error: {e}")
        return redirect("/rating")
    finally:
        db.close()

    return render_template(
        "rating_select.html",
        game_data=game_data,
        isSignedIn=session.get('isSignedIn', False),
        review_data=review_data,
        average_rating=average_rating,
        hasReviewed=hasReviewed,
        sort_order=sort_order
    )



@app.route("/upload", methods=['GET', 'POST'])
def Upload():
    print("Upload")
    if not session.get('isSignedIn', False):
        flash("You must log in to upload content.")
        return redirect(url_for('Login'))

    if request.method == 'POST':
        print("POST")        
        title = request.form['title']
        #Check for title existing
        try:
            db = sqlite3.connect("database/games.db")
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Games WHERE title = ?", (title,))
            existing_game = cursor.fetchone()
            if existing_game:
                flash("A game with this title already exists.", 'error')
                return redirect(url_for('Upload'))
        except Exception as e:
            print(f"When connecting to db: \n{e}")
            # Check if the game title already exists

        if 'image' not in request.files:
            flash("No image uploaded", 'error')
            return redirect(url_for('Rating'))

        file = request.files['image']
        if file.filename == '':
            flash("No image selected", 'error')
            return redirect(url_for('Rating'))

        if file and allowed_file(file.filename):
            filename = secure_filename(f"UPLOAD_{datetime.now().timestamp()}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            


            try:
                # Proceed with the insertion if no duplicate title
                cursor.execute('''
                    INSERT INTO Games (title, description, image_path, release_date, developer, publisher)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    title,
                    request.form['description'],
                    f"../uploads/{filename}",
                    request.form['release_date'],
                    request.form['developer'],
                    request.form['publisher']
                ))
                db.commit()
                flash("Entry added successfully!", 'success')
            except Exception as e:
                flash(f"Database error: {e}", 'error')
            finally:
                db.close()
        else:
            flash("Invalid file type", 'error')

    return render_template("upload.html")

@app.route('/offline')
def offline():
    response = make_response(render_template('offline.html'))
    return response
 
@app.route('/service-worker.js')
def sw():
    response = make_response(
        send_from_directory(os.path.join(app.root_path, 'static/js'),
        'service-worker.js')
    )
    return response
 
@app.route('/manifest.json')
def manifest():
    response = make_response(
        send_from_directory(os.path.join(app.root_path, 'static'), 'manifest.json')
    )
    return response


if __name__ == "__main__":
    app.run(debug=True, port=5000)
