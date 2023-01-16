from typing import List

from parking.ParkingData import ParkingData



class BicycleParking(ParkingData):
    def __init__(self, identifier: str, name: str, capacity: int, dataset: List[ParkingData]=[]) -> None:
        super(BicycleParking, self).__init__(identifier, name, dataset);
        self.capacity = capacity