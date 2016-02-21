# -*- coding: utf-8 -*-
import requests, json, pandas as pd
from time import sleep
from ConfigParser import SafeConfigParser
import smtplib
from geopy.distance import vincenty
import sys

# uncomment for prodution
url = 'https://www.autolib.eu/fr/stations'
# url = 'http://localhost:3000/autolib.html'

def vincenty_in_km(lat1, long1, lat2, long2):
    return vincenty((lat1, long1), (lat2, long2)).km

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



class Database:
    def update(self):
        print "fetching page"
        r = requests.get(url)
        source_code = str(r.content)
        raw_data = source_code.split("var map = initMap(",1)[1].split('\n', 1)[0][:-3]
        stations_pandas = pd.DataFrame(pd.read_json(raw_data))
        stations_pandas.set_index('station_id', inplace=True)
        self.stations = stations_pandas
    def get_cars(self, station_id):
        return self.stations.loc[station_id, 'cars']
    def get_parks(self, station_id):
        return self.stations.loc[station_id, 'parks']
    def get_n_closest_stations(self, n, lat, lng):
        self.stations["distance to coord"] = map(vincenty_in_km, [lat]*len(self.stations),
            [lng]*len(self.stations), self.stations["lat"], self.stations["lng"])
        top_n_closest = Stations.stations.sort_values("distance to coord", ascending=True).head(n).index.tolist()
        return top_n_closest

    def monitoring(self, n, lat, lng, trip):
        #make sure we have fresh data
        self.update()
        closest_stations = self.get_n_closest_stations(n, lat, lng)
        type_response = None
        id_response = None

        if (trip=='depart'):
            for ids in closest_stations:
                if (self.get_cars(ids)>0):
                    type_response = "car is available"
                    id_response = ids
                    break
            if not(type_response):
                sleep(5)
                return self.monitoring(n, lat, lng, trip)
                print "no car available on the selected stations yet"

        elif (trip=='arrivee'):
            for ids in closest_stations:
                if (self.get_parks(ids)>0):
                    type_response = "spot is available"
                    id_response = ids
                    break
            if not(type_response):
                sleep(5)
                return self.monitoring(n, lat, lng, trip)
                print "no spot available on the selected stations yet"


        else:
            print "Erreur inconnue"

        # notification_email(type_response)
        print type_response





try:
    nb_stations = int(sys.argv[1])
    lat = float(sys.argv[2])
    lng = float(sys.argv[3])
    trip = str(sys.argv[4])
except IndexError:
    nb_stations = 3
    # empty station coordinates
    lat = 48.87244751
    lng = 2.30416621
    # Paris coordinates
    # lat = 48.8567
    # lng = 2.3508
    trip = "depart"

Stations = Database()

Stations.monitoring(nb_stations, lat, lng, trip)
