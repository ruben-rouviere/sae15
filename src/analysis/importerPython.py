from lxml import etree
import json
import os
import ParkingData
from matplotlib import pyplot as plt 
import time
import datetime


def car():
    parkings = []
    for sample in os.listdir("../../data/carParks"):
        for xml in os.list("../../data/carParks/"+sample):
            etree.parse(xml)
            date = etree.xpath("/park/DateTime")
            name = etree.xpath("/park/Name")
            status=etree.xpath["/park/Status"],
            total = etree.xpath("/park/Total")
            free = etree.xpath("/park/Name")
            monParking = ParkingData(date=date, name=name, status=status, total=total, free=free)
            parkings.append(monParking)
    return parkings
    
def bicycle():
        parkings = []
        for sample in os.listdir("../data/carParks"):
            with open("../data/carParks/"+sample+"/data.json", 'r', encoding='utf8') as data_file:
                data_json = json.parse(data_file);
                for station in data_json["data"]["station"]:
                    parking = ParkingData(
                        date=station["last_reported"],
                        name=station["station_id"],
                        status=station["is_installed"],
                        total=station["bike_total"],
                        free=station["bike_available"]
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


def grafic_parkings(vehicule, date):
    parkings=vehicule()
    x=[]
    y1=[]
    y2=[]
    parking_date=[p for p in parkings if p.getDate()==date]
    for parking in parking_date:
        x.append(parking.getName())
        y1.append(parking.geTotal())
        y2.append(parking.geTotal())-parking.getFree()/(parking.geTotal())
    plt.bar(x, y1)
    plt.bar(x, y2)
    plt.show()

#main
date=datetime.datetime(2023,1,16,19,14,59)
grafic_parkings(car, date)
#grafic_parkings(bicycle,date)

