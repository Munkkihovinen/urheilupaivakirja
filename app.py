from flask import Flask
from flask import render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import db
import crud
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    activities = crud.get_activities()
    return render_template("index.html", activities=activities)


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    # check if username is taken    
    sql = "SELECT id FROM users WHERE username = ?"
    taken = db.query(sql, [username])
    if taken:
        error = "VIRHE: tunnus on jo varattu"
        return render_template("register.html", error=error)

    # check if passwords match
    if password1 != password2:
        error = "VIRHE: salasanat eivät ole samat"
        return render_template("register.html", error=error)
    
    # insert user to db
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    password_hash = generate_password_hash(password1)
    db.execute(sql, [username, password_hash])
    
    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        error = False
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT password_hash FROM users WHERE username = ?"
        db_row = db.query(sql, [username])

        if not db_row:
            error = True
        else:
            password_hash = db_row[0][0]
            if check_password_hash(password_hash, password):
                session["username"] = username
                return redirect("/")
            else:
                error = True
        return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")