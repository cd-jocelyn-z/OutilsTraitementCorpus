# OutilsTraitementCorpus

## TP 1 : Parite 1

1. **CoNLL-2003** est un dataset pour la reconnaissance d’entités nommées. C’est un dataset annoté, plus précisément pour la "language-independent named entity recognition".  
2. Il existe 8 fichiers qui s’occupent de l’anglais et de l’allemand :  
   1. Un fichier training file
   2. Un fichier development file 
   3. Un fichier test file  
   4. Un grand fichier contenant des données non annotées

    **Pour la langue anglaise** :  
   - Les articles ont été pris du Reuters Corpus, qui contient les Reuters News Stories.  
   - Le set de training et de development correspond aux 10 derniers jours d’août 1996.  
   - Le test set date de décembre 1996.  
   - Le grand fichier contient les données prétraitées pour le mois de septembre 1996.

    **Pour la langue allemande** :  
   - Les articles ont été pris du ECI Multilingual Text Corpus, plus précisément du journal allemand Frankfurter Rundschau.  
   - Les sets de training, development et de test concernent les articles écrits durant une semaine vers la fin d’août 1992.  
   - Le grand fichier, contenant les données brutes, couvre la période de septembre à décembre 1992.

2. **Objectif et utilisation** :  
   Le dataset répond au besoin de la reconnaissance d’entités nommées (Named Entity Recognition, NER). Le NER consiste à identifier dans une phrase les noms et prénoms d’une personne, le nom d’un organisateur ou d’endroits.

3. **Modèles entraînés sur CoNLL-2003** :  
   Les modèles suivants ont été entraînés sur ce dataset :  
   - ACE  
   - bert-large-uncased-finetuned-ner  
   - LUKE + SubRegWeigh  
   - FLERT XLM-R

5. C’est un corpus multilingue.

## TP 1 : Partie 2

La tâche est la génération de texte à partir des métadonnées. Le sujet porte sur le programme d’une radio indépendante aux États-Unis appelée WFMU, reconnue aujourd’hui comme la plus ancienne radio free-form du pays. Cela signifie que les DJs y diffusent librement la musique de leur choix, sans contrainte publicitaire.

Les descriptions des programmes sont souvent très courtes et parfois seulement quelques mots-clés ou une ou deux phrases, mais la station publie les playlists complètes de chaque diffusion.

Je souhaite donc créer des données synthétiques à partir des métadonnées, des descriptions existantes, et les playlist diffusés afin de générer des descriptions plus pertinentes pour chaque programme.

Ce type de données augmentées permettra d’entraîner un modèle capable de produire automatiquement des descriptions à partir d’éléments structurés.

Le type de données comprend par exemple :

- program name
- episode date
- program url
- description
- playlist url
- tracks
   - artist 
   - track
   - album

L’idée est d’enrichir les descriptions des programmes en créant un dataset synthétique à partir des métadonnées et des playlists, puis d’entraîner un modèle transformateur capable de générer automatiquement un texte fluide et pertinent à partir de ces éléments, même lorsque les descriptions initiales sont très limitées.

J'ai vérifié leur fichier [robots.txt](https://wfmu.org/robots.txt), qui affiche :

> User-agent: *
   Disallow: /artistbrowser.php?action=artist
   User-agent: Slurp
   Crawl-delay: 30
   User-agent: SemrushBot
   Disallow: /
   User-agent: SemrushBot-SA
   Disallow: /
   User-agent: SemrushBot-BA
   Disallow: /
   User-agent: SemrushBot-SI
   Disallow: /
   User-agent: SemrushBot-SWA
   Disallow: /
   User-agent: SemrushBot-CT
   Disallow: /
   User-agent: SemrushBot-BM
   Disallow: /

Ce qui nous permet d’effectuer le scraping de leur page de planning ainsi que des pages permettant de récupérer leurs playlists.

## TP 2 : Récuperer votre corpus de travail à partir d’une resource web (pas d’API)

C’était intéressant, car je suis plutôt habituée à des sites plus “prévisibles” quand il s’agit de scraper des informations. Celui-ci est un site assez ancien, que certaines personnes essaient encore d’entretenir. Il dispose d’une archive riche, mais certaines informations ne sont pas aussi accessibles qu’elles en ont l’air. Il y avait de nombreux cas où les données n’étaient pas dans les balises qu’on s’attendrait à trouver.

Voici les pages qui m’ont intéressée :

1. **La page où se trouve le planning**
   – J’ai pris seulement 7 programmes pour ce projet.

2. **La page où se trouve l’information du programme, où l’on trouve l’indexation des diffusions faites.**

3. **La page playlist, qui contient un tableau avec les informations sur les musiques jouées pendant la diffusion.**
   – J’ai choisi de prendre seulement les 5 diffusions les plus récentes de chaque programme.


Voici les scripts pour récupérer mes données afin de constituer le corpus :

1. [datastructures.py](https://github.com/cd-jocelyn-z/OutilsTraitementCorpus/blob/main/scripts/process/datastructures.py)
   – Après mes recherches sur les données possibles à utiliser pour mon corpus, j’ai défini la structure avec des `dataclasses` afin de faciliter, plus tard, la tâche de sérialiser et désérialiser, et d’avoir une structure claire pour le corpus.

2. [corpus\_utils.py](https://github.com/cd-jocelyn-z/OutilsTraitementCorpus/blob/main/scripts/process/corpus_utils.py)
   – J’y crée des fonctions pour sérialiser et désérialiser selon la structure définie.

3. [crawler.py](https://github.com/cd-jocelyn-z/OutilsTraitementCorpus/blob/main/scripts/process/crawler.py)
   – Le but, c’est de partir de la page où l’on trouve la liste des diffusions d’un programme, puis de suivre chaque lien “See the playlist” ou “Listen” afin de naviguer vers la page contenant le tableau des chansons jouées.
   – À la fin, je n’ai pas utilisé de bibliothèque dédiée pour crawler, car pour cette tâche, cela ne me semblait pas nécessaire, mais j’ai gardé l’idée en tête lors de la création de ce script.

4. [scraper.py](https://github.com/cd-jocelyn-z/OutilsTraitementCorpus/blob/main/scripts/process/scraper.py)
   – J’y ai organisé mes fonctions pour faire un scrape d’une page en récupérant les éléments que j’avais définis dans `datastructures.py`.

5. [run\_pipeline.py](https://github.com/cd-jocelyn-z/OutilsTraitementCorpus/blob/main/scripts/process/run_pipeline.py)
   – Après avoir testé les autres scripts, j’ai créé ce script pipeline pour exécuter toutes les étapes nécessaires dans l’ordre, afin de constituer le corpus.

## TP3 : Visualiser votre corpus et réaliser des statistiques de texte

> **Note sur l’approche adoptée :** Les textes que j’ai récupérés jusqu’ici sont relativement courts, ce qui limite un peu la richesse des visualisations à cette étape. J’ai toutefois prévu de les enrichir dans la suite (TP4), en intégrant les métadonnées disponibles (nom de l’émission, DJ, date, morceaux joués, etc.) afin de générer des descriptions synthétiques.
Cela permettra de constituer un corpus plus complet et mieux adapté à l’analyse, tout en explorant la génération de données synthétiques de la tâche suivante.

### Vis 1 :
