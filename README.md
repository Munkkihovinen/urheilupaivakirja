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
- Luo tietokanta komennolla `python init_db.py`. Tämä myös lisää lajirivit sports tauluun.
- Käynnistä sovellus `flask run`
- Luo tunnus etusivulla ja kirjaudu sisään

# Välipalautus 3 status

- Sovellusta kannattaa testata luomalla useampi tunnus ja lisätä useita suorituksia etusivun lomakkeen kautta.
- Käyttäjien on tarkoitus nähdä kaikkien lisäämät suoritukset, mutta pystyä muokkaamaan ja poistamaan vain itse lisättyjä.
- Sovelluksessa pitäisi olla lähes kaikki suunnitellut perustoiminnallisuudet valmiina.
- Sivuston tyyli ja css asiat on kesken
