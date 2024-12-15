import pygame
from cell import Cell

# Dimensions du plateau
GRID_ROWS = 12
GRID_COLS = 20

# Taille des cases
CELL_SIZE = 60

class Board:
    def __init__(self, rows, cols):
        self.cells = [[Cell() for _ in range(cols)] for _ in range(rows)]

    def display(self, screen):
        """Display the board and units on it."""
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                cell_color = (200, 200, 200) if self.cells[row][col].type == "empty" else (50, 50, 50)
                pygame.draw.rect(screen, cell_color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, (0, 0, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

                unit = self.cells[row][col].unit
                if unit:
                    unit.draw(screen)

    def add_unit(self, unit):
        """Place a unit on the board at the correct position."""
        self.cells[unit.y][unit.x].unit = unit

    def remove_unit(self, unit):
        """Remove the unit from the board."""
        self.cells[unit.y][unit.x].unit = None

    def is_traversable(self, x, y, x0, y0, unit=None):
        """
        Vérifie si une cellule est traversable.
        """
        if x < 0 or x >= GRID_COLS or y < 0 or y >= GRID_ROWS:
            return False

        cell = self.cells[y][x]

        # 特殊处理 river 类型
        if cell.type == "river":
            if unit and unit.__class__.__name__ == "KnightUnit":
                return getattr(cell, "traversable_for_knight", False)
            return False  # 对其他单位一律阻止

        # 检查 wall 和其他类型
        if x != x0 or y != y0:
            traversable = cell.type != "wall"
        else:
            traversable = True

        return traversable



    def is_another_unit(self, x, y,selected_unit):
        """
        Vérifie si une cellule est occupable (pas de unite dans la cellule).
        """
        if x < 0 or x >= GRID_COLS or y < 0 or y >= GRID_ROWS:
            print(f"Cell ({x}, {y}): Out of bounds")
            return False
        cell = self.cells[y][x]
        if x != selected_unit.x or y != selected_unit.y:
            occupable = cell.unit is None
        else:
            occupable = True
        print(f"Cell ({x}, {y}): type={cell.type}, unit={cell.unit}, occupable={occupable}")
        return occupable