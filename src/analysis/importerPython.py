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
                    #print(station["last_reported"], station["station_id"],station["is_installed"],int(station["num_docks_available"]), int(station["num_bikes_available"]) )
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

def plot_parkings_libre(parkingsdata, date: int):
    x=[]
    y1=[] #total
    y2=[] #disponible
    parking_date=[p for p in parkingsdata if (p.getDate() < date)]
    for parking in parking_date:
        x.append(parking.getName())
        y1.append(parking.getTotal())
        #on traite le cas où le parking a un total de 0 
        if parking.getTotal()==0:
            y2.append(0)
        else:
            y2.append((parking.getFree()/(parking.getTotal())*100)) 
    #plt.bar(x, y1)
    plt.bar(x, y2)
    plt.show()

def plot_parkings_occupation(parkingsdata, date: int):
    x=[]
    y1=[] #total
    y2=[] #disponible
    parking_date=[p for p in parkingsdata if (p.getDate() < date)]
    for parking in parking_date:
        x.append(parking.getName())
        y1.append(parking.getTotal())
        #on traite le cas où le parking a un total de 0 
        if parking.getTotal()==0:
            y2.append(0)
        else:
            y2.append((parking.getTotal()-parking.getFree()/(parking.getTotal())*100)) 
    #plt.bar(x, y1)
    plt.bar(x, y2)
    plt.show()

#main
date=int(datetime(2023, 1, 19).timestamp())
plot_parkings_occupation(car(), date)
#plot_parkings(bicycle(),date)


