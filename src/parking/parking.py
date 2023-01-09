from datetime import *
from typing import List
from typing import Self
import ParkingCode;
import ParkingEntry;
import ParkingStatus;

class Parking():
    # Les parkings étant fixes, il n'y a pas besoin de setter.
    __parkings = []; # Pas de weak reference car on souhaite utiliser la classe comme un holder pour ses instances.
     

    @classmethod
    def getParkings(cls) -> List[Self]:
        return cls.__parkings;

    # TODO: Transform __parkings into a Dict[ParkingCode, Parking] instead?
    # TODO: Refactor into a true Singleton.
    """
        Get the parking instance associated with this ParkingCode, initializing it if necessary.
    """
    @classmethod
    def getParking(cls, code: ParkingCode) -> Self:
        for parking in [x for x in cls.__parkings if x.nameCode == code]:
             assert len(parking) == 1;
             return parking[0];
             

    def __init__(self, nameCode: ParkingCode):
        self.nameCode: ParkingCode = nameCode;
        self.entries: List[ParkingEntry()];
        self.__parkings.append(self);

    def lastStatus(self) -> ParkingStatus:
        last = self.entries[len(self.entries)];
        cutoff = 12 * 60 * 60 # Si la dernière donnée date d'il y a plus de 12h

        if((datetime.now().timestamp - last.timestamp) > cutoff):
            print(f"Warning: no new data for ${self.nameCode} since more than ${cutoff} seconds.")
            return ParkingStatus.UNKNOWN;
        return last.status;


    def insert(self, entry: ParkingEntry):
        self.entries.append(entry);

    # TODO: Switch to lxml.objectify ?
    """
        Insert an entry into a Parking, initializing it if necessary.
    """    
    @classmethod
    def deserializeEntry(cls, filename: str) -> ParkingEntry:
            from lxml import etree;
            tree = etree.parse(filename);
            parkingCode: ParkingCode = ParkingCode[tree.xpath("/park/Name").text];

            return ParkingEntry(
                tree.xpath("/park/DateTime").text,
                int(tree.xpath("/park/Total").text),
                int(tree.xpath("/park/Free").text),
                ParkingStatus[tree.xpath("/park/Status").text]
            );