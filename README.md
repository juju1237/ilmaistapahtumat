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
2. 
Varmista, että koneellesi on asennettu **Python 3**.

3. Sovelluksen lataaminen
Kloonaa projekti:

		$ git clone https://github.com/juju1237/ilmaistapahtumat.git

4. Mene projektikansioon linux komentotulkilla:

		$ cd ilmaistapahtumat

5. Virtuaaliympäristön käynnistäminen
	
		$ python3 -m venv venv
		$ source venv/bin/activate

6. Python kirjastojen paikallinen asennus
	
		$ pip install flask

7. Tietokannan alustus
	
		$ sqlite3 database.db < schema.sql

8. Sovelluksen käynnistäminen:
	
		$ flask run


Testaukset suurella tietomäärällä:

TIKAWE kurssin materiaalien mukaan ja curre chatin avulla loin seed.py tiedoston joka vastaa kurssin tyyliä mutta soveltuu sovellukseeni.
Lisäsin ajanottoon tarvittavat rivit app.py tiedostoon ja loin sivunvaihdot.

Huomioita käytettävyydestä nyt:
Etusivu:
* Tapahtumien lista näkyy oikein event.id:n mukaan niin että ylhäällä on suurin event id (10000 ylimpänä ja siitä laskee alaspäin)
* sivutus toimii oikein ja sivuja on yhteensä 1001
Tapahtumat:
* Yksittäisen tapahtuman tietoja voi tarkastella normaalisti
* tapahtumaan lähetetyt kommentit näkyvät nekin uusimmasta vanhimpaan
* Tapahtuman luokat näkyvät myös oikein
Käyttäjät:
* Käyttäjien profiileja sekä lähettämiä kommentteja yms voi tarkastella normaalisti
Haku:
* Tapahtumien hakeminen hakusanalla toimii myös normaalisti


 En vielä ole indeksoinut tietokantaa mutta tässä on terminaaliin tulostuvat rivit:
	
	Running on http://127.0.0.1:5000
	
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
	
	127.0.0.1 - - [28/Apr/2026 16:13:58] "GET /static/main.css HTTP/1.1" 304 -
	
	elapsed time: 0.06 s
	
	127.0.0.1 - - [28/Apr/2026 16:14:08] "POST /create_event HTTP/1.1" 302 -
	
	elapsed time: 0.0 s
	
	127.0.0.1 - - [28/Apr/2026 16:14:08] "GET / HTTP/1.1" 200 -
	
	elapsed time: 0.0 s
	
	127.0.0.1 - - [28/Apr/2026 16:14:08] "GET /static/main.css HTTP/1.1" 304 -
	
	elapsed time: 0.0 s
	
	127.0.0.1 - - [28/Apr/2026 16:14:18] "GET /logout HTTP/1.1" 302 -
	
	elapsed time: 0.0 s



Siis sovellus toimii hyvin ja nopeasti vaikka tietomäärä on erittäin suuri.


Seuraavaksi lisäsin indeksit suoraan sovellukseen koodilla


	def ensure_indexes():

				"""
				Checks if there are indexes in database. If not, creates them.
				"""
				db = sqlite3.connect("database.db")
				db.execute("CREATE INDEX IF NOT EXISTS idx_events_user_id ON events (user_id);")
				db.execute("CREATE INDEX IF NOT EXISTS idx_events_date ON events (date);")
				db.execute("CREATE INDEX IF NOT EXISTS idx_events_id ON events (id);")
				db.execute("CREATE INDEX IF NOT EXISTS idx_event_classes_event_id ON event_classes (event_id);")
				db.execute("CREATE INDEX IF NOT EXISTS idx_comments_event_id ON comments (event_id);")
				db.execute("CREATE INDEX IF NOT EXISTS idx_comments_user_id ON comments (user_id);")
				db.execute("CREATE INDEX IF NOT EXISTS idx_users_id ON users (id);")
				db.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users (username);")
				db.commit()
				db.close()



	ensure_indexes()


Indeksien lisäämisen jälkeen ajat näyttävät seuraavalta:

	Running on http://127.0.0.1:5000
	
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
	
	elapsed time: 0.01 s
	
	127.0.0.1 - - [28/Apr/2026 16:35:26] "GET /user/650 HTTP/1.1" 200 -
	
	elapsed time: 0.0 s
	
	127.0.0.1 - - [28/Apr/2026 16:35:26] "GET /static/main.css HTTP/1.1" 304 -
	
	elapsed time: 0.0 s
	
	127.0.0.1 - - [28/Apr/2026 16:35:27] "GET /event/8472 HTTP/1.1" 200 -
	
	elapsed time: 0.0 s

Ajat siis hieman lyhenivät vielä mutta ero ei ole suuri. Tämä luultavasti johtuu siitä että lisäsin sivunvaihdot suoraan enkä testannut aikoja ja tehokkuutta ilman sivuttamista.

