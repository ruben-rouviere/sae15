from datetime import *
from typing import List

import requests

class ParkingData():


    def __init__(self, status: str, total: int, free: int):
        self.status = status
        self.total = total
        self.free = free


    def getStatus(self) -> str:
        return self.status
    
    def getTotal(self) -> str:
        return self.total
    
    def getFree(self) -> str:
        return self.free
    
    def getOccupation(self) -> float:
        return self.free/self.total
    

    def getMean(dataset) -> float:
        return sum(dataset)/len(dataset)
    



# class Parking():     
#     def __init__(self, identifier: str, url: str):
#         self.parkings: List[self()] = [];
#         self.identifier: str = identifier;
#         self.url: str = url;
    



#     # TODO: Transform __parkings into a Dict[ParkingCode, Parking] instead?
#     # TODO: Refactor into a true Singleton.
#     """
#         Get the parking instance associated with this ParkingCode, initializing it if necessary.
#     """
#     @classmethod
#     def getParking(cls, identifier: str):
#         for parking in [x for x in cls.__parkings if x.identifier == identifier]:
#              assert len(parking) == 1;
#              return parking[0];

#     def lastStatus(self) -> ParkingStatus:
#         last = self.entries[len(self.entries)];
#         cutoff = 12 * 60 * 60 # Si la dernière donnée date d'il y a plus de 12h

#         if((datetime.now().timestamp - last.timestamp) > cutoff):
#             print(f"Warning: no new data for ${self.identifier} since more than ${cutoff} seconds.")
#             return ParkingStatus.UNKNOWN;
#         return last.status;


#     def insert(self, entry: ParkingEntry):
#         self.entries.append(entry);

#     # TODO: Switch to lxml.objectify ?
#     # FIXME: Security: "The xml.etree.ElementTree module is not secure against maliciously constructed data. If you need to parse untrusted or unauthenticated data see XML vulnerabilities."
#     """
#         Deserialize and insert an entry into a Parking, initializing it if necessary.
#     """    
#     @classmethod
#     def deserializeEntry(cls, filename: str) -> ParkingEntry:
#             from lxml import etree;
#             tree = etree.parse(filename);
#             identifier = tree.xpath("/park/Name")[0].text;
#             print(f"identifier: {identifier}, {type(identifier)}")
#             # On construit une entrée à partir du XML.
#             # xpath retourne un generateur, par conséquent on ne peut pas accéder (subscript) au premier éléement avec la syntaxe x[n].
#             # On utilise donc next()
#             entry: ParkingEntry = ParkingEntry(
#                 tree.xpath("/park/DateTime")[0].text,
#                 next(int(tree.xpath("/park/Total")).text),
#                 next(int(tree.xpath("/park/Free")).text),
#                 ParkingStatus[next(tree.xpath("/park/Status")).text]
#             );
#             Parking.getParking(identifier).insert(entry);
