from abc import abstractmethod, ABCMeta
from typing import List
from parking.Parking import Parking

class Parkings(metaclass=ABCMeta):
    @abstractmethod
    def getParkings() -> List[Parking]:
        raise NotImplementedError
    
    @abstractmethod
    def sample(self):
        raise NotImplementedError
    
    @abstractmethod
    def saveData(self):
        raise NotImplementedError
