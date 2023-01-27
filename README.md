# SAÉ Données - Analyse des données des parkings de Montpellier

## Structure

## Collecteur

Le collecteur est chargé de recolter les données depuis les APIs.

### Setup

Via docker:

```bash
mkdir data
docker build collector/ -t rouviere-etzweiler/sae15-collector
docker run -v "$(realpath ./data):/usr/local/src/data" rouviere-etzweiler/sae15-collector
```

Ou directement via python:

```bash
python3 ./collector/main.py
```

## Analyse

## Setup

```bash
pip install -r requirements.txt
```