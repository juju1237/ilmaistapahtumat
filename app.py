import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session, flash
import db
import config
import events
import users
import comments
import os
import secrets

con = sqlite3.connect("database.db", timeout=10)
app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form or request.form["csrf_token"] != session.get("csrf_token"):
        abort(403)

def validate_event_data(title, description, time, date, location):
    if not title or len(title) > 60:
        return False
    if not description or len(description) > 5000:
        return False
    if not location or len(location) > 100:
        return False
    return True


@app.route("/")
def index():
    all_events = events.get_events()
    return render_template("index.html", events=all_events)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    events = users.get_events(user_id)
    user_comments = users.get_user_comments(user_id)

    return render_template("show_user.html", user=user, events=events, user_comments=user_comments)


@app.route("/find_event")
def find_event():
    query = request.args.get("query")
    if query:
        results = events.find_events(query)
    else:
        query = ""
        results = []
    return render_template("find_event.html", query=query, results=results)

@app.route("/event/<int:event_id>")
def page(event_id):
    event = events.get_event(event_id)
    if not event:
        abort(404)
    classes = events.get_classes(event_id)
    comments_list = comments.get_comments(event_id)
    return render_template("show_event.html", event=event, classes=classes, comments=comments_list)


@app.route("/update_event/<int:event_id>", methods=["GET", "POST"])
def update_event(event_id):
    require_login()
    if request.method == "GET":
        event = events.get_event(event_id)
        if not event:
            abort(404)
        if event["user_id"] != session["user_id"]:
            abort(403)
        return render_template("edit_event.html", event=event)

    if request.method == "POST":
        event_id = request.form["event_id"]
        event = events.get_event(event_id)
        if not event:
            abort(404)
        if event["user_id"] != session["user_id"]:
            abort(403)
        title = request.form["title"]
        if not title or len(title) > 60:
            abort(403)
        description = request.form["description"]
        if not description or len(description) > 5000:
            abort(403)
        time = request.form["time"]
        date = request.form["date"]
        location = request.form["location"]
        if not location or len(location) > 100:
            abort(403)

        events.edit_event(event_id, title, description, date, time, location)

        return redirect("/event/" + str(event_id))

@app.route("/new_event")
def new_event():
    require_login()
    return render_template("new_event.html")

@app.route("/create_event", methods=["POST"])
def create_event():
    require_login()

    title = request.form["title"]
    description = request.form["description"]
    time = request.form["time"]
    date = request.form["date"]
    location = request.form["location"]

    if validate_event_data(title, description, time, date, location):
        classes = request.form.getlist("section")
        user_id = session["user_id"]
        events.add_event(title, description, date, time, location, user_id, classes)

        return redirect("/")
    else:
        flash("VIRHE: Tarkista syötteesi. Varmista, että kaikki kentät ovat oikein.")
        return redirect("/new_event")


@app.route("/remove_event/<int:event_id>", methods=["GET", "POST"])
def remove_event(event_id):
    require_login()
    if "user_id" not in session:
        flash("Sinun täytyy olla kirjautuneena poistaaksesi tapahtumia.")
        return redirect("/login")
    event = events.get_event(event_id)
    if not event:
        abort(404)

    if event["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_event.html", event=event)

    if request.method == "POST":
        try:
            if "remove" in request.form:
                events.remove_event(event_id)
                flash("Tapahtuma on poistettu onnistuneesti.")
                return redirect("/")
            else:
                return redirect("/event/" + str(event_id))
        except Exception as e:
            flash("Tapahtuman poistamisessa tapahtui virhe.")
            return redirect("/event/" + str(event_id))


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    return render_template("registration_success.html", username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session["csrf_token"] = secrets.token_hex(16)
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")

@app.route("/logout")
def logout():
    #require_login()
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

@app.route("/add_comment/<int:event_id>", methods=["POST"])
def add_comment(event_id):
    require_login()
    comment = request.form["comment"]
    user_id = session["user_id"]
    comments.add_comment(event_id, user_id, comment)
    return redirect("/event/" + str(event_id))
