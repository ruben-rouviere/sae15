import os
import time
from parking.CarParks import CarParks;
import time


import logging
logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.DEBUG)


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
            saveFileName: str = input("Merci de renseigner le nom du fichier de sortie : ")
            return (Te, saveFileName)
        except Exception: # Afin que ctrl+c reste fonctionnel, on limite aux Exceptions et non aux Interupts.
            logging.error("Paramètre invalide, merci de bien vouloir réessayer.")

def main():
    carParks = CarParks();
    #bicyleParks = bicyleParks();
    # Paramètres
    Te = getOpts();

    logging.info(f"Starting data collection every {Te} seconds.")

    # On se synchronise sur un multiple de Te afin de garder une cohérence 
    # entre différentes exécution du script.
    # Si le script est executé deux fois, on aura donc dans le pire des cas
    # une différence de temps entre le dernier sample et le premier sample qui sera
    # un multiple de Te.
    nextCycle = lambda currentTime, Te: Te-(round(currentTime) % Te)
    while nextCycle(time.time(), Te) != Te:
        logging.info(f"Waiting {nextCycle(time.time(), Te)}s for synchronization...")
        time.sleep(nextCycle(time.time(), Te))
    
    # On démarre la collection à proprement parler.
    while True:
        logging.info("Starting sampling...")
        # Temps départ
        Td = time.time()
        carParks.sample()
        # Durée
        D = time.time() - Td
        logging.info(f"Acquired data in {D:f.0} seconds. Next collection in {Te-D:f.0} seconds.")
        # On compense Te par la durée de la collection de donnée.
        # Cela devrait en théorie permettre un écart temporel constant entre les points de données,
        # pourvu que max(D) < Te
        if(D > Te):
            logging.warn("Duration of sampling greater than sampling interval !")
        time.sleep(Te-D);

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