# -*- coding: utf-8 -*-
import requests, json, pandas as pd
from time import sleep
from ConfigParser import SafeConfigParser
import smtplib

url = 'https://www.autolib.eu/fr/stations'

def update():
    r = requests.get(url)
    source_code = str(r.content)
    raw_data = source_code.split("var map = initMap(",1)[1].split('\n', 1)[0][:-3]
    
    global stations
    stations = pd.DataFrame(pd.read_json(raw_data))

    stations.set_index('station_id', inplace=True)


def get_cars(station_id):
    update()
    return stations.loc[station_id, 'cars']

def get_parks(station_id):
    update()
    return stations.loc[station_id, 'parks']

def notification_email(type_response):

    config = SafeConfigParser()
    config.read('config.ini')

    fromaddr = config.get('main', 'username')+'@gmail.com'
    receiver = config.get('main', 'receiver')

    if type_response = "car already available":
        msg = "Subject: Une voiture est deja disponible\n\n"
    elif type_response = "new car":
        msg = "Subject: Une voiture est maintenant disponible\n\n"
    elif type_response = "spot already available":
        msg = "Subject: Une place est deja disponible\n\n"
    elif type_response = "new spot":
        msg = "Subject: Une place est maintenant disponible\n\n"

    username = config.get('main', 'username')
    password = config.get('main', 'password')

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, receiver, msg)
    server.quit()

def monitoring(station_id, trip):
    update()
    if (trip=='depart') and (get_cars(station_id)==0):
        while (get_cars(station_id) == 0):
            sleep(1)
            update()
        type_response = "new car"

    elif (get_cars(station_id)>0):
        type_response = "car already available"

    elif (trip=="arrivee") and (get_parks(station_id)==0):
        while (get_parks(station_id) == 0):
            sleep(1)
            update()
        type_response = "new spot"

    elif (get_parks(station_id)>0):
        type_response = "spot already available"

    else:
        print "Erreur inconnue"

    notification_email(type_response)

monitoring(233, "depart")