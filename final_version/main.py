import pygame
from game import Game
import sys
from board import GRID_ROWS, GRID_COLS, CELL_SIZE  # Importer les dimensions et la taille des cases

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((GRID_COLS * CELL_SIZE, GRID_ROWS * CELL_SIZE))
pygame.display.set_caption("Jeu de stratégie")

# Initialisation du jeu
game = Game(screen)

# Boucle principale
def main_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # Tour du joueur
        game.handle_player_turn()

        # Vérifier les conditions de victoire/défaite
        if not game.enemy_units:
            print("Victoire !")
            running = False
        elif not game.player_units:
            print("Défaite !")
            running = False

        # Tour des ennemis
        game.handle_enemy_turn()

        # Affichage
        game.flip_display()

# Lancer le jeu
if __name__ == "__main__":
    main_loop()
