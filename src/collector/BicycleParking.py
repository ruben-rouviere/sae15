from typing import List
import json
import os
import time
import traceback
from typing import List
import requests
from CommonParking import CommonParking
from analysis.ParkingData import ParkingData


class BicycleParking(CommonParking):
    def __init__(self, identifier: str, name: str, capacity: int, dataset: List[ParkingData]=[]) -> None:
        super(BicycleParking, self).__init__(identifier, name, dataset);
        self.capacity = capacity

class BicycleParkings():
    def __init__(self):
        self.parkings: List[BicycleParking()] = [];

        anwser = requests.get(
            "https://montpellier-fr-smoove.klervi.net/gbfs/en/station_information.json")
        info = json.JSONDecoder().decode(anwser.text)

        for station in info['data']['stations']:
            self.parkings.append(
                BicycleParking(
                    identifier=station['station_id'],
                    name=station['name'],
                    capacity=station['capacity']
                )
            )


    def save(self, timestamp: str, data: str):
        baseDir = f"data/bicyclePark/{timestamp}"
        os.makedirs(baseDir, exist_ok=True)

        fileName = f"{baseDir}/data.json"
        with open(fileName, "w", encoding='utf8') as fileWriter:
            fileWriter.write(data)


    def internal_sample(self, timestamp):
        URL = "https://montpellier-fr-smoove.klervi.net/gbfs/en/station_status.json"
        req = requests.get(URL)
        data = req.text
        self.save(timestamp, data)
    
#        timestamp = datetime.now().isoformat(timespec='seconds').replace(':', '_')
    def sample(self, timestamp):
        for attempt in range(3): # 3 essais
            try:
                self.internal_sample(timestamp)
                print("Finished sampling bicycles.")
                break;
            except Exception:
                traceback.print_exc()
                print(f"Could not sample bicycles parking (attempt {attempt}/3).")
                time.sleep(3^attempt); # Back-off

    def getParkings(self) -> List[BicycleParking]: 
        return self.parkings

