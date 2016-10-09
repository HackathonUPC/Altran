import sqlite3

TABLENAME = "altran"

conn = sqlite3.connect("database/altran.db")
c = conn.cursor()

class point:
    def __init__(self, timestamp, date, lat, lng, carrier, fullCarrier, status, net, net_type):
        self.timestamp = timestamp
        self.date = date
        self.lat = lat
        self.lng = lng
        self.carrier = carrier
        self.fullCarrier = fullCarrier
        self.status = status
        self.net = net
        self.net_type = net_type
    
    def to_string(self):
        if self.net_type is None:
            self.net_type = "None"
            print("SET NONE")
        try:
            return ("(timestamp=" + str(timestamp) +
                    ", date=" + date +
                    ", lat=" + str(lat) +
                    ", lng=" + str(lng) +
                    ", carrier=" + carrier +
                    ", fullCarrier=" + fullCarrier +
                    ", status=" + str(status) +
                    ", net=" + str(net) +
                    ", net_type=" + self.net_type +
                    ")")
        except:
            return "(something strange)"


#sql = ("SELECT DISTINCT timestamp, date, lat, lng, carrier, fullCarrier, status, net, net_type " +
#       "FROM " + TABLENAME + " " +
#       "WHERE year = 2016 " +
#       "AND month = 09 " +
#       "AND day = 17 " +
#       "ORDER BY timestamp")
sql = ("SELECT DISTINCT timestamp, date, lat, lng, carrier, fullCarrier, status, net, net_type " +
       "FROM " + TABLENAME +
       " WHERE year = 2016 " +
       "AND month = 09" +
       " ORDER BY timestamp")
rows = c.execute(sql)

points = []

for i, row in enumerate(rows):
    timestamp = row[0]
    date = row[1]
    lat = row[2]
    lng = row[3]
    carrier = row[4]
    fullCarrier = row[5]
    status = row[6]
    net = row[7]
    net_type = row[8]
    p = point(timestamp,
              date,
              lat,
              lng,
              carrier,
              fullCarrier,
              status,
              net,
              net_type)
    points.append(p)

conn.close()

t_diff = 10 * 60 * 1000  # 3 min
l_diff = 0.02
def compare(p, a):
    res = p.timestamp - a.timestamp <= t_diff
    res &= abs(p.lat - a.lat) <= l_diff
    res &= abs(p.lng - a.lng) <= l_diff
    res &= p.carrier == a.carrier
    res &= p.fullCarrier == a.fullCarrier
    res &= p.status == a.status
    res &= p.net == a.net
    res &= p.net_type == a.net_type
    return res

active = []
inds = set()

for p in points:
    assigned = False
    no_longer_active = []
    for i in inds:
        a = active[i]
        if (p.timestamp - a[-1].timestamp > t_diff):
            # is no longer active
            no_longer_active.append(i)
        if not assigned:
            if compare(p, a[-1]):
                #print("(%i, %f, %f) -> (%i, %f, %f)" % (a[-1].timestamp, a[-1].lat, a[-1].lng, p.timestamp, p.lat, p.lng))
                a.append(p)
                assigned = True
    if not assigned:
        new_person = []
        new_person.append(p)
        inds.add(len(active))
        active.append(new_person)
    # remove no longer active persons
    for i in no_longer_active:
        inds.remove(i)

#print("lon\tlat\ttitle\tdescription\ticon\ticonSize\ticonOffset")
#k = 0
#print("var coordinates = [")
#for a in active:
#    if len(a) >= 2:
#        print(("," if k > 0 else "") + "[")
#        k += 1
#        for i, p in enumerate(a):
#            #print("%f\t%f\t%i\t%s\tOl_icon_blue_example.png\t16,16\t0,0" % (p.lng, p.lat, i, p.date))
#            print("{lat: %f, lng: %f}" % (p.lat, p.lng) + ("," if i < len(a) - 1 else ""))
#        print("]")
#print("]")

old_date = ""
line = ""
for i, a in enumerate(active):
    date = a[0].date[:10]
    if old_date != date:
        old_date = date
        if i > 0:
            print(line)
            line = ""
    if len(a) >= 2:
        if len(line) > 0:
            line += ";"
        for p in a:
            if len(line) > 0 and line[-1] != ";":
                line += ","
            line += str(p.lat) + "#" + str(p.lng)
print(line)
