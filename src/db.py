import sqlite3

connection = sqlite3.connect("./src/database.db")

with open("./src/schema.sql") as f:
    connection.executescript(f.read())

connection.commit()
connection.close()
