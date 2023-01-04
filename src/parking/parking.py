from enum import Enum
from datetime import *
from typing import List
import ParkingCode;
import ParkingEntry;
import ParkingStatus;

class Parking():
    nameCode: ParkingCode;
    entries: List[ParkingEntry()];

    def __init__(self, nameCode: ParkingCode):
        self.nameCode = nameCode;

    def insert(self, entry: ParkingEntry):
        self.entries.append(entry);

    def lastStatus(self) -> ParkingStatus:
        last = self.entries[len(self.entries)];
        cutoff = 12 * 60 * 60 # Si la dernière donnée date d'il y a plus de 12h

        if((datetime.now().timestamp - last.timestamp) > cutoff):
            print(f"Warning: no new data for ${self.nameCode} since more than ${cutoff} seconds.")
            return ParkingStatus.UNKNOWN;
        return last.status;