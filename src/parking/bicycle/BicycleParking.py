from typing import List
from parking.parking import Parking
from parking.parkingData import ParkingData


class BicycleParking(Parking):
    def __init__(self, identifier: str, name: str, capacity: int, dataset: List[ParkingData]=[]) -> None:
        super(BicycleParking, self).__init__(identifier, name, dataset);
        self.capacity = capacity