import sqlite3

old_db = "altran_duplicates.db"
new_db = "altran.db"
table = "altran"

def num_rows(database, table):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    sql = "SELECT COUNT(*) FROM " + table
    rows = c.execute(sql)
    for r in rows:
        num = r[0]
    c.close()
    return num

n_old = num_rows(old_db, table)
n_new = num_rows(new_db, table)

print(n_old)
print(n_new)
print(n_old - n_new)
