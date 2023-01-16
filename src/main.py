from datetime import datetime
import os
import time
import traceback
from BicycleParking import BicycleParkings

from CarParkings import CarParkings

def getOpts():
    # On essaye d'abord de se configurer depuis l'environnement. 
    try:
        return (int(os.environ['SAMPLE_TIME']))
    except KeyError:
        # On n'accepte pas de prendre une configuration partielle depuis l'environnement
        # On fallback sur la configuration interactive. 
        pass

    while True:
        try:
            # Temps_échantionnage
            Te: int = int(input("Merci de rensigner le temps d'échantillonage (en secondes): "));
            # Durée_acquisition
            #Da: int = round(int(input("Merci de rensigner la durée totale d'acquisition (en minutes): ")) * 60 / Te) # 5 minutes * 60 secondes 
            #saveFileName: str = input("Merci de renseigner le nom du fichier de sortie : ")
            return Te
        except Exception: # Afin que ctrl+c reste fonctionnel, on limite aux Exceptions et non aux Interupts.
            print("Paramètre invalide, merci de bien vouloir réessayer.")

def main():
    carParks = CarParkings();
    bicyleParks = BicycleParkings();
    # Paramètres
    Te = getOpts();

    print(f"Starting data collection every {Te} seconds.")

    # On se synchronise sur un multiple de Te afin de garder une cohérence temporelle
    # entre différentes exécutions du script.
    # Si le script est executé deux fois, on aura donc dans le pire des cas
    # une différence de temps entre le dernier sample et le premier sample qui sera
    # un multiple de Te.
    nextCycle = lambda currentTime, Te: Te-(round(currentTime) % Te)
    while nextCycle(time.time(), Te) != Te:
        print(f"Waiting {nextCycle(time.time(), Te)}s for synchronization...")
        time.sleep(nextCycle(time.time(), Te))
    
    # On démarre la collection à proprement parler.
    while True:
        print("Starting sampling...")
        # Temps départ
        Td = time.time()
        timestamp = datetime.fromtimestamp(Td).isoformat(timespec='seconds').replace(':', '_')

        try:
            carParks.sample(timestamp)
        except Exception:
            traceback.print_exc()
            print("Car sampling failed !")
        # On traite indépendament les deux collectes de données
        # afin de ne pas perdre l'intégralité des données si la collecte de l'une d'entre elle échoue. 
        try:
            bicyleParks.sample(timestamp)
        except Exception:
            traceback.print_exc()
            print("Bicycle parking sampling failed !")


        # Durée
        D = time.time() - Td
        print(f"Acquired data in {D:.1f} seconds. Next collection in {Te-D:.1f} seconds.")
        
        # On compense Te par la durée de la collection de donnée.
        # Cela devrait en théorie permettre un écart temporel constant entre les points de données,
        # pourvu que max(D) < Te
        if(D > Te):
            print("Duration of sampling greater than sampling interval !")
        # On doit flush manuellement le logger pour une raison inconnue.
        time.sleep(max(0, Te-D));


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