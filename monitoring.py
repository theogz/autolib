import requests, json, pandas as pd
from time import sleep

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



def monitoring(station_id, trip):
    update()
    if (trip=='depart') and (get_cars(station_id)=0):
        while (get_cars(stations_id) = 0):
            sleep(1)
            update()
        print r"Une voiture est disponible à la station"

    elif (get_cars(station_id)>0):
        print r"Il y a déjà une voiture."

    elif (trip=="arrivee") and (get_parks(station_id)=0):
        while (get_parks(station_id) = 0):
            sleep(1)
            update
        print r"Une place est disponible à la station."

    elif (get_parks(station_id)=0):
        print r"Il y a déjà une place."

    else:
        print "Erreur inconnue"
