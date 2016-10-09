import socket
import sys
import time
import json
import re
import datetime
import sqlite3
import json

trajectories = []

def get_json(query):
    #try:
    elems = query.split("/")
    if len(elems) == 3:
        #####################
        ### SINGLE POINTS ###
        #####################
        
        gap = int(elems[0])
        da = datetime.date(2015, 1, 5) + datetime.timedelta(days = gap) # first day of the dataset + query offset
        y = da.year
        m = da.month
        d = da.day
        h = int(elems[1])
        mi = int(elems[2])
        
        conn = sqlite3.connect("../database/altran.db")
        c = conn.cursor()
        
        data = []
        for row in c.execute(("SELECT lat, lng, signal_avg " +
                              "FROM altran " +
                              "WHERE year = " + str(y) +
                              " AND month = " + str(m) +
                              " AND day = " + str(d) +
                              " AND hours = " + str(h) +
                              " AND minutes = " + str(mi))):
            lat = row[0]
            lng = row[1]
            sig = row[2]
            point = {'lat': lat, 'lng': lng, 'signal_avg': sig}
            data.append(point)

        conn.close()
        
        return json.dumps({'coordinates': data})
    else:
        ####################
        ### TRAJECTORIES ###
        ####################
        print(trajectories[int(query)])
        return json.dumps({'coordinates': trajectories[int(query)]})
    #except:
    #    return "{\"state\": -1}"


def read_trajectories():
    k = 0
    with open("../trajectories.data") as f:
        lines = f.readlines()
    for line in lines:
        line = line[:-1]
        for seg in line.split(";"):
            trajectory = []
            for segseg in seg.split(","):
                position = {}
                segsegseg = segseg.split("#")
                position['lat'] = float(segsegseg[0])
                position['lng'] = float(segsegseg[1])
                trajectory.append(position)
            trajectories.append(trajectory)
            k = k + 1
    print("num trajectories: " + str(k))
            

def serve(port):
    # Create communication socket and listen on port.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((socket.gethostname(), port))
    print("Started server: %s:%s" % (socket.gethostname(), port))
    server.listen(3)
    # Server loop.
    while True:
        print("\x1b[1mWaiting for requests on port %d ... \x1b[0m" % port)
        (client, address) = server.accept()
        print("Incoming request at " + time.ctime())
        message = client.recv(1 << 31)
        print(message)
        message = message.decode("ascii")
        # Consider only HTTP GET requests.
        print("Handling request at " + time.ctime())
        match = re.match("^GET /(.*) HTTP", message)
        if not match:
            continue
        query = match.group(1)
        print("HTTP GET request received: \"%s\"" % query)
        content = get_json(query)
        content_type = "text/plain"
        # Send result with proper HTTP headers.
        # print("Sending content: " + content)
        result = ("HTTP/1.1 200 OK\r\n"
                  "Content-type: %s\r\n"
                  "Access-Control-Allow-Origin: *\n"
                  "Content-length: %s\r\n\r\n%s") % (content_type,
                                                     len(content),
                                                     content)
        client.send(result.encode())
        client.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <port>")
        exit(1)
    port = int(sys.argv[1])
    read_trajectories()
    serve(port)
