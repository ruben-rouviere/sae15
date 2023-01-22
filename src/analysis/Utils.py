
# Format souhaité : {"nom du parking": [ParkingData]}
from typing import List
from ParkingData import ParkingData

def parkingsByName(data: List[ParkingData]):
    parkingsByName = {}
    for parking in data:
        previousEntries = parkingsByName.get(parking.name, [])
        previousEntries.append(parking)
        parkingsByName.update({parking.name: previousEntries})
    return parkingsByName