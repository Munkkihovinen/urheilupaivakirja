# urheilupaivakirja

- Sovelluksessa käyttäjät pystyvät jakamaan urheilusuorituksiaan. Suorituksessa on laji, päivämäärä, ajallinen kesto minuuteissa, lajista riippuen mahdollisesti matka, sekä vapaa tekstikenttä, jossa voi antaa kuvauksen suorituksesta. Suoritukselle valittava laji ei ole vapaa tekstikenttä vaan valitaan sovelluksen tarjoamalta listalta.
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään urheilusuorituksia ja muokkaamaan ja poistamaan niitä.
- Käyttäjä näkee sovelluksessa omat ja muiden lisäämät suoritukset.
- Käyttäjä pystyy etsimään suorituksia käyttäjänimen ja lajin perusteella ja järjestämään hakutulokset keston, matkan tai päivämäärän mukaan.
- Käyttäjäsivu näyttää lajikohtaisesti suorituskerrat, yhteenlasketun ajan ja matkan, sekä listan kaikista suorituksista.
- Käyttäjä pystyy lisäämään kommentteja omiin ja muiden suorituksiin. Suoritussivulla näytetään kaikki kommentit.

- Pääasiallinen tietokohde on urheilusuoritus ja toissijainen tietokohde on kommentti.

# Projektin käynnistäminen ja testaaminen

- Asenna sqlite3 ja python
- Asenna Flask: `pip install flask`
- Luo tietokanta `sqlite3 database.db < schema.sql`
- Käynnistä sovellus `flask run`

- Testaa tietokantaa suoraan `sqlite3 database.db`

# Välipalautus 2 status

- urheilusuorituksien kommentit toteuttamatta, vaikka taulu on mukana tietokannassa
