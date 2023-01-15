#import parking.ParkingEntry;
from math import *

"""def main():
    parkings[] = [
        Parking(parking.ParkingCode.COME) 
        # On initialize chaque parking au debut du programme
    ]
    
    # http
    # xml
    # 
    time = "2022-01-04T12:33"
    free = 101
    total = 500

    entry = ParkingEntry(time, total, free, status)
    parkings['tonparking'].insert(entry)

import requests
response = requests.get("https://data.montpellier3m.fr/")
print(response.content)"""

def min(l):
    m=l[0]
    ind=0
    for i in range(len(l)):
        if l[i]<m:
            m=l[i]
            ind=i
    return(m, ind)

def max(l):
    m=l[0]
    ind=0
    n=len(l)
    for i in range(len(l)):
        if l[i]>m:
            m=l[i]
            ind=i
    return(m, ind)

def moyenne(L):
    if L==[]:
        print("erreur")
    else:
        n=0
        somme=0
        for e in L:
            somme+=e
            n+=1
        return somme/n

def variance(l):
    moy=moyenne(l)
    var=0
    n=len(l)
    for nb in l:
        var += (nb-moy)**2

    return (1/n) * var

def ecart_type(l):
    moy=moyenne(l)
    n=len(l)
    var=0
    for nb in l:
        var+=(nb-moy)**2
    return sqrt((1/n)*var)

def mediane(l):
    n = len(l)
    s = sorted(l)
    return (s[n//2-1]/2.0+s[n//2]/2.0, s[n//2])[n % 2] if n else None


#main
Liste=[0,10,20,15,5,13,7,0,20,18,16,4,2]
print("le minimum et son indice sont:",min(Liste))
print("le maximum et son indice sont:",max(Liste))
print("moyenne:", moyenne(Liste))
print("ecart-type:", ecart_type(Liste))
print("variance:", variance(Liste))
print("médiane:", mediane(Liste))


        