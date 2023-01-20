from typing import List
from lxml import etree
import json
import os
from ParkingData import ParkingData
from matplotlib import pyplot as plt 
import time
from datetime import datetime


def car() -> List[ParkingData]:
    parkings = []
    for sample in os.listdir("./data/carParks"):
        for xml in os.listdir("./data/carParks/"+sample):
            try:
                tree = etree.parse(f"./data/carParks/{sample}/{xml}")
                date = int(datetime.fromisoformat(tree.xpath("/park/DateTime")[0].text.split('.')[0]).timestamp())
                name = tree.xpath("/park/Name")[0].text
                status = tree.xpath("/park/Status")[0].text
                total = int(tree.xpath("/park/Total")[0].text)
                free = int(tree.xpath("/park/Free")[0].text)

                monParking: ParkingData = ParkingData(date=date, name=name, status=status, total=total, free=free)
                parkings.append(monParking)
            except etree.XMLSyntaxError:
                #print(f"Could not parse {xml}: {e}")
                pass
    return parkings
    
def bicycle():

        parkings = []
        for sample in os.listdir("data/bicyclePark"):
            with open("data/bicyclePark/"+sample+"/data.json", 'r', encoding='utf8') as data_file:
                data_json = json.JSONDecoder().decode("\n".join(data_file.readlines()))
                for station in data_json["data"]["stations"]:
                    print(station["last_reported"], station["station_id"],station["is_installed"],int(station["num_docks_available"]), int(station["num_bikes_available"]) )
                    parking = ParkingData(
                        date=station["last_reported"],
                        name=station["station_id"],
                        status=station["is_installed"],
                        total= int(station["num_docks_available"]),
                        free=int(station["num_bikes_available"])
                    )
                    parkings.append(parking) 
        return parkings

parkings = bicycle.__annotations__
#for parking in parkings...

"""
# Préparer les données pour le graphique
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

# Créer le graphique à barres
plt.bar(x, y)

# Ajouter des titres aux axes
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# Ajouter un titre au graphique
plt.title('Simple bar chart')

# Afficher le graphique
plt.show()
"""

"""def grafic_parkings_car(date):
    parkings=car()
    x=[]
    y1=[]
    y2=[]
    for parking in parkings:
        x.append(parking.getName())
        y1.append(parking.geTotal())
        y2.append(parking.geTotal())-parking.getFree()/(parking.geTotal())
    plt.bar(x, y1)
    plt.bar(x, y2)
    plt.show()

def grafic_bicycle(date):
    parkings=bicycle()
    x=[]
    y1=[]
    y2=[]
    for parking in parkings:
        x.append(parking.getName())
        y1.append(parking.geTotal())
        y2.append(parking.geTotal())-parking.getFree()/(parking.geTotal())
    plt.bar(x, y1)
    plt.bar(x, y2)
    plt.show()"""


def plot_parkings(parkingsdata, date: int):
    x=[]
    y1=[]
    y2=[]
    parking_date=[p for p in parkingsdata if (p.getDate() < date)]
    for parking in parking_date:
        x.append(parking.getName())
        y1.append(parking.getTotal())
        y2.append((parking.getFree()/(parking.getTotal())*100))
    #plt.bar(x, y1)
    plt.bar(x, y2)
    plt.show()

#main
date=int(datetime(2023, 1, 1).timestamp())
#plot_parkings(car(), date)
plot_parkings(bicycle(),date)


