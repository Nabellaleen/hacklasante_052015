# HackLaSanté 05-2015

## Introduction

Ce projet a été développé dans le cadre du hackathon *Hack La Santé* organisé par *Médecins du Monde* les 23 et 24 mai 2015.

Le thème, centré sur l'identification et le suivi des usagers/patients lors des missions de l'ONG, nous a amené à développer cette application.

Au coeur de celle-ci se trouvent :
- un algorithme de 'dé-doublonnage' permettant d'identifier deux fiches utilisateur partageant des données similaires
- une interface de saisi permettant de retrouver / créer / modifier une fiche

## Pré-requis

- Python 2.7.6 ou supérieur / Python 3.4 ou supérieur (https://www.python.org/)
- numpy (http://www.numpy.org/)

## Installation

- Télécharger le dépôt et l'extraire
- (optionnel - conseillé) Créer un environnement virtuel python (virtualenv, pyvenv, virtualenvwrapper, conda ...)
- Installer les dépendances
    pip install -r requirements.txt

## Exécution

- Lancer le serveur
    python main.py
- Accéder à l'interface avec un navigateur à l'url :
    http://127.0.0.1:5000/

    
