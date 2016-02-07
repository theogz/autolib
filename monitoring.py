import requests, json, pandas as pd

url = 'https://www.autolib.eu/fr/stations'
r = requests.get(url)
source_code = str(r.content)
raw_data = source_code.split("var map = initMap(",1)[1].split('\n', 1)[0][:-3]


stations = pd.DataFrame(pd.read_json(raw_data))

stations.set_index('station_id', inplace=True)


def get_cars(station_id):
    return stations.loc[station_id, 'cars']
print get_cars(60)
# def get_spots(station_id):
# def monitoring(station_id, type): #type = depart ou arrivee
