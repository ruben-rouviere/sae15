import ParkingStatus;
import datetime;

class ParkingEntry():
    timestamp: int;
    capacity: int;
    free: int;
    status: ParkingStatus;

    def __init__(self, iso_timestamp: str, capacity: int, free: int, status: ParkingStatus):
        self.timestamp = datetime.fromisoformat(iso_timestamp).timestamp(); # On ne souhaite pas une précision en deça de la seconde, le cast de float vers int est donc acceptable.
        self.capacity = capacity
        self.free = free
        self.status = status
