# "NOM DU JEU"

Un jeu de stratégie en 2D avec des mécaniques de plateau, où le joueur contrôle des unités qui se déplacent et attaquent dans un environnement dynamique. Le jeu est développé en Python en utilisant Pygame pour la gestion graphique.

## Table des Matières
- [Contributeurs](#contributeurs)
- [Aperçu du Jeu](#aperçu-du-jeu)
- [Fonctionnalités](#fonctionnalités)
- [Utilisation](#utilisation)
- [Gameplay](#gameplay)
- [Architecture du Code](#architecture-du-code)
- [Contribuer](#contribuer)

## Contributeurs
Étudiants de Sorbonne Université Sciences dans le cadre d'un projet pédagogique dans l'unité d'enseignement de Programmation Orientée Objet en Python.
Master 1 - Ingénierie pour la Santé, Systèmes Mécatroniques pour la Réhabilitation (M1-IPS SMR).

### Liste des contributeurs : 
- GUERRERO ESCOBAR Fabian: fabian.guerrero_escobar@sorbonne-universite.fr
- LIU Kaiyu: kaiyu.liu@sorbonne-universite.fr
- WU William: william.wu@sorbonne-universite.fr

### Encadrants universitaires: 
- Louis ANNABI: louis.annabi@sorbonne-universite.fr
- Ramy ISKANDER, ramy.iskander@sorbonne-universite.fr

## Aperçu du Jeu
Capture d'écran ou GIF animé montrant le jeu en action, si possible.

## Fonctionnalités
- **Tour par tour** : Le jeu se déroule sur des tours où chaque joueur et chaque ennemi agissent à leur tour.
- **Système de points de vie et de dégâts** : Les unités ont des points de vie, et chaque attaque inflige des dégâts calculés selon la défense et l'attaque.
- **Différents types de personnages ou unités** : Chaque unité a des compétences spécifiques, des points de vie et des capacités de déplacement.
- **Interface utilisateur basique** : Affichage du plateau de jeu et des unités, avec des informations sur les points de vie.
- **Modes de jeu** : Joueur contre IA, avec des ennemis contrôlés par une IA simple.

## Utilisation
### Lancer le Jeu
Pour démarrer le jeu, exécutez le fichier `main.py`. Il est nécessaire d'avoir Pygame installé.

```bash
pip install pygame
```

Ensuite, lancez le jeu avec la commande suivante :
```bash
python main.py
```

## Gameplay
Le jeu se joue sur un plateau de 8x8 cases. Le joueur contrôle des unités avec différentes compétences, comme les attaques à distance ou de mêlée.

### Commandes :
- **Déplacement** : Utilisez les touches fléchées pour déplacer votre personnage.
- **Attaquer** : Appuyez sur la touche `Espace` pour valider un déplacement et accéder à un menu de compétences.
- **Compétences** : Choisissez une compétence via les touches numériques (`1`, `2`, etc.) pour attaquer les ennemis.
- **Quitter** : Fermez la fenêtre pour quitter le jeu.

## Architecture du Code
Le jeu est organisé en plusieurs fichiers Python, chacun ayant une responsabilité spécifique :

- **`main.py`** : Point d'entrée principal du jeu. Gère l'affichage et le cycle de jeu.
- **`game.py`** : Contient la logique du jeu, comme la gestion des tours du joueur et des ennemis, ainsi que l'application des compétences.
- **`board.py`** : Gère le plateau de jeu, les cellules et les unités présentes sur chaque case.
- **`cell.py`** : Représente chaque cellule du plateau, avec des informations sur son type et l'unité qui y est présente.
- **`unit.py`** : Définit la classe `Unit`, qui représente une unité sur le terrain, avec ses points de vie, son attaque, sa défense et ses compétences.
- **`skill.py`** : Contient les compétences des unités, leur utilisation et leurs effets sur les ennemis.

### Description des classes principales :
- **`Unit`** : Les unités ont des attributs comme la santé, la défense, l'attaque, la vitesse et les compétences. Elles peuvent se déplacer sur le plateau et attaquer d'autres unités.
- **`Skill`** : Chaque compétence a un pouvoir, une portée, une précision et un effet de zone.
- **`Board`** : Le plateau est une grille de cellules, où chaque cellule peut contenir une unité ou être vide. Certaines cellules peuvent être spéciales, comme des cellules d'eau ou de lave.
  
### Exemple de diagramme UML
Un diagramme UML peut être ajouté ici pour visualiser la structure du code.