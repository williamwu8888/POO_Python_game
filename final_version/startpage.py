import pygame
import sys

# Définit les dimensions de l'écran
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720

# Couleurs
WHITE = (255, 255, 255)
BUTTON_COLOR = (0, 128, 128)
BUTTON_HOVER_COLOR = (0, 180, 255)
TEXT_COLOR = (255, 255, 255)

# Charger les images
BACKGROUND_IMAGE_PATH = "unit_icons/startpage.jpg"  # Chemin vers votre image de fond

def start_screen():
    """Affiche l'écran de démarrage avec un bouton interactif pour commencer le jeu."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Start Screen")

    # Charger l'image de fond
    background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Police pour le texte
    font = pygame.font.Font(None, 50)

    # Dimensions du bouton
    button_width = 200
    button_height = 80
    button_x = (SCREEN_WIDTH - button_width) // 2
    button_y = (SCREEN_HEIGHT - button_height) // 2

    # Boucle principale
    running = True
    while running:
        screen.blit(background_image, (0, 0))  # Dessiner l'image de fond

        # Obtenir la position de la souris
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Déterminer si la souris survole le bouton
        is_hovered = button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height

        # Dessiner le bouton
        button_color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))

        # Ajouter du texte au bouton
        text = font.render("Start Game", True, TEXT_COLOR)
        text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(text, text_rect)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and is_hovered:
                running = False  # Quitte l'écran de démarrage pour lancer le jeu

        pygame.display.flip()

    return True  # Indique que l'utilisateur a cliqué sur le bouton pour commencer le jeu
