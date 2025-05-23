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

## TP 1 : partie 2

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