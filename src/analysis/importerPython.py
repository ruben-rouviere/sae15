from lxml import etree
import json
import os
import ParkingData
from matplotlib import piplot as plt 


def car():
    parkings = []

    for sample in os.listdir("../data/carParks"):
        for xml in os.list("../data/carParks/"+sample):
            etree.parse(xml)
            name = etree.xpath("/park/Name")
            date = etree.xpath("/park/DateTime")
            total = etree.xpath("/park/Total")
            free = etree.xpath("/park/Name")
            monParking = ParkingData(name=name, date=date, total=total, free=free)
            parkings.append(monParking)
    return parkings
    
def bicycle():
        parkings = []
        for sample in os.listdir("../data/carParks"):
            with open("../data/carParks/"+sample+"/data.json", 'r', encoding='utf8') as data_file:
                data_json = json.parse(data_file);
                for station in data_json["data"]["station"]:
                    parking = ParkingData(
                        name=station["station_id"],
                        date=station["last_reported"],
                        total=station["bike_total"],
                        fre=station["bike_available"]
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

def grafic_parkings_car(date):
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

def grafic_bicycle_car(date):
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

"""
def grafic_parkings(vehicule, date):
    parkings=vehicule()
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


#main
"""grafic_parkings(car,date)
grafic_parkings(bicycle,date)"""
