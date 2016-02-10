# -*- coding: utf-8 -*-
import requests, json, pandas as pd
from time import sleep
from ConfigParser import SafeConfigParser
import smtplib

url = 'https://www.autolib.eu/fr/stations'


class Database:
    def get_cars(self, station_id):
        return self.stations.loc[station_id, 'cars']
    def get_parks(self, station_id):
        return self.stations.loc[station_id, 'parks']
    def update(self):
        print "fetching page"
        r = requests.get(url)
        source_code = str(r.content)
        raw_data = source_code.split("var map = initMap(",1)[1].split('\n', 1)[0][:-3]
        result = pd.DataFrame(pd.read_json(raw_data))
        result.set_index('station_id', inplace=True)
        self.stations = result

# instantiate Stations
Stations = Database()


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
    Stations.update()

    # either sleep for 5 sec or send notification
    if (trip=='depart'):
        if (Stations.get_cars(station_id)==0):
            print "no car there yet"
            sleep(5)
            return monitoring(station_id, trip)
            
        elif (Stations.get_cars(station_id)>0):
            type_response = "car is available"

    elif (trip=="arrivee"):
        if (Stations.get_parks(station_id)==0):
            print "no spot there yet"
            sleep(5)
            return monitoring(station_id, trip)

        elif (Stations.get_parks>0):
            type_response = "spot is available"

    else:
        print "Erreur inconnue"

    notification_email(type_response)


monitoring(5, "arrivee")