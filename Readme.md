# Projet Théorie des langages Athène Rousseau Rambach

Ce projet consiste à mettre en place de la création et manipulation d'automates en Python.

## Mise en place préalable

Avant de lancer le projet, il faut s'assurer que votre machine ai `graphviz`.
Pour télécharger graphviz, vous pouvez vous rendre sur ce site `https://graphviz.org/download/` et télécharger la dernière version.
Pensez à ajouter graphviz au PATH si ce n’est pas fait automatiquement.
Il faut également installer la bibliothèque Python associée :
pip install graphviz

## Lancer les tests

Un fichier de test est déjà préparé.  
Pour l'exécuter, entrez dans un terminal :
`python tests.py`

## Tester avec un autre fichier

Des fichiers de tests ont été mis à disposition dans le dossier `supports`, ayant un nom commençant par "automate", suivi d'un chiffre.
Ces automates n'ont pas été utilisés dans le fichier `tests.py`, mais sont à disposition de l'utilisateur.
Si vous souhaitez tester un autre fichier de test compatible avec le projet, utilisez la commande suivante (en remplaçant `[nom_fichier]` par votre fichier) :
python [nom_du_fichier_test_compatible].py

**Attention :** le fichier de test doit être **compatible avec la structure du projet** pour fonctionner correctement (noms des fonctions, format des automates, etc.)

## Résultats

Les résultats (par exemple, les fichiers générés pour les automates) sont automatiquement enregistrés dans le dossier `résultats` du projet.
Vous pourrez trouver, avec des noms explicites, les résultats du dernier lancement de code en fichiers exportés dans le dossier `résultats`.
Les fichiers dont le nom de sauvegarde dans le fichier de test n'est pas changé entre deux lancement de code se verront remplacés par la nouvelle version. Veuillez donc à renommer les fichiers qui pourraient être à garder entre deux lancement de code, dans le fichier `tests.py` ou dans le dossier `résultats`.
Il y a également un affichage ordonné des résultats dans le terminal, avec les résultats attendus et les résultats renvoyés.

## Structure du projet

- `automate.py` : contient la mise en place de la classe Automate
- `tests.py` : fichier de test principal
- `fonctions.py` : contient les fonctions de manipulation d'automates qui ne sont pas directement des fonctions dans la classe Automate
- `résultats/` : dossier où sont enregistrées les résultats des fonctions
- `supports/` : dossier où sont enregistrées les fichiers qui servent lors du lancement de `tests.py` ainsi que quelques fichiers supplémentaires si besoin
