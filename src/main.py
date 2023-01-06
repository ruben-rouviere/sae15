"""import parking.ParkingEntry;
import requests"""
from lxml import etree

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

def readxml():
    tree=etree.parse("FR_MTP_EURO.xml")
    dateTime=tree.xpath("/park/DateTime")
    print(dateTime.text)
    return()

readxml()






