Pylint antaa tämän raportin:

************* Module app
app.py:227:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:181:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:286:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:320:12: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:299:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:377:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:363:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:415:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)

------------------------------------------------------------------
Your code has been rated at 9.69/10 (previous run: 9.66/10, +0.04)

************* Module comments

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)

************* Module config

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)

************* Module db

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)

************* Module events
events.py:11:0: R0913: Too many arguments (8/5) (too-many-arguments)
events.py:11:0: R0917: Too many positional arguments (8/5) (too-many-positional-arguments)
events.py:97:0: R0913: Too many arguments (7/5) (too-many-arguments)
events.py:97:0: R0917: Too many positional arguments (7/5) (too-many-positional-arguments)

------------------------------------------------------------------
Your code has been rated at 9.27/10 (previous run: 9.09/10, +0.18)


Tarpeeton else:

app.py:286:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)

Koodia on selkeämpää lukea, kun else haarat ovat myös mukana.

Viittaa esim tähän pätkään update_event() funktiossa:

    if validate_event_data(title, description, date, location):
        events.edit_event(event_id, title, description, date, time, location, image_blob)
        events.update_classes(event_id, classes)

        flash("Tapahtuma päivitetty onnistuneesti.")
        return redirect("/event/" + str(event_id))
    else:
        flash("VIRHE: Tarkista syötteesi.")
        return redirect(f"/update_event/{event_id}")


Sen voisi kirjoittaa lyhemmin ilman elseä:

    if validate_event_data(title, description, date, location):
        events.edit_event(event_id, title, description, date, time, location, image_blob)
        events.update_classes(event_id, classes)

        flash("Tapahtuma päivitetty onnistuneesti.")
        return redirect("/event/" + str(event_id))

    flash("VIRHE: Tarkista syötteesi.")
    return redirect(f"/update_event/{event_id}")


Puuttuva palautusarvo:

app.py:361:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:413:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)

Liittyy tilanteisiin joissa on vain GET ja POST metodit. Esim funktiossa login() on tämän tyylinen tapaus:

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

TIKAWE kurssin mukaan periaatteessa request.method voisi olla muutakin kuin GET tai POST jolloin koodi ei palauttaisi arvoa, mutta kun on erikseen määrittänyt GET ja POST metodeiksi niin tuonlaisia tilanteita ei pysty tulemaan.


Liikaa argumentteja:

events.py:11:0: R0913: Too many arguments (8/5) (too-many-arguments)
events.py:97:0: R0913: Too many arguments (7/5) (too-many-arguments)

Hyvänä ylärajana argumenttien määrälle olisi 5 kpl, mutta tässä tapauksessa on selkeintä pitää tuo 8 tai 7, vaikka se onkin enemmän kuin suositeltu tyyli.
