from abc import abstractmethod, ABCMeta
from typing import List
from parking.parking import Parking

class Parkings(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, saveDir: str) -> None:
        pass

    @abstractmethod
    def getParkings(self) -> List[Parking]:
        raise NotImplementedError
    
    @abstractmethod
    def sample(self, timestamp: str):
        raise NotImplementedError