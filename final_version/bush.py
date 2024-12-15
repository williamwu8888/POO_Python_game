import pygame
import random
from board import GRID_ROWS, GRID_COLS

class Bush:
    """
    Représente un buisson dans le jeu.
    """
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        board.cells[y][x].type = 'bush'
        board.cells[y][x].traversable = True  # Les buissons sont toujours traversables

def generate_bushes(board, player_positions, enemy_positions, walls, rivers):
    """
    Génère des buissons tout en évitant les murs, les rivières et les unités.
    """
    safe_radius = 1  # Rayon de sécurité autour des unités, murs et rivières
    bushes = []

    def is_safe_position(x, y, positions):
        """
        Vérifie si une cellule est sûre pour placer un buisson.
        """
        if board.cells[y][x].type in ['wall', 'river', 'bush']:
            return False  # Évite les collisions avec d'autres entités
        for px, py in positions:
            if abs(px - x) <= safe_radius and abs(py - y) <= safe_radius:
                return False  # Trop proche des entités
        return True

    all_units_positions = player_positions + enemy_positions
    occupied_positions = walls + rivers

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            if not is_safe_position(col, row, all_units_positions + occupied_positions):
                continue
            # Avec une probabilité de 25%, placer un buisson
            if random.random() < 0.25:
                bushes.append(Bush(col, row, board))

    return bushes

def draw_bushes(screen, board, cell_size):
    """
    Dessine les buissons sur le plateau.
    """
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            cell = board.cells[row][col]
            if cell.type == 'bush':
                pygame.draw.rect(
                    screen,
                    (34, 139, 34),  # Vert pour les buissons
                    (col * cell_size, row * cell_size, cell_size, cell_size)
                )
