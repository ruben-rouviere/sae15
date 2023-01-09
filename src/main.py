"""import parking.ParkingEntry;
import requests"""
from lxml import etree

from parking.ParkingCode import ParkingCode
from parking.parking import Parking


def main():
    initParkings();
    loadRecords('./data');

def initParkings():
    for parking in ParkingCode:
        Parking(nameCode=parking); # La classe Parking maintient une liste de toutes ses instances.

def loadRecords(dir: str):
    import os;
    for filename in [x for x in os.walk(dir) if x.endswith(".xml")]:
        readxml(filename);


"""def main():
    parkings[] = [
        Parking(parking.ParkingCode.COME) 
        # On initialize chaque parking au debut du programme
    ]
    
    # http
    # xml
    # 
    time = "2022-01-04T12:33"
    free = 101
    total = 500

    entry = ParkingEntry(time, total, free, status)
    parkings['tonparking'].insert(entry)"""

def readxml(file: str):

    return()

readxml()






