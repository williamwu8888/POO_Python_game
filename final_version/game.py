import random
import pygame
from board import Board
from unit import WarriorUnit, ArcherUnit, MageUnit
from skill import DamageSkill, HealingSkill, BuffSkill

from board import GRID_ROWS, GRID_COLS, CELL_SIZE

class Game:
    def __init__(self, screen):
        self.screen = screen

        # Créer un plateau basé sur les dimensions globales
        self.board = Board(GRID_ROWS, GRID_COLS)

        # Ajouter des unités pour le joueur et l'ennemi
        self.player_units = [
            WarriorUnit(0, 0, 'player'),
            ArcherUnit(1, 0, 'player'),
            MageUnit(2, 0, 'player')
        ]

        self.enemy_units = [
            WarriorUnit(GRID_COLS - 1, GRID_ROWS - 1, 'enemy'),
            ArcherUnit(GRID_COLS - 2, GRID_ROWS - 1, 'enemy'),
            MageUnit(GRID_COLS - 3, GRID_ROWS - 1, 'enemy')
        ]

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
        """Handle the player's turn."""
        for selected_unit in self.player_units:
            has_acted = False
            moves_left = selected_unit.speed  # Rayon de déplacement
            selected_unit.is_selected = True
            current_x, current_y = selected_unit.x, selected_unit.y  # Position temporaire
            self.flip_display()

            while not has_acted:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # Vérifie que l'événement est un appui sur une touche
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

                        # Vérifie si le mouvement est valide
                        if (0 <= new_x < 8 and 0 <= new_y < 8 and
                            distance <= moves_left and
                            self.board.cells[new_y][new_x].unit is None):
                            current_x, current_y = new_x, new_y  # Met à jour la position temporaire
                            self.flip_display()  # Rafraîchir l'affichage
                            self.display_movement_radius(selected_unit, moves_left)  # Afficher le rayon
                            pygame.draw.rect(
                                self.screen,
                                (0, 255, 0),  # Vert pour la position temporaire
                                (current_x * CELL_SIZE, current_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                                2
                            )
                            pygame.display.flip()

                        # Appuyer sur Espace pour valider le déplacement ou afficher les compétences
                        if event.key == pygame.K_SPACE:
                            # Déplace l'unité vers la position finale
                            self.board.remove_unit(selected_unit)
                            selected_unit.x, selected_unit.y = current_x, current_y
                            self.board.add_unit(selected_unit)
                            self.flip_display()

                            # Vérifie si au moins une compétence a une cible à portée
                            available_skills = self.get_available_skills(selected_unit)
                            if available_skills:
                                # Affiche le menu des compétences
                                chosen_skill = self.display_skill_menu(selected_unit, available_skills)
                                if chosen_skill is not None:
                                    # Appliquer la compétence sur un ennemi à portée
                                    for enemy in self.enemy_units:
                                        distance = abs(selected_unit.x - enemy.x) + abs(selected_unit.y - enemy.y)
                                        if distance <= chosen_skill.range:
                                            chosen_skill.use(selected_unit, enemy, self)
                                            self.flip_display()
                                            break
                            else:
                                print("Aucun ennemi à portée pour aucune compétence.")

                            # Terminer le tour
                            has_acted = True
                            selected_unit.is_selected = False

    def handle_enemy_turn(self):
        """Simple AI for enemies."""
        for enemy in self.enemy_units:
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

                if (0 <= new_x < 8 and 0 <= new_y < 8 and
                    self.board.cells[new_y][new_x].unit is None and distance <= moves_left):
                    # Déplace l'unité ennemie
                    self.board.remove_unit(enemy)
                    enemy.x, enemy.y = new_x, new_y
                    self.board.add_unit(enemy)
                    moves_left -= distance
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


    def display_movement_radius(self, unit, radius):
        """Affiche les cases accessibles autour de l'unité sélectionnée."""
        from board import GRID_ROWS, GRID_COLS, CELL_SIZE  # Importer les dimensions et la taille des cases

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
        pygame.display.flip()
