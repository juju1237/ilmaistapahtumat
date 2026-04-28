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
