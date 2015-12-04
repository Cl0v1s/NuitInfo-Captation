import sqlite3
import signal
import smtplib
from email.mime.text import MIMEText

def handler(signum, truc):
    database = sqlite3.connect('bdd.db')
    cursor = database.cursor()
    users  = cursor.execute("SELECT Users.is_in_danger, Users.is_wounded, Geolocalizations.latitude, Geolocalizations.longitude FROM Users INNER JOIN Geolocalizations ON Geolocalizations.id  = Users.Geolocalizations_id WHERE Users.is_wounded = '1' OR Users.is_in_danger = '1' ").fetchall()
    if len(users) < 1:
        return
    body = "Bonjour, <br>Nous pensons que "+str(len(users))+" personnes sont blessees ou en danger, voici leur localisation et un indicatif de leur etat:<br><table border=1><tr><td>Localisation</td><td>Est blesse</td><td>Est en danger</td></tr>"
    for user in users:
        body = body + "<tr><td>"+str(user[2])+":"+str(user[3])+"</td><td>"
        if user[0] == "1":
            body = body+"Oui"
        else:
            body = body+"Non"
        body = body+"<td><td>"
        if user[1] == "1":
            body = body+"Oui"
        else:
            body = body+"Non"
        body = body + "</td></tr>"
    body = body + "</table>"
    orgas = cursor.execute("SELECT Organisations.mail FROM Organisations")
    for orga in orgas:
        #envoyer le mail ici avec le body definit plus haut
        pass
    cursor.execute("UPDATE Users SET is_wounded = '0', is_in_danger = '0'")
    database.commit()
    database.close()


signal.signal(signal.SIGALARM, handler)
signal.alarm(60*60*2)
