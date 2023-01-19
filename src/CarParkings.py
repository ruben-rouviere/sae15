
import os
from datetime import datetime
import time
import traceback
from typing import List

import requests
from lxml import etree, html
from analysis.ParkingData import ParkingData
from CommonParking import CommonParking

class CarParkings(CommonParking):
    parkings: List[ParkingData] = []

    def __init__(self):
        # https://data.montpellier3m.fr/dataset/disponibilite-des-places-dans-les-parkings-de-montpellier-mediterranee-metropole/resource-9
        ids = [
            "FR_MTP_ANTI",
            "FR_MTP_COME",
            "FR_MTP_CORU",
            "FR_MTP_EURO",
            "FR_MTP_FOCH",
            "FR_MTP_GAMB",
            "FR_MTP_GARE",
            "FR_MTP_TRIA",
            "FR_MTP_ARCT",
            "FR_MTP_PITO",
            "FR_MTP_CIRC",
            "FR_MTP_SABI",
            "FR_MTP_GARC",
            "FR_MTP_SABL",
            "FR_MTP_MOSS",
            "FR_STJ_SJLC",
            "FR_MTP_MEDC",
            "FR_MTP_OCCI",
            "FR_CAS_VICA",
            "FR_MTP_GA109",
            "FR_MTP_GA250",
            "FR_CAS_CDGA",
            "FR_MTP_ARCE",
            "FR_MTP_POLY"
        ]

        for identifier in ids:
            self.parkings.append(
                CommonParking(identifier=identifier, name=identifier))

    """
        Timestamp: unix timestamp, really should be ISO 8601 (yyyy-mm-ddThh:mm:ssZ), however ':' are not a valid character for windows filenames.
        Data: Raw data from API
    """

    def save(self, parking: CommonParking, timestamp: str, data: str):
        baseDir = f"data/carParks/{timestamp}"
        os.makedirs(baseDir, exist_ok=True)

        fileName = f"{baseDir}/{parking.getIdentifier()}.xml"
        with open(fileName, "w", encoding='utf8') as fileWriter:
            fileWriter.write(data)

    def internal_sample(self, timestamp: str, parking: CommonParking):
        url = f"https://data.montpellier3m.fr/sites/default/files/ressources/{parking.getIdentifier()}.xml"
        req = requests.get(url)
        data = req.text
        self.save(parking, timestamp, data)

        # https://stackoverflow.com/a/57833150 pour la solution.
        xml = html.fromstring(bytes(data, encoding='utf8'))
        # Il serait également possible d'utiliser directement lxml pour récuperer l'XML en HTTP,
        # mais cela impliquerait d'utiliser la librarie pour déserialiser l'XML afin de le sauvegarder.
        # Le choix a été fait d'essayer de conserver les données aussi "brutes" que possible

        for status in xml.xpath("Status"):
            for name in xml.xpath("Name"):
                for free in xml.xpath("Free"):
                    for total in xml.xpath("Total"):
                        parking.addDataPoint(ParkingData(status, total, free))

    def sample(self, timestamp):
        for parking in self.parkings:
            print("sampling " + parking.getIdentifier())
            for attempt in range(3): # 3 essais
                try:
                    self.internal_sample(timestamp, parking)
                    break;
                except Exception:
                    traceback.print_exc()
                    print(f"Could not sample {parking.getName()} (attempt {attempt}/3).")
                    time.sleep(3^attempt); # Back-off
        
        print("Finished sampling cars.")

    def getParkings(self) -> List[CommonParking]: 
        return self.parkings
