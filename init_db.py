import subprocess
import sqlite3

subprocess.run(["sqlite3", "database.db", ".read schema.sql"])

con = sqlite3.connect("database.db")
con.executemany(
    "INSERT INTO sports (name) VALUES (?);",
    [
        ("Juoksu",),
        ("Kävely",),
        ("Pyöräily",),
        ("Uinti",),
        ("Kuntosali",),
        ("Jooga",),
        ("Hiihto",),
        ("Muu liikunta",),
    ],
)
con.commit()
con.close()
print('Tietokanta luotu')