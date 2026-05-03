"""
app.py: A Flask-based application for event management.
Contains routes and actions for users and events.
"""
import math
import time


import sqlite3
import secrets
from datetime import datetime

from flask import Flask, abort, make_response, redirect, render_template, request, session, flash, g
import markupsafe

import config
import events
import users
import comments


app = Flask(__name__)
app.secret_key = config.SECRET_KEY


@app.before_request
def before_request():
    """
    Starting time for efficiency test
    """
    g.start_time = time.time()

@app.after_request
def after_request(response):
    """
    Ending time for efficiency test
    """
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response



def require_login():
    """
    Checks if the user is logged in. If not, returns an HTTP 403 error.
    """
    if "user_id" not in session:
        abort(403)

def check_csrf():
    """
    Checks for csrf. If it doesn't exist, returns an HTTP 403 error.
    """
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session.get("csrf_token"):
        abort(403)


def validate_event_data(title, description, date, location):
    """
    Checks if event data is validate. If not, returns False and user has to try again.
    """
    if not title or len(title) > 60:
        return False
    if not description or len(description) > 5000:
        return False
    if not location or len(location) > 100:
        return False

    try:
        event_date = datetime.strptime(date, "%d.%m.%Y")
        if event_date < datetime.now():
            return False
    except ValueError:
        return False

    return True


def filled_event(title, description, date, event_time, location):
    """
    Fills event data from last insert. Returns new_evemt HTML.
    """
    filled = {
        "title": title,
        "description": description,
        "date": date,
        "time": event_time,
        "location": location
    }
    return render_template("new_event.html", filled=filled)


@app.template_filter()
def show_lines(content):
    """
    Allows line brekaks for inputs in event descriptions and comments.
    """
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)


@app.route("/")
@app.route("/page/<int:page>")
def index(page=1):
    """
    Displays the event list with pagination.

    Args:
        page (int): Current page number. Defaults to 1.

    Returns:
        Rendered HTML page with events for the current page.
    """
    page_size = 10
    event_count = events.event_count()
    page_count = math.ceil(event_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/page/1")
    if page > page_count:
        return redirect(f"/page/{page_count}")

    offset = (page - 1) * page_size
    current_events = events.get_events_with_pagination(offset, page_size)

    return render_template(
        "index.html",
        page=page,
        page_count=page_count,
        events=current_events
    )

@app.route("/user/<int:user_id>")
def show_user(user_id):
    """
    Show user information
    """
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_events = users.get_events(user_id)
    user_comments = users.get_user_comments(user_id)

    return render_template("show_user.html",
                           user=user, events=user_events, user_comments=user_comments)


@app.route("/find_event")
def find_event():
    """
    Function for finding events. Returns find_event html.
    """

    query = request.args.get("query")
    if query:
        results = events.find_events(query)
    else:
        query = ""
        results = []
    return render_template("find_event.html", query=query, results=results)

@app.route("/event/<int:event_id>")
def show_event(event_id):
    """
    Function for showing event page
    """
    event = events.get_event(event_id)
    if not event:
        abort(404)
    classes = events.get_classes(event_id)
    comments_list = comments.get_comments(event_id)
    return render_template("show_event.html", event=event, classes=classes, comments=comments_list)


@app.route("/update_event/<int:event_id>", methods=["GET", "POST"])
def update_event(event_id):
    """
    Function for updating event
    """
    require_login()
    event = events.get_event(event_id)
    if request.method == "GET":
        classes = events.get_classes(event_id)
        if not event:
            abort(404)
        if event["user_id"] != session["user_id"]:
            abort(403)
        return render_template("edit_event.html", event=event, classes=classes)

    check_csrf()
    if request.method == "POST":
        event = events.get_event(event_id)
        if not event:
            abort(404)
        if event["user_id"] != session["user_id"]:
            abort(403)
        title = request.form["title"]
        description = request.form["description"]
        event_time = request.form["time"]
        date_raw = request.form["date"]
        location = request.form["location"]
        classes = request.form.getlist("section")
        image = request.files.get("image")
        image_blob = None

        if image and image.filename != "":
            if not image.filename.endswith(".jpg"):
                flash("VIRHE: Väärä tiedostotyyppi. Vain .jpg-tiedostot ovat sallittuja.")
                return redirect(f"/update_event/{event_id}")

            image_blob = image.read()
            if len(image_blob) > 100 * 1024:  # 100 KB max size
                flash("VIRHE: Liian suuri kuva. Maksimikoko on 100 KB.")
                return redirect(f"/update_event/{event_id}")

        try:
            date = datetime.strptime(date_raw, "%Y-%m-%d").strftime("%d.%m.%Y")
        except ValueError:
            flash("VIRHE: Päivämäärä ei ole oikeassa muodossa.")
            return redirect(f"/update_event/{event_id}")

        if validate_event_data(title, description, date, location):
            events.edit_event(event_id, title, description, date, event_time, location, image_blob)
            events.update_classes(event_id, classes)

            flash("Tapahtuma päivitetty onnistuneesti.")
            return redirect("/event/" + str(event_id))
        else:
            flash("VIRHE: Tarkista syötteesi.")
            return redirect(f"/update_event/{event_id}")

@app.route("/new_event")
def new_event():
    """
    Function for filling new_event if error
    """
    require_login()
    empty = {
        "title": "",
        "description": "",
        "date": "",
        "event_time": "",
        "location": ""
    }
    return render_template("new_event.html", filled=empty)


@app.route("/create_event", methods=["POST"])
def create_event():
    """
    Function for creating new event
    """
    require_login()
    check_csrf()

    title = request.form["title"]
    description = request.form["description"]
    event_time = request.form["time"]
    date_raw = request.form["date"]
    location = request.form["location"]
    image = request.files.get("image")

    try:
        date = datetime.strptime(date_raw, "%Y-%m-%d").strftime("%d.%m.%Y")
    except ValueError:
        flash("VIRHE: Päivämäärä ei ole oikeassa muodossa.")
        return filled_event(title, description, date_raw, event_time, location)

    image_blob = None
    if image and image.filename != "":
        if not image.filename.endswith(".jpg"):
            flash("VIRHE: Väärä tiedostotyyppi. Vain .jpg-tiedostot ovat sallittuja.")
            return filled_event(title, description, date, event_time, location)

        image_blob = image.read()
        if len(image_blob) > 100 * 1024:  # 100 KB max size
            flash("VIRHE: Liian suuri kuva. Maksimikoko on 100 KB.")
            return filled_event(title, description, date_raw, event_time, location)


    if validate_event_data(title, description, date, location):
        classes = request.form.getlist("section")
        user_id = session["user_id"]
        events.add_event(title, description, date_raw, event_time,
                         location, user_id, classes, image_blob)

        return redirect("/")
    else:
        flash("VIRHE: Tarkista syötteesi. Varmista, että kaikki kentät ovat oikein.")
        return filled_event(title, description, date_raw, event_time, location)


@app.route("/remove_event/<int:event_id>", methods=["GET", "POST"])
def remove_event(event_id):
    """
    Function for removing event
    """
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

    check_csrf()
    if request.method == "POST":
        try:
            if "remove" in request.form:
                events.remove_event(event_id)
                flash("Tapahtuma on poistettu onnistuneesti.")
                return redirect("/")
            else:
                return redirect("/event/" + str(event_id))
        except sqlite3.Error as e:
            print(f"debug: tapahtui virhe {e}")
            flash("Tapahtuman poistamisessa tapahtui virhe.")
            return redirect("/event/" + str(event_id))


@app.route("/register")
def register():
    """
    Function for registering new account if method is GET
    """
    return render_template("register.html", filled={})

@app.route("/create", methods=["POST"])
def create():
    """
    Function for registering new account if method is POST
    """
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        filled = {"username": username}
        return render_template("register.html", filled=filled)

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("Virhe tietokannan käsittelyssä.")
        filled = {"username": username}
        return render_template("register.html", filled=filled)

    return render_template("registration_success.html", username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Function for logging in
    """
    if request.method == "GET":
        next_page = request.args.get("next", request.referrer or "/")
        return render_template("login.html", filled={}, next_page=next_page)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        next_page = request.form.get("next_page", "/")

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect(next_page)
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            filled = {"username": username}
            return render_template("login.html", filled=filled, next_page=next_page)

@app.route("/logout")
def logout():
    """
    Function for logging out
    """
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

@app.route("/add_comment/<int:event_id>", methods=["POST"])
def add_comment(event_id):
    """
    Function for adding comment to event
    """

    if "user_id" not in session:
        flash("Sinun täytyy olla kirjautuneena kommentoidaksesi tapahtumia.")
        return redirect(f"/login?next=/event/{event_id}")

    require_login()
    check_csrf()
    comment = request.form["comment"]
    user_id = session["user_id"]
    comments.add_comment(event_id, user_id, comment)
    return redirect("/event/" + str(event_id))

@app.route("/add_event_image/<int:event_id>", methods=["GET", "POST"])
def add_event_image(event_id):
    """
    Function for adding image to event
    """

    require_login()

    event = events.get_event(event_id)
    if not event:
        abort(404)
    if event["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("add_event_image.html", event=event)

    if request.method == "POST":
        file = request.files["image"]
        if not file or file.filename.endswith(".jpg"):
            flash("VIRHE: väärä tiedostomuoto. Vain .jpg-tiedostot ovat sallittuja.")
            return redirect(f"/add_event_image/{event_id}")

        image_blob = file.read()
        if len(image_blob) > 100 * 1024:  # 100 KB max size
            flash("VIRHE: liian suuri kuva. Maksimikoko on 100 KB.")
            return redirect(f"/add_event_image/{event_id}")

        events.update_image(event_id, image_blob)
        flash("Kuva lisätty onnistuneesti!")
        return redirect("/event/" + str(event_id))

@app.route("/image/<int:event_id>")
def show_event_image(event_id):
    """
    Function for showing image in event post
    """

    image = events.get_image(event_id)
    if not image:
        abort(404)

    response = make_response(image)
    response.headers.set("Content-Type", "image/jpeg")
    return response
