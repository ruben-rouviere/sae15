from enum import Enum;
class ParkingStatus(Enum):
    OPEN = "Open",
    CLOSED = "Closed",
    UNKNOWN = "Unknown" # Information ajoutée non présente dans la donnée de base.
