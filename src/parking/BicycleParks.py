import json
from typing import List

import requests
from parking.Parkings import Parkings;

class BicycleParks(Parkings):

    
    def __init__(self):
        self.parkings: List[Parking()];
        anwser = requests.get("https://montpellier-fr-smoove.klervi.net/gbfs/en/station_information.json")
        info = json.parse(anwser)
        for station in info.data.stations:
            self.parkings.append(
                Parking(
                station.station_id,
                url= 
                )
            )

        for name in names:
            self.parkings.append(Parking(
                    identifier,
                    url=f"https://data.montpellier3m.fr/sites/default/files/ressources/${name}.xml"))
            
    def getParkings(cls):
        return self.parkings;