# -*- coding: utf-8 -*-
import requests, json, pandas as pd
from time import sleep
from ConfigParser import SafeConfigParser
import smtplib

url = 'https://www.autolib.eu/fr/stations'

# Fonction qui met a jour le tableau des stations de json a pandas, en remplacant l'index par station_id

# global is declared ... globally
stations = None

def update():
    r = requests.get(url)
    source_code = str(r.content)
    raw_data = source_code.split("var map = initMap(",1)[1].split('\n', 1)[0][:-3]

    global stations
    stations = pd.DataFrame(pd.read_json(raw_data))
    stations.set_index('station_id', inplace=True)


def get_cars(station_id):
    return stations.loc[station_id, 'cars']

def get_parks(station_id):
    return stations.loc[station_id, 'parks']

# Fonction qui recupere les informations dans le fichier de config et qui envoie le mail correspondant
def notification_email(type_response):
    # content of the notification
    if type_response == "car is available":
        msg = "Subject: Une voiture est disponible"
    elif type_response == "spot is available":
        msg = "Subject: Une place est disponible"
    
    # credentials of sender and recipient info
    config = SafeConfigParser()
    config.read('config.ini')
    fromaddr = config.get('main', 'username')+'@gmail.com'
    receiver = config.get('main', 'receiver')
    username = config.get('main', 'username')
    password = config.get('main', 'password')

    # connection to the mail server
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, receiver, msg)
    server.quit()

def monitoring(station_id, trip):
    # make sure we have fresh data
    update()

    # either sleep for 5 sec or send notification
    if (trip=='depart'):
        if (get_cars(station_id)==0):
            print "no car there yet"
            sleep(5)
            return monitoring(station_id, trip)
            
        elif (get_cars(station_id)>0):
            type_response = "car is available"

    elif (trip=="arrivee"):
        if (get_parks(station_id)==0):
            print "no spot there yet"
            sleep(5)
            return monitoring(station_id, trip)

        elif (get_parks(station_id)>0):
            type_response = "spot is available"

    else:
        print "Erreur inconnue"

    notification_email(type_response)


monitoring(1186, "depart")