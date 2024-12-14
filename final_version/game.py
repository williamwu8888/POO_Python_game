import random
import pygame
from board import Board
from unit import *
from skill import *

from board import GRID_ROWS, GRID_COLS, CELL_SIZE
from wall import generate_walls, draw_walls
# Dans game.py

class Game:
    def __init__(self, screen):
        self.screen = screen

        # Créer un plateau basé sur les dimensions globales
        self.board = Board(GRID_ROWS, GRID_COLS)

        # Ajouter des unités pour le joueur
        self.player_units = [
            WarriorUnit(0, (GRID_ROWS-6)//2, 'player'),
            KnightUnit(0, (GRID_ROWS-6)//2 + 1, 'player'),
            ArcherUnit(0, (GRID_ROWS-6)//2 +2, 'player'),
            MageUnit(0, (GRID_ROWS-6)//2 +3, 'player'),
            HealerUnit(0, (GRID_ROWS-6)//2 +4, 'player'),
            SupportUnit(0, (GRID_ROWS-6)//2 +5, 'player')
        ]

        # Ajouter des unités pour l'ennemi
        self.enemy_units = [
            WarriorUnit(GRID_COLS - 1, (GRID_ROWS-6)//2, 'enemy'),
            KnightUnit(GRID_COLS - 1, (GRID_ROWS-6)//2 +1, 'enemy'),
            ArcherUnit(GRID_COLS - 1, (GRID_ROWS-6)//2 +2, 'enemy'),
            MageUnit(GRID_COLS - 1, (GRID_ROWS-6)//2 +3, 'enemy'),
            HealerUnit(GRID_COLS - 1, (GRID_ROWS-6)//2 +4, 'enemy'),
            SupportUnit(GRID_COLS - 1, (GRID_ROWS-6)//2 +5, 'enemy')
        ]

        # Générer les murs
        self.walls = generate_walls(
            self.board,
            [(unit.x, unit.y) for unit in self.player_units],
            [(unit.x, unit.y) for unit in self.enemy_units])

        # Ajouter les unités au plateau
        for unit in self.player_units + self.enemy_units:
            self.board.add_unit(unit)

    def get_available_skills(self, unit):
        """Vérifie quelles compétences ont des cibles à portée."""
        available_skills = []
        for skill in unit.skills:
            # Vérifie si au moins un ennemi est à portée de la compétence
            has_target = any(
                abs(unit.x - enemy.x) + abs(unit.y - enemy.y) <= skill.range
                for enemy in self.enemy_units
            )
            if has_target:
                available_skills.append(skill)
        return available_skills

    def handle_player_turn(self):
        """Gère le tour du joueur avec sélection manuelle de la compétence et attaque au clavier."""
        for selected_unit in self.player_units:
            if selected_unit.stunned:
                print(f"{selected_unit.team} unit is stunned and cannot act this turn.")
                selected_unit.end_turn()  # Fin du tour, réinitialiser le stun
                continue

            has_acted = False
            moves_left = selected_unit.speed
            selected_unit.is_selected = True
            current_x, current_y = selected_unit.x, selected_unit.y  # Position temporaire
            self.flip_display()

            while not has_acted:
                for event in pygame.event.get():
                    self.display_movement_radius(selected_unit, moves_left)
                    pygame.draw.rect(
                        self.screen,
                        (0, 255, 0),  # Vert pour la position temporaire
                        (current_x * CELL_SIZE, current_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                        2
                    )
                    pygame.display.flip()

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        # Calculer la nouvelle position temporaire
                        new_x = current_x + dx
                        new_y = current_y + dy
                        distance = abs(new_x - selected_unit.x) + abs(new_y - selected_unit.y)

                        if self.board.is_traversable(new_x, new_y,current_x, current_y) and distance <= moves_left:
                            print(f"Moving to ({new_x}, {new_y})")
                            current_x, current_y = new_x, new_y
                            self.flip_display()
                            self.display_movement_radius(selected_unit, moves_left)
                        else:
                            print(f"Cannot move to ({new_x}, {new_y}): traversable={self.board.is_traversable(new_x, new_y,current_x, current_y)}")
                            new_x,new_y = current_x,current_y #Returner la position cible à la position actuelle pour éviter de pas pouvoir se bouger


                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        # Confirmant que la position cible n'est pas un mur
                        if self.board.is_another_unit(current_x, current_y,selected_unit):
                            self.board.remove_unit(selected_unit)
                            selected_unit.x, selected_unit.y = current_x, current_y
                            self.board.add_unit(selected_unit)
                            self.flip_display()

                            available_skills = self.get_available_skills(selected_unit)
                            if available_skills:
                                chosen_skill = self.display_skill_menu(selected_unit, available_skills)
                                if chosen_skill.name != "Heal":
                                    # Filtrer les ennemis dans la portée
                                    attackable_targets = self.get_attackable_targets(selected_unit)

                                    if attackable_targets:
                                        # Affiche la portée d'attaque
                                        self.display_attack_radius(selected_unit, chosen_skill.range)

                                        # Attente du joueur pour choisir la cible (au clavier)
                                        target_chosen = False
                                        current_target_idx = 0  # Index du curseur de la cible sélectionnée

                                        # Filtrer les ennemis à portée
                                        valid_targets = [target for target in attackable_targets
                                                        if abs(target[0] - selected_unit.x) + abs(target[1] - selected_unit.y) <= chosen_skill.range]

                                        # Afficher les ennemis à portée
                                        while not target_chosen:
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:
                                                    pygame.quit()
                                                    exit()

                                                if event.type == pygame.KEYDOWN:
                                                    # Déplacer le curseur sur les cibles à portée
                                                    if event.key == pygame.K_DOWN:
                                                        current_target_idx = (current_target_idx + 1) % len(valid_targets)
                                                    elif event.key == pygame.K_UP:
                                                        current_target_idx = (current_target_idx - 1) % len(valid_targets)

                                                    # Sélectionner une cible avec K_1
                                                    if event.key == pygame.K_1:
                                                        target_x, target_y = valid_targets[current_target_idx]
                                                        target_unit = self.board.cells[target_y][target_x].unit
                                                        if target_unit:
                                                            print(f"Using {chosen_skill.name} on {target_unit.team} unit.")
                                                            chosen_skill.use(selected_unit, target_unit, self)
                                                            target_chosen = True
                                                            self.flip_display()

                                            # Redessiner la portée avec la cible sélectionnée
                                            self.display_attack_radius(selected_unit, chosen_skill.range)
                                            pygame.draw.rect(
                                                self.screen,
                                                (0, 0, 255),  # Bleu pour indiquer la cible sélectionnée
                                                (valid_targets[current_target_idx][0] * CELL_SIZE,
                                                valid_targets[current_target_idx][1] * CELL_SIZE,
                                                CELL_SIZE, CELL_SIZE),
                                                3  # Épaisseur du contour pour le curseur
                                            )
                                            pygame.display.flip()
                                elif chosen_skill.name == "Heal":
                                    # Filtrer les ennemis dans la portée
                                    heal_targets = self.get_heal_targets(selected_unit)

                                    if attackable_targets:
                                        # Affiche la portée pour être gueris
                                        self.display_attack_radius(selected_unit, chosen_skill.range)

                                        # Attente du joueur pour choisir la cible (au clavier)
                                        target_chosen = False
                                        current_target_idx = 0  # Index du curseur de la cible sélectionnée

                                        # Filtrer les allies à portée
                                        valid_targets = [target for target in heal_targets
                                                        if abs(target[0] - selected_unit.x) + abs(target[1] - selected_unit.y) <= chosen_skill.range]

                                        # Afficher les allies à portée
                                        while not target_chosen:
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:
                                                    pygame.quit()
                                                    exit()

                                                if event.type == pygame.KEYDOWN:
                                                    # Déplacer le curseur sur les cibles à portée
                                                    if event.key == pygame.K_DOWN:
                                                        current_target_idx = (current_target_idx + 1) % len(valid_targets)
                                                    elif event.key == pygame.K_UP:
                                                        current_target_idx = (current_target_idx - 1) % len(valid_targets)

                                                    # Sélectionner une cible avec K_1
                                                    if event.key == pygame.K_1:
                                                        target_x, target_y = valid_targets[current_target_idx]
                                                        target_unit = self.board.cells[target_y][target_x].unit
                                                        if target_unit:
                                                            print(f"Using {chosen_skill.name} on {target_unit.team} unit.")
                                                            chosen_skill.use(selected_unit, target_unit, self)
                                                            target_chosen = True
                                                            self.flip_display()

                                            # Redessiner la portée avec la cible sélectionnée
                                            self.display_attack_radius(selected_unit, chosen_skill.range)
                                            pygame.draw.rect(
                                                self.screen,
                                                (0, 0, 255),  # Bleu pour indiquer la cible sélectionnée
                                                (valid_targets[current_target_idx][0] * CELL_SIZE,
                                                valid_targets[current_target_idx][1] * CELL_SIZE,
                                                CELL_SIZE, CELL_SIZE),
                                                3  # Épaisseur du contour pour le curseur
                                            )
                                            pygame.display.flip()

                                else:
                                    print("No skills available.")
                            has_acted = True
                            selected_unit.is_selected = False
                        else:
                            print("Cannot move to wall position!")

            # Vérifier les conditions de victoire/défaite
            if not self.enemy_units:
                break

    def handle_enemy_turn(self):
        """Simple AI for enemies."""
        for enemy in self.enemy_units:
            if enemy.stunned:
                print(f"{enemy.team} unit is stunned and cannot act this turn.")
                enemy.end_turn()  # Fin du tour, réinitialiser le stun
                continue
            # Vérifie qu'il reste des cibles disponibles
            if not self.player_units:
                print("L'IA a gagné, toutes les unités du joueur sont vaincues !")
                return

            # Sélectionne une cible valide
            target = random.choice(self.player_units)

            # Se rapproche de la cible dans les limites de la vitesse
            moves_left = enemy.speed
            while moves_left > 0:
                dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
                dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0

                # Vérifie si le mouvement est valide
                distance = abs(dx) + abs(dy)
                new_x = enemy.x + dx
                new_y = enemy.y + dy

                if (0 <= new_x < GRID_COLS and
                    0 <= new_y < GRID_ROWS and
                    self.board.cells[new_y][new_x].type != "wall" and
                    self.board.cells[new_y][new_x].unit is None):
                    self.board.remove_unit(enemy)
                    enemy.x, enemy.y = new_x, new_y
                    self.board.add_unit(enemy)
                    moves_left -= 1
                    self.flip_display()
                else:
                    # Si le mouvement n'est pas valide, casse la boucle
                    break

            # Vérifie si l'ennemi est adjacent à la cible pour attaquer
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target, self)  # Passe le jeu pour gérer les unités mortes
                self.flip_display()

                # Si la cible est morte, retire-la
                if target.health <= 0:
                    print(f"{target.team} unit defeated!")
                    self.player_units.remove(target)
                    self.board.remove_unit(target)
            
            # Vérifier les conditions de victoire/défaite
            if not self.player_units:
                break

    def get_attackable_targets(self, unit):
        """Retourne les cases où l'unité peut attaquer (en fonction des compétences)."""
        attackable_targets = []
        for skill in unit.skills:
            # Utiliser la portée de la compétence, pas de l'unité
            range_ = skill.range
            for dx in range(-range_, range_ + 1):  # Vérifie la portée de l'attaque
                for dy in range(-range_, range_ + 1):
                    target_x = unit.x + dx
                    target_y = unit.y + dy
                    if (0 <= target_x < GRID_COLS and 0 <= target_y < GRID_ROWS):
                        # Vérifie si une unité ennemie se trouve sur la case
                        target_unit = self.board.cells[target_y][target_x].unit
                        if target_unit and target_unit.team != unit.team:
                            attackable_targets.append((target_x, target_y))
        return attackable_targets
    
    def get_heal_targets(self, unit):
        """Retourne les cases où l'unité peut gueri."""
        heal_targets = []
        for skill in unit.skills:
            # Utiliser la portée de la compétence, pas de l'unité
            range_ = skill.range
            for dx in range(-range_, range_ + 1):  # Vérifie la portée de l'attaque
                for dy in range(-range_, range_ + 1):
                    target_x = unit.x + dx
                    target_y = unit.y + dy
                    if (0 <= target_x < GRID_COLS and 0 <= target_y < GRID_ROWS):
                        # Vérifie si une unité allie se trouve sur la case
                        target_unit = self.board.cells[target_y][target_x].unit
                        if target_unit and target_unit.team == unit.team:
                            heal_targets.append((target_x, target_y))
        return heal_targets

    def display_attack_radius(self, unit, radius):
        """Affiche les cases accessibles autour de l'unité sélectionnée, mais seulement celles occupées par des ennemis."""

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                target_x = unit.x + dx
                target_y = unit.y + dy
                distance = abs(dx) + abs(dy)

                # Vérifie si la case cible est dans les limites et dans la portée d'attaque
                if (0 <= target_x < GRID_COLS and
                    0 <= target_y < GRID_ROWS and
                    distance <= radius):
                    
                    target_unit = self.board.cells[target_y][target_x].unit

                    # Vérifie si la case contient une unité ennemie
                    if target_unit and target_unit.team != unit.team:
                        # Dessiner un contour pour les cases contenant une cible ennemie
                        pygame.draw.rect(
                            self.screen,
                            (255, 0, 0),  # Rouge pour indiquer les cibles ennemies à portée
                            (target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                            2  # Épaisseur du contour
                        )

    def display_movement_radius(self, unit, radius):
        """Affiche les cases accessibles autour de l'unité sélectionnée."""
        
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                target_x = unit.x + dx
                target_y = unit.y + dy
                distance = abs(dx) + abs(dy)

                # Vérifie si la case cible est dans les limites et accessible
                if (0 <= target_x < GRID_COLS and
                    0 <= target_y < GRID_ROWS and
                    distance <= radius and
                    self.board.cells[target_y][target_x].type != "obstacle" and
                    self.board.cells[target_y][target_x].unit is None):
                    
                    # Dessiner un contour pour les cases accessibles
                    pygame.draw.rect(
                        self.screen,
                        (100, 100, 255),  # Couleur bleue pour indiquer les cases accessibles
                        (target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                        2  # Épaisseur du contour
                    )

    def display_skill_menu(self, unit, available_skills):
        """Affiche un menu pour choisir une compétence pour l'unité sélectionnée."""
        print("Choisissez une compétence :")
        for i, skill in enumerate(unit.skills):
            # Vérifie si la compétence a des cibles
            is_available = skill in available_skills
            status = "" if is_available else " (indisponible)"
            print(f"{i + 1}. {skill.name} (Portée : {skill.range}){status}")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # Vérifie si le joueur appuie sur une touche correspondant à un choix
                    if event.key in [pygame.K_1, pygame.K_2]:
                        index = event.key - pygame.K_1  # Convertir K_1 ou K_2 en index
                        if 0 <= index < len(unit.skills):
                            chosen_skill = unit.skills[index]
                            if chosen_skill in available_skills:
                                return chosen_skill
                            else:
                                print("Cette compétence n'est pas disponible.")
                    elif event.key == pygame.K_ESCAPE:
                        return None  # Annuler l'action

    def flip_display(self):
        """Display the game."""
        self.screen.fill((0, 0, 0))  # Black background
        self.board.display(self.screen)
        draw_walls(self.screen, self.walls, CELL_SIZE)
        pygame.display.flip()
