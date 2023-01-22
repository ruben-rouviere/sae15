# Adapté de la documentation d'InfluxDB: https://www.influxdata.com/blog/import-json-data-influxdb-using-python-go-javascript-client-libraries/
from datetime import datetime
from dateutil import parser
import json
import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS
from influxdb_client.client.exceptions import InfluxDBError
import requests

def convertBicycle(sample: str):
    points = []
    # On considère station_infos comme statique, et on les injecte avec chaque point de donnée.
    station_infos = json.load(
        requests.get("https://montpellier-fr-smoove.klervi.net/gbfs/en/station_information.json").content
    )
    
    with open(f"{sample}/data.json", "r") as json_file:
        print(f"Processing {sample}...")
        jsonTree = json.load(json_file)
        for station in jsonTree["data"]["stations"]:
            point = Point("bicycleParking")
            # On importe toutes les données des stations
            for key, value in station.items():
                if(key == "last_reported"): 
                    # On importe le temps en tant que donnée temporelle
                   
                    # Pour une raison inconnue, passer directement le timestamp
                    # a Point.time() sans utiliser datetime.fromtimestamp ne fonctionne pas (le point est inséré avec une timestamp=0) 
                    point.time(datetime.fromtimestamp(value))
                    continue;
                if(key == "station_id"):
                    # On injecte également les informations de stations_informations.json
                    for key_info, value_info in station_infos["data"]["stations"][int(value)]:
                        if(key_info == "name"):
                            point.field(key_info, value_info)
                # Les autres données sont des entiers.
                point.field(key, int(value))
            points.append(point)
    return points

def convertCar(sample: str):
    from lxml import etree
    points = []
    for filename in [x for x in os.listdir(sample) if x.endswith(".xml")]:
        try:
            print(f"Processing {filename}...")
            tree = etree.parse(f"{sample}/{filename}");
            point = Point("carParking")
            for element in tree.iter():
                print(f"{element.tag},{element.text}")
                if(element.tag == "DateTime"): 
                    point.time(parser.parse(element.text))
                if(element.tag in ["Free", "Total"]): # On importe en int lorsque possible
                   point.field(element.tag, int(element.text))
                   continue
                point.field(element.tag, element.text)
            points.append(point)
        except etree.XMLSyntaxError as e:
            print(f"{sample}/{filename} has a syntax error.")
    return points


# Main
bucket = "parkings-v3"
# Dans une situation profesionnelle réelle, le token ne serait bien évidement pas hardcodé, mais injecté au runtime via une variable d'environement ou via des technologies telles que Hasicorp Vault.
with InfluxDBClient(url="http://45.147.97.88:8086", token="6C80FZTgMCAQPAA-8djqW2mUvSQ9FsSMfYwt722etTLUIT83tN9_ghooyAWQPI5VA3SJ80WpkWokm9k3dJYQvQ==", org="RT1") as client:
    with client.write_api(write_options=SYNCHRONOUS) as writer:
        try:
            for sample in os.listdir("../data/bicyclePark"):
                points = convertBicycle(f"../data/bicyclePark/{sample}")
                writer.write(bucket=bucket, record=points)
                print(f"Processed {sample}.")
            for sample in os.listdir(f"../data/carParks"):
                points = convertCar(f"../data/carParks/{sample}")
                writer.write(bucket=bucket, record=points)
                print(f"Processed {sample}.")
        except InfluxDBError as e:
            print(e)
