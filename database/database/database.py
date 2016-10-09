import sqlite3
import os
import re

DUMMYTABLE = "import"
TABLENAME = "altran"
DATA_PATH = "../data_export_cobercat"

conn = sqlite3.connect("altran.db")
#conn = sqlite3.connect("/media/matze/C529-C47F/database/altran.db")
c = conn.cursor()

def drop_table(tablename):
    sql = "DROP TABLE IF EXISTS " + tablename
    c.execute(sql)

def create_table(tablename):
    sql = ("CREATE TABLE IF NOT EXISTS " + tablename + " " +
           "(" +
           "timestamp integer," +
           "date text," +
           "year integer," +
           "month integer," +
           "day integer," +
           "hours integer," +
           "seconds integer," +
           "minutes integer," +
           "milliseconds integer," +
           "lat float," +
           "lng float," +
           "signal_inst integer," +
           "signal_min integer," +
           "signal_max integer," +
           "signal_avg integer," +
           "carrier text," +
           "fullCarrier text," +
           "status integer," +
           "net integer," +
           "net_type text," +
           "lac integer," +
           "cid integer," +
           "psc integer," +
           "speed float," +
           "satellites integer," +
           "precision1 integer," +
           "provider text," +
           "activity integer," +
           "incident text," +
           "downloadSpeed float," +
           "uploadSpeed float" +
           ")")
    c.execute(sql)

def get_filenames():
    return [dirname for dirname in os.listdir(DATA_PATH) if dirname[0] != '.']

def splitdate(date):
    if (len(date) != len("2015-12-03 12:47:36.744000")):
        print(date)
    vals = []
    vals.append(date[0:4]) # year
    vals.append(date[5:7]) # month
    vals.append(date[8:10]) # day
    vals.append(date[11:13]) # hours
    vals.append(date[14:16]) # minutes
    vals.append(date[17:19]) # seconds
    vals.append(date[20:23]) # milliseconds
    return vals

def splitline(line):
    line = re.sub("\"\".*\"", "", line) # fix 2 weird lines
    splitted = line.split("\"")
    tokens = []
    for i, s in enumerate(splitted):
        if i % 2 == 1:
            tokens.append(s)
        else:
            splitted2 = s.split(",")
            for j, t in enumerate(splitted2):
                if len(t) > 0 or not ((i < len(splitted) and j == 0)
                                      or (j == len(splitted2) - 1)):
                    tokens.append(t)
    # split date
    date = tokens[1]
    datevals = splitdate(date)
    for dv in datevals:
        tokens.append(dv)
    # filter newline
    tokens = [t.replace("\n", "") for t in tokens]
    return tokens

def str2int(s):
    if s == "unknown" or s == "null" or s == "(null)":
        return None
    if len(s) == 0:
        return None
    else:
        try:
            return int(s)
        except:
            try:
                return int(float(s))
            except:
                print("ERROR")
                print(s)
                return 0

def str2str(s):
    if len(s) == 0:
        return None
    else:
        return s

def str2float(s):
    if s == "unknown" or s == "null" or s == "(null)":
        return None
    if len(s) == 0:
        return None
    else:
        return float(s)

def tokens2dict(tokens):
    d = {}
    d["timestamp"] = str2int(tokens[0])
    d["date"] = str2str(tokens[1])
    d["lat"] = str2float(tokens[2])
    d["lng"] = str2float(tokens[3])
    d["signal_inst"] = str2int(tokens[4])
    d["signal_min"] = str2int(tokens[5])
    d["signal_max"] = str2int(tokens[6])
    d["signal_avg"] = str2int(tokens[7])
    d["carrier"] = str2str(tokens[8])
    d["fullCarrier"] = str2str(tokens[9])
    d["status"] = str2int(tokens[10])
    d["net"] = str2int(tokens[11])
    d["net_type"] = str2str(tokens[12])
    d["lac"] = str2int(tokens[13])
    d["cid"] = str2int(tokens[14])
    d["psc"] = str2int(tokens[15])
    d["speed"] = str2float(tokens[16])
    d["satellites"] = str2int(tokens[17])
    d["precision1"] = str2int(tokens[18])
    d["provider"] = str2str(tokens[19])
    d["activity"] = str2int(tokens[20])
    d["incident"] = str2str(tokens[21])
    d["downloadSpeed"] = str2float(tokens[22])
    d["uploadSpeed"] = str2float(tokens[23])
    d["year"] = str2int(tokens[24])
    d["month"] = str2int(tokens[25])
    d["day"] = str2int(tokens[26])
    d["hours"] = str2int(tokens[27])
    d["minutes"] = str2int(tokens[28])
    d["seconds"] = str2int(tokens[29])
    d["milliseconds"] = str2int(tokens[30])
    return d

def insert_vals(vals):
    sql = ("INSERT INTO " + DUMMYTABLE + " (" +
           "timestamp," +
           "date," +
           "year," +
           "month," +
           "day," +
           "hours," +
           "minutes," +
           "seconds," +
           "milliseconds," +
           "lat," +
           "lng," +
           "signal_inst," +
           "signal_min," +
           "signal_max," +
           "signal_avg," +
           "carrier," +
           "fullCarrier," +
           "status," +
           "net," +
           "net_type," +
           "lac," +
           "cid," +
           "psc," +
           "speed," +
           "satellites," +
           "precision1," +
           "provider," +
           "activity," +
           "incident," +
           "downloadSpeed," +
           "uploadSpeed" +
           ") VALUES (" +
           ":timestamp," +
           ":date," +
           ":year," +
           ":month," +
           ":day," +
           ":hours," +
           ":minutes," +
           ":seconds," +
           ":milliseconds," +
           ":lat," +
           ":lng," +
           ":signal_inst," +
           ":signal_min," +
           ":signal_max," +
           ":signal_avg," +
           ":carrier," +
           ":fullCarrier," +
           ":status," +
           ":net," +
           ":net_type," +
           ":lac," +
           ":cid," +
           ":psc," +
           ":speed," +
           ":satellites," +
           ":precision1," +
           ":provider," +
           ":activity," +
           ":incident," +
           ":downloadSpeed," +
           ":uploadSpeed" +
           ")")
    c.execute(sql, vals)

def copy_data():
    filenames = get_filenames()
    for fn in filenames:
        print(fn)
        with open(DATA_PATH + "/" + fn) as f:
            lines = f.readlines()
            for l in lines[1:]:
                tokens = splitline(l)
                length = len(tokens)
                if length != 31:
                    print(length)
                    print(l)
                    print(tokens)
                vals = tokens2dict(tokens)
                insert_vals(vals)

def copy_table():
    sql = "CREATE TABLE " + TABLENAME + " AS SELECT DISTINCT * FROM " + DUMMYTABLE
    c.execute(sql)

print("providing table structures...")
drop_table(TABLENAME)
drop_table(DUMMYTABLE)
create_table(DUMMYTABLE)

print("reading data...")
copy_data()

print("copying distinct values...")
copy_table()

print("dropping table...")
drop_table(DUMMYTABLE)

print("vacuuming...")
c.execute("VACUUM")

conn.commit()
conn.close()

print("done.")

print(get_filenames())
