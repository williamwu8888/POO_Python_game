import random
import pygame
from board import Board
from unit import *
from skill import *
from board import GRID_ROWS, GRID_COLS, CELL_SIZE
from wall import generate_walls, draw_walls

class Game:
    def __init__(self, screen, mode='PVE'):
        self.screen = screen
        self.mode = mode  # Ajout pour différencier les modes PVP et PVE

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

        # Ajouter des unités pour l'ennemi ou le second joueur
        self.enemy_units = [
            WarriorUnit(GRID_COLS - 1, GRID_ROWS - 4, 'enemy' if mode == 'PVE' else 'player2'),
            KnightUnit(GRID_COLS - 1, GRID_ROWS - 5, 'enemy' if mode == 'PVE' else 'player2'),
            ArcherUnit(GRID_COLS - 1, GRID_ROWS - 6, 'enemy' if mode == 'PVE' else 'player2'),
            MageUnit(GRID_COLS - 1, GRID_ROWS - 7, 'enemy' if mode == 'PVE' else 'player2'),
            HealerUnit(GRID_COLS - 1, GRID_ROWS - 8, 'enemy' if mode == 'PVE' else 'player2'),
            SupportUnit(GRID_COLS - 1, GRID_ROWS - 9, 'enemy' if mode == 'PVE' else 'player2')
        ]

        # Générer les murs
        self.walls = generate_walls(
            self.board,
            [(unit.x, unit.y) for unit in self.player_units],
            [(unit.x, unit.y) for unit in self.enemy_units])

        # Ajouter les unités au plateau
        for unit in self.player_units + self.enemy_units:
            self.board.add_unit(unit)

        self.current_team = 'player'  # Débuter avec le joueur 1

    def flip_display(self):
        """Mettre à jour l'affichage du jeu."""
        self.screen.fill((0, 0, 0))  # Fond noir
        self.board.display(self.screen)  # Affiche le plateau
        draw_walls(self.screen, self.walls, CELL_SIZE)  # Affiche les murs
        pygame.display.flip()  # Met à jour l'écran

    def handle_turn(self):
        """Gérer le tour basé sur le mode."""
        if self.mode == 'PVE':
            self.handle_player_turn()  # Gérer le tour du joueur
            self.handle_enemy_turn()  # Gérer le tour de l'IA
        elif self.mode == 'PVP':
            if self.current_team == 'player':
                self.handle_player_turn()
                self.current_team = 'player2'
            elif self.current_team == 'player2':
                self.handle_team_turn(self.enemy_units)  # P2 utilise les mêmes touches que P1
                self.current_team = 'player'

    def handle_player_turn(self):
        """Gérer le tour des joueurs."""
        self.handle_team_turn(self.player_units)

    def handle_team_turn(self, team_units):
        """Gérer le tour d'une équipe donnée."""
        for selected_unit in team_units:
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
                                (0, 255, 0),  # Vert pour la position actuelle
                                (current_x * CELL_SIZE, current_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                                2
                            )
                            pygame.display.flip()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        if self.board.is_traversable(current_x, current_y):
                            self.board.remove_unit(selected_unit)
                            selected_unit.x, selected_unit.y = current_x, current_y
                            self.board.add_unit(selected_unit)
                            self.flip_display()
                            has_acted = True
                            selected_unit.is_selected = False

    def handle_enemy_turn(self):
        """Gérer le tour de l'ennemi dans le mode PVE."""
        for enemy in self.enemy_units:
            if enemy.stunned:
                enemy.end_turn()
                continue

            # Sélectionner une cible
            target = random.choice(self.player_units)

            # Calculer le nombre de déplacements restant
            moves_left = enemy.speed

            while moves_left > 0:
                dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
                dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0

                new_x = enemy.x + dx
                new_y = enemy.y + dy

                # Vérifier si l'emplacement est traversable
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
                    break

        # Attaquer la cible si elle est à portée
        if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
            enemy.attack(target, self)
            self.flip_display()
            if target.health <= 0:
                self.player_units.remove(target)
                self.board.remove_unit(target)

    def display_movement_radius(self, unit, radius):
        """Afficher le rayon de mouvement possible d'une unité."""
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                target_x = unit.x + dx
                target_y = unit.y + dy
                distance = abs(dx) + abs(dy)
                if self.board.is_traversable(target_x, target_y) and distance <= radius:
                    pygame.draw.rect(
                        self.screen,
                        (100, 100, 255),  # Bleu pour les cases accessibles
                        (target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                        2
                    )
