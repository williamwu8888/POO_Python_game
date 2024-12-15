import pygame
import random
from board import GRID_ROWS, GRID_COLS

class River:
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        board.cells[y][x].type = 'river'
        board.cells[y][x].traversable = False  # Non traversable par défaut
        board.cells[y][x].traversable_for_knight = True  # Propriété spéciale pour les chevaliers

def generate_rivers(board, player_positions, enemy_positions):
    """
    Génère des rivières tout en évitant les murs, les unités amies et ennemies.
    """
    safe_radius = 1  # Rayon de sécurité autour des unités
    rivers = []

    def is_safe_position(x, y, positions):
        """
        Vérifie si une cellule est sûre pour placer une rivière.
        """
        # Vérifier si la cellule est déjà un mur ou une rivière
        if board.cells[y][x].type in ['wall', 'river']:
            return False
        # Vérifier si elle est trop proche des unités
        for px, py in positions:
            if abs(px - x) <= safe_radius and abs(py - y) <= safe_radius:
                return False
        return True

    all_units_positions = player_positions + enemy_positions

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            # Si la cellule est déjà occupée ou proche d'une unité, la sauter
            if not is_safe_position(col, row, all_units_positions):
                continue
            # Avec une probabilité de 10%, placer une rivière
            if random.random() < 0.1:
                rivers.append(River(col, row, board))

    return rivers

def ensure_connectivity(board):
    """
    S'assure que la carte reste connectée en supprimant les rivières qui bloquent le chemin.
    """
    visited = [[False for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

    def dfs(x, y):
        if x < 0 or x >= GRID_COLS or y < 0 or y >= GRID_ROWS:
            return
        if visited[y][x] or board.cells[y][x].type in ['wall', 'river']:
            return
        visited[y][x] = True
        dfs(x + 1, y)
        dfs(x - 1, y)
        dfs(x, y + 1)
        dfs(x, y - 1)

    start_x, start_y = None, None
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            if board.cells[row][col].type == 'empty':
                start_x, start_y = col, row
                break
        if start_x is not None:
            break

    if start_x is not None and start_y is not None:
        dfs(start_x, start_y)

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            if board.cells[row][col].type == 'river' and not visited[row][col]:
                board.cells[row][col].type = 'empty'

def draw_rivers(screen, board, cell_size):
    """
    Dessine les rivières sur le plateau.
    """
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            cell = board.cells[row][col]
            if cell.type == 'river':
                pygame.draw.rect(
                    screen,
                    (0, 0, 255),  # Couleur bleue pour les rivières
                    (col * cell_size, row * cell_size, cell_size, cell_size)
                )
