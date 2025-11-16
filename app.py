from flask import Flask
from flask import render_template, request, session, redirect, abort
from werkzeug.security import generate_password_hash, check_password_hash
import db
import crud
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    query = request.args.get("query", "").strip()
    activities = crud.get_activities(search=query if query else None)
    return render_template("index.html", activities=activities, query=query)

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
        
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        db_row = db.query(sql, [username])

        if not db_row:
            error = True
        else:
            user_id = db_row[0][0]
            password_hash = db_row[0][1]
            if check_password_hash(password_hash, password):
                session["username"] = username
                session["user_id"] = user_id
                return redirect("/")
            else:
                error = True
        return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/new_activity", methods=["POST"])
def new_activity():
    activity_id = crud.add_activity(request.form["sport"], request.form["duration_in_minutes"], request.form["content"], session["user_id"])
    return redirect("/activity/" + str(activity_id))

@app.route("/activity/<int:activity_id>")
def show_activity(activity_id):
    activity = crud.get_activity(activity_id)
    return render_template("activity.html", activity=activity)

@app.route("/remove/<int:activity_id>")
def remove_activity(activity_id):
    db.execute("DELETE FROM activities WHERE id = ?", [activity_id])
    return redirect("/")

@app.route("/activity/<int:activity_id>/edit", methods=["GET", "POST"])
def edit_activity(activity_id):
    activity = crud.get_activity(activity_id)

    # check user has right to edit
    if activity["user_id"] != session.get("user_id"):
        abort(403)

    if request.method == "GET":
        return render_template("edit_activity.html", activity=activity)

    sport = request.form.get("sport", "").strip()
    duration = request.form.get("duration_in_minutes", "").strip()
    content = request.form.get("content", "").strip()

    crud.update_activity(activity_id, sport=sport, duration_in_minutes=duration, content=content)
    return redirect(f"/activity/{activity_id}")