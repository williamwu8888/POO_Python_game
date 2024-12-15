import pygame
import sys

# Définit les dimensions de l'écran
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720

# Couleurs
BUTTON_COLOR = (0, 128, 128)
BUTTON_HOVER_COLOR = (0, 180, 255)
TEXT_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (255, 248, 220)


def win_screen(result, mode):
    """
    Affiche l'écran de victoire ou de défaite selon le résultat et le mode de jeu.

    :param result: "victory" ou "defeat" selon le résultat du joueur.
    :param mode: "PVP" ou "PVE" selon le mode de jeu.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Résultat du Jeu")

    # Police pour le texte
    font = pygame.font.Font(None, 80)

    # Dimensions des boutons
    button_width = 300
    button_height = 80
    button_spacing = 20

    return_button_x = (SCREEN_WIDTH - button_width) // 2
    return_button_y = SCREEN_HEIGHT // 2 + 50

    restart_button_x = (SCREEN_WIDTH - button_width) // 2
    restart_button_y = return_button_y + button_height + button_spacing

    running = True

    while running:
        screen.fill(BACKGROUND_COLOR)  # Fond noir

        # Afficher le message de victoire ou de défaite
        if mode == "PVE":
            result_text = "Victory!" if result == "victory" else "Defeat!"
        elif mode == "PVP":
            result_text = "Victory of P1!" if result == "victory" else "Victory of P2!"

        result_color = (0, 255, 0) if result == "victory" else (255, 0, 0)
        result_surface = font.render(result_text, True, result_color)
        result_rect = result_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(result_surface, result_rect)

        # Obtenir la position de la souris
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Déterminer si la souris survole les boutons
        is_return_hovered = return_button_x <= mouse_x <= return_button_x + button_width and return_button_y <= mouse_y <= return_button_y + button_height
        is_restart_hovered = restart_button_x <= mouse_x <= restart_button_x + button_width and restart_button_y <= mouse_y <= restart_button_y + button_height

        # Dessiner les boutons
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR if is_return_hovered else BUTTON_COLOR, (return_button_x, return_button_y, button_width, button_height))
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR if is_restart_hovered else BUTTON_COLOR, (restart_button_x, restart_button_y, button_width, button_height))

        # Ajouter du texte aux boutons
        button_font = pygame.font.Font(None, 50)

        return_text = button_font.render("Return to Menu", True, TEXT_COLOR)
        return_text_rect = return_text.get_rect(center=(return_button_x + button_width // 2, return_button_y + button_height // 2))
        screen.blit(return_text, return_text_rect)

        restart_text = button_font.render("Restart", True, TEXT_COLOR)
        restart_text_rect = restart_text.get_rect(center=(restart_button_x + button_width // 2, restart_button_y + button_height // 2))
        screen.blit(restart_text, restart_text_rect)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_return_hovered:
                    return "menu"  # Retourne au menu principal
                elif is_restart_hovered:
                    return "restart"  # Redémarre le jeu

        pygame.display.flip()

if __name__ == "__main__":
    # Exemple d'appel pour tester le fonctionnement
    result = win_screen("Defeat", "PVP")
    print(f"Action sélectionnée : {result}")
