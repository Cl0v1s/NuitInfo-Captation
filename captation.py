#coding: utf-8

import twitter
import time
import os

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

while 1:
    print "Lancement d'une nouvelle captation..."
    #verification depuis twitter
    api = twitter.Api(consumer_key='trsjWIC37dPVaMranGc29hpfc',consumer_secret='eoVDETqmppowd6uxGbpedwPC8wiYLKoPsWuuwYsCSwAJ7PQnO8',access_token_key='413250016-YTyaTmIbbUjZJqG4QzDGwF79ufTTqPSY3S0ZjkN4',access_token_secret='wRLkJpw0eyrkcVQoAKIf2fvA5zphr4lD9E1fHU8jhIgXA')
    #Pour chacun des termes de la liste on fait une recherche. A partir de la on recupere le nombre de tweets
    index = 0
    for li in terms:
        #initialisation des valeurs si elles n'existent pas
        if index >= len(lasts):
            lasts.append(0)
        if index >= len(occurences):
            occurences.append(0)
        for term in li:
            status = api.GetSearch(term = term, since_id = lasts[index], lang = "fr", count=100)
            occurences[index] = occurences[index] + len(status)

        lasts[index] = status[len(status)-1].GetId()
        index = index + 1

    #Lorsque le nombre de tweets depasse le nombre limit on lance la procedure de verification pour le terme associe
    index = 0
    for occ in occurences:
            print terms[index][0] + " a "+str(occ)
            if(occ > limit):
                #on lance la procedure de verification pour le term terms[index]
                os.system("verification.py "+terms[index][0])
                pass
            index = index + 1

    print "Travail termine."
    time.sleep(5)
