# Jeu de stratégie 2D - "Fakaiwi"

Un jeu de stratégie en 2D basé sur un plateau, où les joueurs contrôlent différentes unités possédant des compétences uniques, évoluant dans un environnement dynamique avec des obstacles variés. Ce projet est développé en Python avec la bibliothèque Pygame pour la gestion graphique.

## Table des Matières
- [Contributeurs](#contributeurs)
- [Aperçu du Jeu](#aperçu-du-jeu)
- [Fonctionnalités](#fonctionnalités)
- [Installation et Lancement](#installation-et-lancement)
- [Gameplay](#gameplay)
- [Architecture du Code](#architecture-du-code)
- [Contribuer](#contribuer)

## Contributeurs
Étudiants de Sorbonne Université Sciences dans le cadre d'un projet pédagogique dans l'unité d'enseignement de Programmation Orientée Objet en Python.
Master 1 - Ingénierie pour la Santé, Systèmes Mécatroniques pour la Réhabilitation (M1-IPS SMR).

### Liste des contributeurs :
- **GUERRERO ESCOBAR Fabian**: fabian.guerrero_escobar@sorbonne-universite.fr
- **LIU Kaiyu**: kaiyu.liu@sorbonne-universite.fr
- **WU William**: william.wu@sorbonne-universite.fr

### Encadrants universitaires :
- Louis ANNABI: louis.annabi@sorbonne-universite.fr
- Ramy ISKANDER: ramy.iskander@sorbonne-universite.fr

## Aperçu du Jeu
Capture d'écran ou GIF animé montrant le jeu en action (à ajouter).

## Fonctionnalités
- **Modes de jeu** :
  - **PVE** : Joueur contre Jeu aléatoire (Intelligence artificielle randomisée).
  - **PVP** : Joueur contre Joueur.
- **Tour par tour** : Le jeu se déroule en alternant les actions des joueurs et des ennemis.
- **Système de compétences** :
  - Attaques de mêlée, à distance ou en zone.
  - Compétences de soin, de buff et de debuff.
- **Obstacles dynamiques** :
  - Murs : non traversables.
  - Rivières : traversables uniquement par certains types d'unités.
  - Buissons : traversables mais stratégiques (on peut s'y cacher)
- **Interface utilisateur intuitive** :
  - Indicateurs visuels pour les déplacements, attaques et compétences.
  - Barre de santé visible pour chaque unité.

## Installation et Lancement
### Prérequis
Assurez-vous d'avoir Python 3.8 ou une version ultérieure installé ainsi que la bibliothèque Pygame.

```bash
pip install pygame
```

### Lancer le Jeu
Exécutez le fichier `main.py` :

```bash
python main.py
```

## Gameplay
Le jeu se déroule sur un plateau de 12x20 cases avec différentes unités et obstacles.

### Commandes :
- **Déplacement** : Utilisez les touches fléchées pour déplacer une unité sélectionnée.
- **Choix des compétences** : Utilisez la souris lorsque le menu de choix de compétences apparaît. 
- **Validation** : Appuyez sur `Espace` pour valider un déplacement ou valider une compétence.
- **Navigation dans les menus** : Utilisez les flèches haut et bas pour naviguer et `Espace` pour sélectionner.

### Objectifs :
- **PVE** : Éliminez toutes les unités ennemies pour remporter la victoire.
- **PVP** : Contrôlez vos unités et battez l'adversaire.

## Architecture du Code
Le code est structuré en plusieurs modules pour garantir la lisibilité et la modularité.

- **`main.py`** : Point d'entrée du jeu.
- **`game.py`** : Logique principale du jeu (gestion des tours, conditions de victoire/défaite).
- **`board.py`** : Gère le plateau, ses cellules et les interactions entre unités.
- **`cell.py`** : Représente une cellule avec ses propriétés (traversable, type, unité présente).
- **`unit.py`** : Définit les unités et leurs actions (déplacement, attaque, compétences).
- **`skill.py`** : Implémente les différentes compétences (attaque, soin, buff, debuff).
- **`wall.py`, `river.py`, `bush.py`** : Modules pour la génération et l'affichage des obstacles.
- **`startpage.py`, `winscreen.py`** : Interfaces graphiques pour les écrans de démarrage et de fin de jeu.

### Diagramme UML

Voici le diagramme UML du projet pour visualiser les relations entre les classes :

![Diagramme UML](./game_diagram.png)