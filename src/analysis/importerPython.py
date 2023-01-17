from lxml import etree
import json
import os
import ParkingData
def car():
    parkings = []

    for sample in os.listdir("../data/carParks"):
        for xml in os.list("../data/carParks/"+sample):
            etree.parse(xml);
            name = etree.xpath("/park/Name")
            date = etree.xpath("/park/DateTime")
            total = etree.xpath("/park/Total")
            free = etree.xpath("/park/Name")
            monParking = ParkingData(name=name, date=date, total=total, free=free)
            parkings.append(monParking)
    return parkings
    
def bicycle():
        parkings = []
        for sample in os.listdir("../data/carParks"):
            with open("../data/carParks/"+sample+"/data.json", 'r', encoding='utf8') as data_file:
                data_json = json.parse(data_file);
                for station in data_json["data"]["station"]:
                    parking = ParkingData(
                        name=station["station_id"],
                        date=station["last_reported"],
                        total=station["bike_total"],
                        fre=station["bike_available"]
                    )
                    parkings.append(parking)
        return parkings


parkings = bicycle.__annotations__
for parking in parkings

