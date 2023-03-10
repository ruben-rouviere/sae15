from typing import List

from analysis.ParkingData import ParkingData

class CommonParking():
    def __init__(self, identifier: str, name: str, dataset: List[ParkingData]=[]) -> None:
        self.identifier = identifier
        self.name = name
        self.dataset = dataset    

    def getIdentifier(self) -> str:
        return self.identifier  

    def getName(self) -> str:
        return self.name    

    def getDataset(self) -> str:
        return self.dataset
    
    def addDataPoint(self, data: ParkingData):
        self.dataset.append(data)
    