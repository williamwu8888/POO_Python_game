import pygame
import random
from board import GRID_ROWS, GRID_COLS

class Wall:
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.traversable = False  # Walls are not traversable
        board.cells[y][x].type = 'wall'
        board.cells[y][x].traversable = False  # Ensure the cell also marks non-traversable



def generate_walls(board, player_positions, enemy_positions):
    safe_radius = 2
    walls = []

    def is_safe_position(x, y, positions):
        for px, py in positions:
            if abs(px - x) <= safe_radius and abs(py - y) <= safe_radius:
                return True
        return False

    all_units_positions = player_positions + enemy_positions

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            if board.cells[row][col].unit is not None or is_safe_position(col, row, all_units_positions):
                continue
            if random.random() < 0.15:  # Adjust probability as needed
                board.cells[row][col].type = "wall"
                board.cells[row][col].traversable = False
                walls.append(Wall(col, row, board))  # Pass the board here

    return walls


def ensure_connectivity(board):
    """
    Vérifie que la carte reste connectée et traversable. Supprime des murs si nécessaire.
    """
    visited = [[False for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

    def dfs(x, y):
        """Parcours en profondeur pour vérifier la connectivité."""
        if x < 0 or x >= GRID_COLS or y < 0 or y >= GRID_ROWS:
            return
        if visited[y][x] or board.cells[y][x].type == "wall":
            return
        visited[y][x] = True
        # Parcourir les voisins
        dfs(x + 1, y)
        dfs(x - 1, y)
        dfs(x, y + 1)
        dfs(x, y - 1)

    # Trouver une case de départ non murée
    start_x, start_y = None, None
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            if board.cells[row][col].type != "wall":
                start_x, start_y = col, row
                break
        if start_x is not None:
            break

    # Effectuer le DFS
    if start_x is not None and start_y is not None:
        dfs(start_x, start_y)

    # Supprimer les murs bloquants
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            if board.cells[row][col].type == "wall" and not visited[row][col]:
                board.cells[row][col].type = "empty"

def draw_walls(screen, walls, cell_size):
    for wall in walls:
        if not wall.traversable:  # Only draw walls that are not traversable
            pygame.draw.rect(
                screen,
                (50, 50, 50),  # Dark gray color for walls
                (wall.x * cell_size, wall.y * cell_size, cell_size, cell_size)
            )

