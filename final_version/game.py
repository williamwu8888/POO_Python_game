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
            WarriorUnit(0, 3, 'player'),
            KnightUnit(0, 4, 'player'),
            ArcherUnit(0, 5, 'player'),
            MageUnit(0, 6, 'player'),
            HealerUnit(0, 7, 'player'),
            SupportUnit(0, 8, 'player')
        ]

        # Ajouter des unités pour l'ennemi
        self.enemy_units = [
            WarriorUnit(GRID_COLS - 1, GRID_ROWS - 4, 'enemy'),
            KnightUnit(GRID_COLS - 1, GRID_ROWS - 5, 'enemy'),
            ArcherUnit(GRID_COLS - 1, GRID_ROWS - 6, 'enemy'),
            MageUnit(GRID_COLS - 1, GRID_ROWS - 7, 'enemy'),
            HealerUnit(GRID_COLS - 1, GRID_ROWS - 8, 'enemy'),
            SupportUnit(GRID_COLS - 1, GRID_ROWS - 9, 'enemy')
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
        """Handle the player's turn."""
        for selected_unit in self.player_units:
            if selected_unit.stunned:
                selected_unit.end_turn()
                continue

            has_acted = False
            moves_left = selected_unit.speed
            selected_unit.is_selected = True
            current_x, current_y = selected_unit.x, selected_unit.y
            self.flip_display()

            while not has_acted:
                for event in pygame.event.get():
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

                        new_x = current_x + dx
                        new_y = current_y + dy
                        distance = abs(new_x - selected_unit.x) + abs(new_y - selected_unit.y)

                        if self.board.is_traversable(new_x, new_y) and distance <= moves_left:
                            current_x, current_y = new_x, new_y
                            self.flip_display()
                            self.display_movement_radius(selected_unit, moves_left)
                            pygame.draw.rect(
                                self.screen,
                                (0, 255, 0),  # Green for current position
                                (current_x * CELL_SIZE, current_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                                2
                            )
                            pygame.display.flip()


                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        # Vérifiez que la cible actuelle n’est pas un mur
                        if self.board.is_traversable(current_x, current_y):
                            self.board.remove_unit(selected_unit)
                            selected_unit.x, selected_unit.y = current_x, current_y
                            self.board.add_unit(selected_unit)
                            self.flip_display()
                            has_acted = True
                            selected_unit.is_selected = False





    def handle_enemy_turn(self):
        """Simple AI for enemies."""
        for enemy in self.enemy_units:
            if enemy.stunned:
                print(f"{enemy.team} unit is stunned and cannot act this turn.")
                enemy.end_turn()
                continue

            if not self.player_units:
                print("L'IA a gagné, toutes les unités du joueur sont vaincues !")
                return

            target = random.choice(self.player_units)
            moves_left = enemy.speed
            while moves_left > 0:
                dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
                dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0

                new_x = enemy.x + dx
                new_y = enemy.y + dy

                if (0 <= new_x < GRID_COLS and
                    0 <= new_y < GRID_ROWS and
                    self.board.cells[new_y][new_x].type != "wall" and  # détection des murs
                    self.board.cells[new_y][new_x].unit is None):
                    self.board.remove_unit(enemy)
                    enemy.x, enemy.y = new_x, new_y
                    self.board.add_unit(enemy)
                    moves_left -= 1
                    self.flip_display()
                else:
                    break

            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target, self)
                self.flip_display()
                if target.health <= 0:
                    print(f"{target.team} unit defeated!")
                    self.player_units.remove(target)
                    self.board.remove_unit(target)



    def display_movement_radius(self, unit, radius):
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                target_x = unit.x + dx
                target_y = unit.y + dy
                distance = abs(dx) + abs(dy)
                
                # Vérifier si l’emplacement cible est à l’intérieur des limites et peut être traversé
                if self.board.is_traversable(target_x, target_y) and distance <= radius:
                    pygame.draw.rect(
                        self.screen,
                        (100, 100, 255),  # Utilisez le bleu pour les cases à déplacer
                        (target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                        2  # Épaisseur du cadre
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
