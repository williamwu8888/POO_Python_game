import pygame
from cell import Cell

class Board:
    def __init__(self, rows, cols):
        self.cells = [[Cell() for _ in range(cols)] for _ in range(rows)]

    def display(self, screen):
        """Display the board and units on it."""
        for row in range(8):
            for col in range(8):
                pygame.draw.rect(screen, (200, 200, 200), (col * 60, row * 60, 60, 60))  # Cell background
                pygame.draw.rect(screen, (0, 0, 0), (col * 60, row * 60, 60, 60), 2)  # Cell border

                unit = self.cells[row][col].unit
                if unit:
                    unit.draw(screen)

    def add_unit(self, unit):
        """Place a unit on the board at the correct position."""
        self.cells[unit.y][unit.x].unit = unit

    def remove_unit(self, unit):
        """Remove the unit from the board."""
        self.cells[unit.y][unit.x].unit = None
