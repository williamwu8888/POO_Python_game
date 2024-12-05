import pygame
from cell import Cell

# Dimensions du plateau
GRID_ROWS = 16
GRID_COLS = 16

# Taille des cases
CELL_SIZE = 40

class Board:
    def __init__(self, rows, cols):
        self.cells = [[Cell() for _ in range(cols)] for _ in range(rows)]

    def display(self, screen):
        """Display the board and units on it."""
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                cell_color = (200, 200, 200) if self.cells[row][col].type == "empty" else (50, 50, 50)
                pygame.draw.rect(screen, cell_color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, (0, 0, 0), (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)

                unit = self.cells[row][col].unit
                if unit:
                    unit.draw(screen)

    def add_unit(self, unit):
        """Place a unit on the board at the correct position."""
        self.cells[unit.y][unit.x].unit = unit

    def remove_unit(self, unit):
        """Remove the unit from the board."""
        self.cells[unit.y][unit.x].unit = None
