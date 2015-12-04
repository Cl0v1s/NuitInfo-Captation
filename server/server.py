from bottle import route, run
import sqlite3
import math
import re

from bottle import response


class Distance:
    def __init__(self, string):
        data = re.split(":", string)
        self.latitude = float(data[0])
        self.longitude = float(data[1])
        pass

    def distance(self, other):
        return math.fabs(self.latitude - other.latitude) + math.fabs(self.longitude - other.longitude)
    pass

@route("/register", method=['OPTIONS', 'GET'])
def register():
    response.headers["Access-Control-Allow-Headers"] = "Origin, Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Request-Headers"] = "Origin, Content-Type"
    database = sqlite3.connect('bdd.db')
    cursor = database.cursor()
    cursor.execute("INSERT INTO Users(is_wounded, is_in_danger) VALUES ('0','0')")
    database.commit()
    ide = cursor.execute("SELECT MAX(id) FROM Users").fetchone()[0]
    database.close()
    return dict(state = "ok", id = ide)


@route("/update/<user>/<lat>/<long>", method=['OPTIONS', 'GET'])
def update(user, lat, long):
    response.headers["Access-Control-Allow-Headers"] = "Origin, Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Request-Headers"] = "Origin, Content-Type"
    database = sqlite3.connect('bdd.db')
    cursor = database.cursor()
    cursor.execute("INSERT INTO Geolocalizations(latitude, longitude) VALUES ('"+lat+"','"+long+"')")
    database.commit()
    ide  = cursor.execute("SELECT MAX(id) FROM Geolocalizations").fetchone()[0]
    cursor.execute("UPDATE Users SET Geolocalizations_id = '"+str(ide)+"' WHERE id = '"+str(user)+"'")
    database.commit()
    database.close()
    return dict(state="ok")



@route("/danger/<user>", method=['OPTIONS', 'GET'])
def danger(user):
    response.headers["Access-Control-Allow-Headers"] = "Origin, Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Request-Headers"] = "Origin, Content-Type"
    database = sqlite3.connect('bdd.db')
    cursor = database.cursor()
    userdata = cursor.execute("SELECT Users.id, Geolocalizations.latitude, Geolocalizations.longitude FROM Users INNER JOIN Geolocalizations ON Geolocalizations.id = Users.Geolocalizations_id").fetchone()
    userpos = Distance(str(userdata[1])+":"+str(userdata[2]))
    events = cursor.execute("SELECT Events.id, Events.date, Events.name, Geolocalizations.latitude as latitude, Geolocalizations.longitude as longitude FROM Events INNER JOIN Geolocalizations ON Geolocalizations.id = Events.Geolocalizations_id").fetchall()
    results = []
    for event in events:
        #calcul de la distance entre l'emplacement de l'user et l'event
        eventpos = Distance(str(event[3]) + ":" +str(event[4]))
        if userpos.distance(eventpos) < 1.30:
            warns = cursor.execute("SELECT Warns.id, Warns.Events_id FROM Warns WHERE Warns.Users_id = "+user).fetchall()
            found = False
            for warn in warns:
                if event[0] == warn[1]:
                    found = True
                    break
            if found == False:
                results.append(event)
    database.close()
    return dict(state="ok", events = results)

@route("/response/<user>/<value>", method=['OPTIONS', 'GET'])
def respons(user, value):
    response.headers["Access-Control-Allow-Headers"] = "Origin, Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Request-Headers"] = "Origin, Content-Type"
    database = sqlite3.connect('bdd.db')
    cursor = database.cursor()
    request = "UPDATE Users SET "
    if value == "wounded":
        request = request + "is_wounded"
    elif value == "danger":
        request = request + "is_in_danger"
    request = request + " = '1' WHERE Users.id = '"+user+"'"
    print request
    cursor.execute(request)
    database.commit()
    database.close()
    return dict(state = "ok")

@route("/read/<user>/<event>")
def readd(user, event):
    response.headers["Access-Control-Allow-Headers"] = "Origin, Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Request-Headers"] = "Origin, Content-Type"
    database = sqlite3.connect('bdd.db')
    cursor = database.cursor()
    cursor.execute("INSERT INTO Warns(Users_id, Events_id) VALUES ('"+user+"', '"+event+"')")
    database.commit()
    database.close()
    return dict()


@route("/victims", method=['OPTIONS', 'GET'])
def victims():
    response.headers["Access-Control-Allow-Headers"] = "Origin, Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Request-Headers"] = "Origin, Content-Type"
    database = sqlite3.connect('bdd.db')
    cursor = database.cursor()
    users  = cursor.execute("SELECT Users.is_in_danger, Users.is_wounded, Geolocalizations.latitude, Geolocalizations.longitude FROM Users INNER JOIN Geolocalizations ON Geolocalizations.id  = Users.Geolocalizations_id WHERE Users.is_wounded = '1' OR Users.is_in_danger = '1' ").fetchall()
    results = []
    for user in users:
        results.append(dict(is_in_danger = user[0], is_wounded = user[1], latitude = user[2], longitude = user[3]))
    return dict(results = results)

run(host='localhost', port=8080, reloader = True)
