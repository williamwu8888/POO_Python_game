import pygame
from game import Game
from startpage import start_screen
import sys
from board import GRID_ROWS, GRID_COLS, CELL_SIZE

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((GRID_COLS * CELL_SIZE, GRID_ROWS * CELL_SIZE))
pygame.display.set_caption("Jeu de stratégie")


# Boucle principale
def main_loop(mode="PVE"):  # Ajout d'un paramètre pour le mode
    game = Game(screen, mode)  # Transmet le mode à l'instance du jeu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # Gérer les tours selon le mode
        if mode == "PVE":
            game.handle_turn()  # Inclut le tour du joueur et de l'IA
        elif mode == "PVP":
            game.handle_turn()  # Inclut le tour des deux joueurs

        # Vérifier les conditions de victoire/défaite
        if not game.enemy_units:
            print("Victoire !")
            running = False
        elif not game.player_units:
            print("Défaite !")
            running = False

        # Affichage
        game.flip_display()


# Lancer le jeu
if __name__ == "__main__":
    # Obtenir le mode de jeu depuis l'écran de démarrage
    selected_mode = start_screen()
    if selected_mode:
        main_loop(selected_mode)
