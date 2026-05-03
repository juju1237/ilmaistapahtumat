# ilmaistapahtumat

Nykyiset toiminnot:
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään sovellukseen tapahtuma-ilmoituksia.
* Käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään ilmoituksia.
* Käyttäjä näkee sovellukseen lisätyt ilmoitukset. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät ilmoitukset.
* Käyttäjä pystyy etsimään tietokohteita hakusanalla. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä tietokohteita.
* Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokittelun (esim. sijainti, kellonaika, päivämäärä).
* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät ilmoitukset.
* Käyttäjä pystyy kommentoimaan omiin sekä muiden käyttäjien ilmoituksiin (esim. lisätietoa tapahtumasta, hype).

**Käynnistysohje:**

Näillä ohjeita voit ajaa sovelluksen omalla koneellasi. 

1. Esivaatimukset
Varmista, että koneellesi on asennettu **Python 3**.

2. Sovelluksen lataaminen
Kloonaa projekti:
$ git clone https://github.com/juju1237/ilmaistapahtumat.git

3. Mene projektikansioon linux komentotulkilla:
$ cd ilmaistapahtumat

4. Virtuaaliympäristön käynnistäminen
$ python3 -m venv venv
$ source venv/bin/activate

5. Python kirjastojen paikallinen asennus
$ pip install flask

6. Tietokannan alustus
$ sqlite3 database.db < schema.sql

7. Sovelluksen käynnistäminen:
$ flask run


Testaukset isolla tietomäärällä:

TIKAWE kurssin materiaalien mukaan ja curre chatin avulla loin seed.py tiedoston joka vastaa kurssin tyyliä mutta soveltuu sovellukseeni.
Lisäsin ajanottoon tarvittavat rivit app.py tiedostoon ja loin sivunvaihdot.

Huomioita käytettävyydestä nyt:
Etusivu:
Tapahtumien lista näkyy oikein event.id:n mukaan niin että ylhäällä on suurin event id (10000 ylimpänä ja siitä laskee alaspäin)
sivutus toimii oikein ja sivuja on yhteensä 1001
Tapahtumat:
Yksittäisen tapahtuman tietoja voi tarkastella normaalisti
tapahtumaan lähetetyt kommentit näkyvät nekin uusimmasta vanhimpaan
Tapahtuman luokat näkyvät myös oikein
Käyttäjät:
Käyttäjien profiileja sekä lähettämiä kommentteja yms voi tarkastella normaalisti
Haku:
Tapahtumien hakeminen hakusanalla toimii myös normaalisti


 En vielä ole indeksoinut tietokantaa mutta tässä on terminaaliin tulostuvat rivit:

 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
elapsed time: 0.02 s
127.0.0.1 - - [28/Apr/2026 16:13:39] "GET / HTTP/1.1" 200 -
elapsed time: 0.01 s
127.0.0.1 - - [28/Apr/2026 16:13:39] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.07 s
127.0.0.1 - - [28/Apr/2026 16:13:45] "GET /event/9991 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [28/Apr/2026 16:13:45] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.14 s
127.0.0.1 - - [28/Apr/2026 16:13:48] "GET /user/532 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [28/Apr/2026 16:13:48] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.05 s
127.0.0.1 - - [28/Apr/2026 16:13:54] "GET /event/6023 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [28/Apr/2026 16:13:54] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [28/Apr/2026 16:13:55] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [28/Apr/2026 16:13:55] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.05 s
127.0.0.1 - - [28/Apr/2026 16:13:56] "GET /event/9999 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [28/Apr/2026 16:13:56] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [28/Apr/2026 16:13:58] "GET /new_event HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [28/Apr/2026 16:13:58] "GET /static/main.css HTTP/1.1" 304 

Siis sovellus toimii hyvin ja nopeasti vaikka tietomäärä on erittäin suuri.


Seuraavaksi lisäsin indeksit schema.sql:ään koodilla


CREATE INDEX IF NOT EXISTS idx_events_user_id ON events (user_id);
CREATE INDEX IF NOT EXISTS idx_events_date ON events (date);
CREATE INDEX IF NOT EXISTS idx_events_id ON events (id);
CREATE INDEX IF NOT EXISTS idx_event_classes_event_id ON event_classes (event_id);
CREATE INDEX IF NOT EXISTS idx_comments_event_id ON comments (event_id);
CREATE INDEX IF NOT EXISTS idx_comments_user_id ON comments (user_id);
CREATE INDEX IF NOT EXISTS idx_users_id ON users (id);
CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);


Indeksien lisäämisen jälkeen ajat näyttävät seuraavalta:
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
elapsed time: 0.02 s
127.0.0.1 - - [28/Apr/2026 16:35:14] "GET / HTTP/1.1" 200 -
elapsed time: 0.01 s
127.0.0.1 - - [28/Apr/2026 16:35:14] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [28/Apr/2026 16:35:16] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [28/Apr/2026 16:35:16] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [28/Apr/2026 16:35:17] "GET /event/10000 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [28/Apr/2026 16:35:17] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [28/Apr/2026 16:35:19] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [28/Apr/2026 16:35:19] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [28/Apr/2026 16:35:22] "GET /event/9993 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [28/Apr/2026 16:35:22] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.07 s
127.0.0.1 - - [28/Apr/2026 16:35:24] "GET /user/650 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [28/Apr/2026 16:35:24] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [28/Apr/2026 16:35:25] "GET /event/2072 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [28/Apr/2026 16:35:25] "GET /static/main.css HTTP/1.1" 304 -

Ajat siis hieman lyhenivät vielä mutta ero ei ole suuri. Tämä luultavasti johtuu siitä että lisäsin sivunvaihdot suoraan enkä testannut aikoja ja tehokkuutta ilman sivuttamista.

Seuraavaksi poistin indeksit schema.sql:stä ja poistin database.db:n, jonka jälkeen lisäsin scheman takaisin database.db. Tämän jälkeen muutin testidataa näin:

user_count = 10**6
event_count = 10**6
class_count = 10**6
comment_count = 10**6

Sitten ajat näyttivät seuraavilta kun testailin käydä tapahtumailmoituksissa ja lähettää kommentteja ja käydä käyttäjän profiilissa:

elapsed time: 0.17 s
127.0.0.1 - - [03/May/2026 11:47:16] "GET /event/1000000 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [03/May/2026 11:47:16] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.22 s
127.0.0.1 - - [03/May/2026 11:47:19] "GET /user/165143 HTTP/1.1" 200 -
elapsed time: 0.19 s
127.0.0.1 - - [03/May/2026 11:47:19] "GET /user/165143 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [03/May/2026 11:47:19] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.17 s
127.0.0.1 - - [03/May/2026 11:47:25] "GET /event/767957 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [03/May/2026 11:47:25] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.05 s
127.0.0.1 - - [03/May/2026 11:47:29] "POST /add_comment/767957 HTTP/1.1" 302 -
elapsed time: 0.16 s
127.0.0.1 - - [03/May/2026 11:47:30] "GET /event/767957 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [03/May/2026 11:47:30] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.06 s
127.0.0.1 - - [03/May/2026 11:47:35] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [03/May/2026 11:47:35] "GET /static/main.css HTTP/1.1" 304 -

Sovellus toimii yhä tehokkaasti vaikka datan määrä on erittäin suuri. Tapahtumailmoituksen tarkastelu vaikuttaa vievän eniten aikaa.

Tämän jälkeen lisäsin indeksit uudestaan ja ajat näyttävät tältä

elapsed time: 0.98 s
127.0.0.1 - - [03/May/2026 12:05:08] "GET /page/5 HTTP/1.1" 200 -
elapsed time: 0.05 s
127.0.0.1 - - [03/May/2026 12:05:08] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.05 s
127.0.0.1 - - [03/May/2026 12:05:12] "GET /event/999959 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [03/May/2026 12:05:12] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.05 s
127.0.0.1 - - [03/May/2026 12:05:15] "GET /user/454210 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [03/May/2026 12:05:15] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.03 s
127.0.0.1 - - [03/May/2026 12:05:18] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [03/May/2026 12:05:18] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.02 s
127.0.0.1 - - [03/May/2026 12:05:20] "GET /page/2 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [03/May/2026 12:05:20] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.05 s
127.0.0.1 - - [03/May/2026 12:05:24] "GET /event/999985 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [03/May/2026 12:05:24] "GET /static/main.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [03/May/2026 12:05:29] "GET /logout HTTP/1.1" 302 -
elapsed time: 0.01 s
127.0.0.1 - - [03/May/2026 12:05:29] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [03/May/2026 12:05:30] "GET /static/main.css HTTP/1.1" 304 

Nyt vain sivun lataaminen vei melkein sekunnin mutta kaikki muut ajat ovat pieniä.