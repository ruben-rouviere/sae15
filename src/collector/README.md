# Collecteur

Auteur: Ruben
Ce collecteur récupère toutes les 5 minutes (par défaut, valeur configurable) les données relatives au parkings vélos et voiture de Montpellier.

## Setup

### Via docker

```bash
mkdir data
docker build collector/ -t rouviere-etzweiler/sae15-collector
docker run -v "$(realpath ./data):/usr/local/src/data" rouviere-etzweiler/sae15-collector
```

### Via python

```bash
pip install -r requirements.txt
```

```bash
python3 ./collector/main.py
```

## Configuration (via variables d'environnement)

Intervalle de collecte:

``
SAMPLE_TIME = #En secondes)
``

Exemple:

```bash
SAMPLE_TIME="300" python3 ./collector/main.py
```

Ou via docker:

```bash
docker run -e "SAMPLE_TIME=300" # ...
```
