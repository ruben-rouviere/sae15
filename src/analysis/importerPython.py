from typing import List
from lxml import etree
import json
import os

import requests
from ParkingData import ParkingData
from matplotlib import pyplot as plt 
from datetime import datetime, timedelta

def car() -> List[ParkingData]:
    parkings = []
    for sample in os.listdir("./data/carParks"):
        for xml in os.listdir("./data/carParks/"+sample):
            try:
                tree = etree.parse(f"./data/carParks/{sample}/{xml}")

                # Filtre temporel (voir analysis.ipynb): date de collecte de l'échantillon - date des donneés
                delta = abs(datetime.fromisoformat(sample.replace('_', ':')) - datetime.fromisoformat(tree.xpath("/park/DateTime")[0].text.split('.')[0]))
                #print(delta)
                if(delta > timedelta(hours=12)):
                    print(f"Invalid sample: {sample}/{xml}: timedelta = {delta}")
                    continue; 

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
        for sample in os.listdir("./data/bicycleParks"):
            with open("./data/bicycleParks/"+sample+"/data.json", 'r', encoding='utf8') as data_file:
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


def demande():
    #renvoie un graphique barre du pourcentage de libre d'un parking ou d'un relai-vélo en fonction de la réponse de la requête
    vehicule=int(input("Voulez-vos des informations à propos des parkings voitures (1) ou des relais vélos (2) ?"))
    annee=int(input("A quelle année voulez-vous cette information ? (année)"))
    if annee!=2023:
        return False
    mois=int(input("Quel mois ?"))
    if mois>12:
        return False
    jour=int(input("Quel jour ?"))
    if jour> 31:
        return False
    heure=int(input("Quelle heure ?"))
    if heure>24:
        return False
    minute=int(input("Quelle minute ?"))
    if minute>59:
        return False
    date=int(datetime(annee, mois, jour, heure,minute).timestamp())
    if vehicule==1:
        plot_parkings_libre(car(), date)
    else:
        plot_parkings_libre(bicycle(), date)
        
#demande()