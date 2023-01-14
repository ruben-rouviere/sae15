import time
from parking.CarParks import CarParks;


def getOpts():
    while True:
        try:
            # Temps_échantionnage
            Te: int = int(input("Merci de rensigner le temps d'échantillonage (en secondes): "));
            # Durée_acquisition
            #Da: int = round(int(input("Merci de rensigner la durée totale d'acquisition (en minutes): ")) * 60 / Te) # 5 minutes * 60 secondes 
            saveFileName: str = input("Merci de renseigner le nom du fichier de sortie : ")
            return (Te, saveFileName)
        except Exception: # Afin que ctrl+c reste fonctionnel, on limite aux Exceptions et non aux Interupts.
            print("Paramètre invalide, merci de bien vouloir réessayer.")


def main():
    carParks = CarParks();
    #bicyleParks = bicyleParks();
    # Paramètres
    (Te, saveFileName) = getOpts();

    while True:
        carParks.sample()
        print("Acquired data.")
        for p in carParks.parkings:
            p.getIdentifier()
        time.sleep(Te); # On attend le prochain Te

main()


""" def loadRecords(directory: str):
    import os;
    for filename in [x for x in os.listdir(directory) if x.endswith(".xml")]:
        try:
            Parking.deserializeEntry(directory+filename);
        except:
            print(f"Warning: Could not load file {directory+filename}")
            traceback.print_exc()
            pass; """