from flask import Flask, render_template, request, session, redirect, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import crud
import config
import sqlite3
import markupsafe

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form or "csrf_token" not in session:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
def index():
    query = request.args.get("query", "").strip()
    activities = crud.get_all_activities(search=query if query else None)
    sports = crud.get_sports()
    return render_template("index.html", activities=activities, query=query, sports=sports)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    # check any of the fields is empty
    if not username or not password1 or not password2:
        flash("VIRHE: kaikki kentät ovat pakollisia.", "error")
        return render_template("register.html", username=username)

    # check if passwords match
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat", "error")
        return render_template("register.html", username=username)

    # insert user to db
    password_hash = generate_password_hash(password1)
    try:
        crud.create_user(username, password_hash)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu", "error")
        return render_template("register.html", username=username)

    flash("Tunnus luotu. Voit nyt kirjautua sisään.", "success")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = crud.get_user_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            session["username"] = username
            session["user_id"] = user['id']
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("Virheellinen käyttäjätunnus tai salasana.", "error")
            return render_template('login.html')

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/new_activity", methods=["POST"])
def new_activity():
    require_login()
    check_csrf()

    # validate content length
    content = request.form.get("content", "").strip()
    if len(content) > 1000:
        flash("VIRHE: liian pitkä kuvaus", "error")
        return redirect("/")

    # validate duration
    duration = request.form.get("duration_in_minutes", "").strip()
    if not duration.isdigit() or int(duration) <= 0:
        flash("VIRHE: keston täytyy olla positiivinen numero.", "error")
        return redirect("/")

    activity_id = crud.add_activity(
        int(request.form["sport"]),
        int(duration),
        content,
        session["user_id"]
    )
    return redirect("/activity/" + str(activity_id))

@app.route("/activity/<int:activity_id>")
def show_activity(activity_id):
    activity = crud.get_activity(activity_id)
    comments = crud.get_comments_for_activity(activity_id)
    return render_template("activity.html", activity=activity, comments=comments)

@app.route("/remove/<int:activity_id>", methods=["GET", "POST"])
def remove_activity(activity_id):
    require_login()
    activity = crud.get_activity(activity_id)
    if activity["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove.html", activity=activity)

    if request.method == "POST":
        check_csrf()
        if "continue" in request.form:
            crud.remove_activity(activity["id"])
            flash("Aktiviteetti poistettu.", "success")
        return redirect("/")

@app.route("/activity/<int:activity_id>/edit", methods=["GET", "POST"])
def edit_activity(activity_id):
    activity = crud.get_activity(activity_id)

    require_login()
    # check user has right to edit
    if activity["user_id"] != session.get("user_id"):
        abort(403)

    if request.method == "GET":
        sports = crud.get_sports()
        return render_template("edit_activity.html", activity=activity, sports=sports)

    if request.method == "POST":
        check_csrf()
        sport = request.form.get("sport", "").strip()
        duration = request.form.get("duration_in_minutes", "").strip()
        content = request.form.get("content", "").strip()

        # validate content
        if len(content) > 1000:
            flash("VIRHE: liian pitkä kuvaus", "error")
            return redirect(f"/activity/{activity_id}/edit")

        # validate duration
        duration = request.form.get("duration_in_minutes", "").strip()
        if not duration.isdigit() or int(duration) <= 0:
            flash("VIRHE: keston täytyy olla positiivinen.", "error")
            return redirect(f"/activity/{activity_id}/edit")

        crud.update_activity(activity_id,
            sport=sport,
            duration_in_minutes=int(duration),
            content=content)
        return redirect(f"/activity/{activity_id}")

@app.route("/user/<int:user_id>")
def user_profile(user_id):
    activities = crud.get_activities_by_user_id(user_id)
    username = activities[0]["username"] if activities else None
    count = len(activities)
    total_duration = sum(a["duration_in_minutes"] for a in activities) if activities else 0
    return render_template(
        "user.html",
        activities=activities,
        username=username,
        count=count,
        total_duration=total_duration,
    )

@app.route("/activity/<int:activity_id>/comment", methods=["POST"])
def add_comment(activity_id):
    require_login()
    check_csrf()
    content = request.form.get("content", "").strip()
    if len(content) > 500:
        flash("VIRHE: liian pitkä kommentti", "error")
        return redirect(f"/activity/{activity_id}")
    if content:
        crud.add_comment(activity_id, session["user_id"], content)
    return redirect(f"/activity/{activity_id}")
