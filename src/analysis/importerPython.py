from typing import List
from lxml import etree
import json
import os

import requests
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
    
bicycleInfos = {};

def getBicycleInfos(identifier: str):
    if(identifier in bicycleInfos):
       return bicycleInfos[identifier] # Memoization
    jsonInfo = json.JSONDecoder().decode(requests.get("https://montpellier-fr-smoove.klervi.net/gbfs/en/station_information.json").text)
    
    # L'index et le numéro d'ID ne correspondent pas systématiquement.
    # De plus, certains IDs n'existant pas (plus?), on ne peut pas utiliser l'index d'une liste.
    # On doit donc utiliser un dictionnaire.
    for station in jsonInfo["data"]["stations"]:
        bicycleInfos.update({station["station_id"]: station}) 
    return bicycleInfos[identifier]
    

def bicycle():

        parkings = []
        for sample in os.listdir("data/bicyclePark"):
            with open("data/bicyclePark/"+sample+"/data.json", 'r', encoding='utf8') as data_file:
                data_json = json.JSONDecoder().decode("\n".join(data_file.readlines()))
                for station in data_json["data"]["stations"]:
                    #print(station["last_reported"], station["station_id"],station["is_installed"],int(station["num_docks_available"]), int(station["num_bikes_available"]) )
                    bicycleInfo = getBicycleInfos(station["station_id"])
                    parking = ParkingData(
                        date=station["last_reported"],
                        name=bicycleInfo["name"],
                        status=station["is_installed"],
                        total= bicycleInfo["capacity"],
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
    barContainer = plt.bar(x, y2)
    print()
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


