#coding: utf-8

import twitter
import time
import sqlite3
import datetime

#definition des variables
limit = 100 #limite d'urgence
terms = [
    [u"séisme"], [u"tsunami"],
    [u"glissement de terrain", u"éboulement"],
    [u"catastrophe Nucléaire"], [u"incendie"],
    [u"attaque terroriste", u"coup de feu", u"fusillade"],
    [u"tornade", u"vents violent", u"ouragan", u"typhon", u"cyclone", u"tempête"],
    [u"coulée de boue"], [u"chute de météorites"],
    [u"tempête de neige", u"blizzard", u"avalanche"],
    [u"crue", u"innondation"],
    [u"explosion"], [u"éruption volcanique"]
] #Liste des termes de menaces a rechercher
lasts = [] #Liste des id des derniers elements
occurences = [] #Dictionnaire associant chaque terme avec le nombre d'occurence
places = []



while 1:
    print "Lancement d'une nouvelle captation..."
    #verification depuis twitter
    api = twitter.Api(consumer_key='36KxAiR6jLZmR4KLAGtwLRlZL',consumer_secret='OOgBXovEOkC7ZR5bNz7PPBjV5H8TolQK4jQktf398vtypLbi8r',access_token_key='3404138933-yo015NGKxT2W09TPV3RmDMIxCxyrDe3uiWn3DaK',access_token_secret='Nnq5NzdasR5chkqmOJI6BtW3Aj0Rp97Zvs11nQitjCeD3')
    #Pour chacun des termes de la liste on fait une recherche. A partir de la on recupere le nombre de tweets
    index = 0
    for li in terms:
        coords = 0
        status = []
        #initialisation des valeurs si elles n'existent pas
        if index >= len(lasts):
            lasts.append(0)
        if index >= len(occurences):
            occurences.append(0)
        if index >= len(places):
            places.append(dict(latitude = 0, longitude = 0))
        for term in li:
            status = status + api.GetSearch(term = term, since_id = lasts[index], lang = "fr", count=100)
            occurences[index] = occurences[index] + len(status)
        for statu in status:
            if statu.GetCoordinates() != None:
                places[index]['latitude'] = places[index]['latitude']+statu.GetCoordinates()['coordinates'][0]
                places[index]['longitude'] = places[index]['longitude']+statu.GetCoordinates()['coordinates'][1]
                coords = coords + 1
        if coords != 0:
            places[index]['latitude'] = places[index]['latitude'] / coords
            places[index]['longitude'] = places[index]['longitude'] / coords
        lasts[index] = status[len(status)-1].GetId()
        index = index + 1

    #Lorsque le nombre de tweets depasse le nombre limit on lance la procedure de verification pour le terme associe
    index = 0
    database = sqlite3.connect('bdd.db')
    cursor = database.cursor()
    for occ in occurences:
            print terms[index][0] + " a "+str(occ)
            if(occ > limit):
                #on lance la procedure de verification pour le term terms[index]
                #os.system(u"verification.py "+terms[index][0])
                # Pas le temps, on vérifie pas on enregistre direct dans la base
                if places[index]['latitude'] !=  0 and places[index]['longitude'] != 0: #si on a trouvé une position
                    cursor.execute(u"INSERT INTO Geolocalizations(latitude, longitude) VALUES ('"+str(places[index]['latitude'])+"','"+str(places[index]['longitude'])+"')")
                    database.commit()
                    geoid = cursor.execute("SELECT MAX(Geolocalizations.id) FROM Geolocalizations").fetchone()[0]
                    t =datetime.datetime.now().strftime("%d/%m/%Y", )
                    cursor.execute(u"INSERT INTO Events(name, date, Geolocalizations_id) VALUES ('"+terms[index][0]+"', '"+t+"', '"+str(geoid)+"')")
                    database.commit()
                pass
            index = index + 1
    database.close()
    print "Travail termine."
    time.sleep(5)
