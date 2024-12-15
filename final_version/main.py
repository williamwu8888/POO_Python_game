import pygame
from game import Game, GameOver
from startpage import start_screen
import sys
from board import GRID_ROWS, GRID_COLS, CELL_SIZE
from winscreen import win_screen

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((GRID_COLS * CELL_SIZE, GRID_ROWS * CELL_SIZE))
pygame.display.set_caption("Jeu de stratégie")


# Boucle principale
def main_loop(mode="PVE"):  # Ajout d'un paramètre pour le mode
    game = Game(screen, mode)  # Transmet le mode à l'instance du jeu
    running = True
    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            # Gérer les tours selon le mode
            game.handle_turn()

            # Affichage du jeu
            game.flip_display()

        except GameOver as e:
            result = win_screen(e.result, mode) 
            if result == "menu":
                selected_mode = start_screen()
                game = Game(screen, selected_mode)
            elif result == "restart":
                game = Game(screen, mode)


        # Affichage
        game.flip_display()


# Lancer le jeu
if __name__ == "__main__":
    # Obtenir le mode de jeu depuis l'écran de démarrage
    selected_mode = start_screen()
    if selected_mode:
        main_loop(selected_mode)
