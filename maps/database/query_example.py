import sqlite3

conn = sqlite3.connect("altran.db")
c = conn.cursor()

for row in c.execute("SELECT * FROM altran"):
    print(row)

conn.close()
