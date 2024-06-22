# QUIZY2ANKY

C'est un outil qui permet de convertir des fiches de Quizypedia.fr en des notes sur Anki. 

## Installation

- Téléchargez le répo en local (avec git clone ou en téléchargeant le zip) 
- Installez poetry pour gérer les dépendences (https://python-poetry.org/docs/)
- Téléchargez Google Chrome ou Chromium (si ce n'est pas déjà fait)
- Enfin, téléchargez le Chrome Driver qui correspond à votre installation : https://sites.google.com/chromium.org/driver/downloads?authuser=0

Vous aurez ensuite simplement à faire un `poetry install` puis `poetry run python Quizy2Anki.py args` ou rejoindre le virtual environment avec poetry shell.

## Usage

usage: Quizy2Anki: Convertissez vos fiches Quizy en notes Anki. [-h] --file FILE --output OUTPUT --driver DRIVER

options:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  le chemin de votre fichier contenant les URL des fiches que vous voulez convertir
  --output OUTPUT, -o OUTPUT
                        le fichier qui sera créé avec toutes vos notes dans un format txt à importer directement dans
                        Anki
  --driver DRIVER, -d DRIVER
                        le dossier où se trouve votre driver Chrome

## Exécution du script

Préparez votre fichier d'URL : Créez un fichier texte contenant les URL des fiches Quizy que vous souhaitez convertir. Chaque URL doit être sur une nouvelle ligne.

Puis exécutez le script
python quizy2anki.py --file chemin/vers/votre/fichierdurl.txt --output chemin/vers/fichierdesortie.txt --driver chemin/vers/chromedriver

### Fonctionnement

Extraction des URL : Le script lit les URL à partir du fichier fourni.
Connexion à chaque URL : Le script utilise Selenium pour ouvrir chaque URL et attend que la page soit complètement chargée.
Extraction des informations des fiches : Il extrait le thème et les détails de chaque fiche.
Sélection des indices : Il demande à l'utilisateur de sélectionner les indices (champs) à inclure dans la conversion. L'utilisateur est guidé dans cette phase.
Formatage pour Anki : Il convertit les informations extraites dans un format compatible avec Anki et les écrit dans le fichier de sortie.

## Remarques:

Assurez-vous que la version de ChromeDriver correspond à la version de Google Chrome installée.
Le script exécute Chrome en mode headless, ce qui signifie qu'il n'ouvrira pas de fenêtre de navigateur visible.
Le script inclut une note de test pour vérifier que le processus d'importation fonctionne correctement.
