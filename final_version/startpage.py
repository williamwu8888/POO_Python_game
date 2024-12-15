import pygame
import sys

# Définit les dimensions de l'écran
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720

# Couleurs
NOIR = (238, 180, 34)
BUTTON_COLOR = (0, 128, 128)
BUTTON_HOVER_COLOR = (0, 180, 255)
TEXT_COLOR = (255, 255, 255)

# Charger les images
BACKGROUND_IMAGE_PATH = "unit_icons/startpage.jpg"  # Chemin vers votre image de fond


def start_screen():
    """Affiche l'écran de démarrage avec des boutons interactifs."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Notre Jeu de stratégie")

    # Charger l'image de fond
    background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Police pour le texte
    font = pygame.font.Font(None, 50)

    # Dimensions des boutons
    button_width = 200
    button_height = 80

    start_button_x = (SCREEN_WIDTH - button_width) // 2
    start_button_y = (SCREEN_HEIGHT - button_height) // 2 - 100

    options_button_x = (SCREEN_WIDTH - button_width) // 2
    options_button_y = start_button_y + 150

    # Boucle principale
    running = True
    selected_mode = "PVE"  # Par défaut, le mode est PVE
    while running:
        screen.blit(background_image, (0, 0))  # Dessiner l'image de fond

        # Ajouter le titre
        title_font = pygame.font.Font(None, 80)
        title_text = title_font.render("NOTRE JEU DE STRATEGIE", True, NOIR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # Obtenir la position de la souris
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Déterminer si la souris survole les boutons
        is_start_hovered = start_button_x <= mouse_x <= start_button_x + button_width and start_button_y <= mouse_y <= start_button_y + button_height
        is_options_hovered = options_button_x <= mouse_x <= options_button_x + button_width and options_button_y <= mouse_y <= options_button_y + button_height

        # Dessiner les boutons
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR if is_start_hovered else BUTTON_COLOR, (start_button_x, start_button_y, button_width, button_height))
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR if is_options_hovered else BUTTON_COLOR, (options_button_x, options_button_y, button_width, button_height))

        # Ajouter du texte aux boutons
        start_text = font.render("Start", True, TEXT_COLOR)
        start_text_rect = start_text.get_rect(center=(start_button_x + button_width // 2, start_button_y + button_height // 2))
        screen.blit(start_text, start_text_rect)

        options_text = font.render("Options", True, TEXT_COLOR)
        options_text_rect = options_text.get_rect(center=(options_button_x + button_width // 2, options_button_y + button_height // 2))
        screen.blit(options_text, options_text_rect)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_start_hovered:
                    running = False  # Quitte l'écran de démarrage pour lancer le jeu
                elif is_options_hovered:
                    selected_mode = options_menu(screen, background_image, font)
                    print(f"Mode sélectionné : {selected_mode}")

        pygame.display.flip()

    return selected_mode  # Retourne le mode choisi


def options_menu(screen, background_image, font):
    """Affiche un menu des options pour choisir entre PVP et PVE."""
    button_width = 200
    button_height = 80

    pvp_button_x = (SCREEN_WIDTH - button_width) // 2 - 150
    pvp_button_y = (SCREEN_HEIGHT - button_height) // 2

    pve_button_x = (SCREEN_WIDTH - button_width) // 2 + 150
    pve_button_y = (SCREEN_HEIGHT - button_height) // 2

    running = True
    selected_mode = "PVE"  # Par défaut

    while running:
        screen.blit(background_image, (0, 0))  # Dessiner l'image de fond

        # Ajouter le titre
        title_font = pygame.font.Font(None, 80)
        title_text = title_font.render("Options", True, NOIR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # Obtenir la position de la souris
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Déterminer si la souris survole les boutons
        is_pvp_hovered = pvp_button_x <= mouse_x <= pvp_button_x + button_width and pvp_button_y <= mouse_y <= pvp_button_y + button_height
        is_pve_hovered = pve_button_x <= mouse_x <= pve_button_x + button_width and pve_button_y <= mouse_y <= pve_button_y + button_height

        # Dessiner les boutons
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR if is_pvp_hovered else BUTTON_COLOR, (pvp_button_x, pvp_button_y, button_width, button_height))
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR if is_pve_hovered else BUTTON_COLOR, (pve_button_x, pve_button_y, button_width, button_height))

        # Ajouter du texte aux boutons
        pvp_text = font.render("PVP", True, TEXT_COLOR)
        pvp_text_rect = pvp_text.get_rect(center=(pvp_button_x + button_width // 2, pvp_button_y + button_height // 2))
        screen.blit(pvp_text, pvp_text_rect)

        pve_text = font.render("PVE", True, TEXT_COLOR)
        pve_text_rect = pve_text.get_rect(center=(pve_button_x + button_width // 2, pve_button_y + button_height // 2))
        screen.blit(pve_text, pve_text_rect)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_pvp_hovered:
                    selected_mode = "PVP"
                    running = False
                elif is_pve_hovered:
                    selected_mode = "PVE"
                    running = False

        pygame.display.flip()

    return selected_mode  # Retourne le mode choisi
