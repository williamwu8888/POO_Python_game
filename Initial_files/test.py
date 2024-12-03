import pygame
import random
import os

# Constants for the game
GRID_SIZE = 16  # Changed to 16x16
CELL_SIZE = 40  # Adjusted for a larger grid
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Full database of the first-generation Pokémon (151) with types and consistent attacks
pokemon_db = {
    'Bulbizarre': {
        'PV': 45, 'DEF': 49, 'type': 'Plante Poison', 'ATK': [
            {'degats': 49, 'attaque': 'Fouet Lianes', 'type': 'Plante'},
            {'degats': 65, 'attaque': 'Griffe', 'type': 'Normal'},
            {'degats': 50, 'attaque': 'Racines', 'type': 'Plante'},
            {'degats': 60, 'attaque': 'Lance-Soleil', 'type': 'Plante'}
        ], 'precision': [100, 100, 100, 100],
        'vitesse': 45, 'esquive': 60, 'portee': [1, 2, 1, 2]
    },
    'Herbizarre': {
        'PV': 60, 'DEF': 63, 'type': 'Plante Poison', 'ATK': [
            {'degats': 62, 'attaque': 'Fouet Lianes', 'type': 'Plante'},
            {'degats': 80, 'attaque': 'Griffe', 'type': 'Normal'},
            {'degats': 70, 'attaque': 'Racines', 'type': 'Plante'},
            {'degats': 90, 'attaque': 'Lance-Soleil', 'type': 'Plante'}
        ], 'precision': [100, 100, 100, 100],
        'vitesse': 60, 'esquive': 65, 'portee': [1, 2, 1, 2]
    },
    'Florizarre': {
        'PV': 80, 'DEF': 83, 'type': 'Plante Poison', 'ATK': [
            {'degats': 82, 'attaque': 'Fouet Lianes', 'type': 'Plante'},
            {'degats': 100, 'attaque': 'Griffe', 'type': 'Normal'},
            {'degats': 70, 'attaque': 'Racines', 'type': 'Plante'},
            {'degats': 120, 'attaque': 'Lance-Soleil', 'type': 'Plante'}
        ], 'precision': [100, 100, 100, 100],
        'vitesse': 80, 'esquive': 70, 'portee': [1, 2, 1, 2]
    },
    'Salamèche': {
        'PV': 39, 'DEF': 43, 'type': 'Feu', 'ATK': [
            {'degats': 52, 'attaque': 'Flamme', 'type': 'Feu'},
            {'degats': 60, 'attaque': 'Griffe', 'type': 'Normal'},
            {'degats': 70, 'attaque': 'Rugissement', 'type': 'Normal'},
            {'degats': 90, 'attaque': 'Lance-Flammes', 'type': 'Feu'}
        ], 'precision': [100, 100, 100, 100],
        'vitesse': 65, 'esquive': 55, 'portee': [1, 2, 1, 2]
    },
    'Reptincel': {
        'PV': 58, 'DEF': 58, 'type': 'Feu', 'ATK': [
            {'degats': 64, 'attaque': 'Flamme', 'type': 'Feu'},
            {'degats': 80, 'attaque': 'Griffe', 'type': 'Normal'},
            {'degats': 70, 'attaque': 'Rugissement', 'type': 'Normal'},
            {'degats': 100, 'attaque': 'Lance-Flammes', 'type': 'Feu'}
        ], 'precision': [100, 100, 100, 100],
        'vitesse': 80, 'esquive': 60, 'portee': [1, 2, 1, 2]
    },
    'Dracaufeu': {
        'PV': 78, 'DEF': 65, 'type': 'Feu Vol', 'ATK': [
            {'degats': 84, 'attaque': 'Flamme', 'type': 'Feu'},
            {'degats': 100, 'attaque': 'Griffe', 'type': 'Normal'},
            {'degats': 70, 'attaque': 'Rugissement', 'type': 'Normal'},
            {'degats': 120, 'attaque': 'Déflagration', 'type': 'Feu'}
        ], 'precision': [100, 100, 100, 100],
        'vitesse': 100, 'esquive': 80, 'portee': [1, 2, 1, 2]
    },
    'Carapuce': {
        'PV': 44, 'DEF': 48, 'type': 'Eau', 'ATK': [
            {'degats': 50, 'attaque': 'Pistolet à O', 'type': 'Eau'},
            {'degats': 60, 'attaque': 'Griffe', 'type': 'Normal'},
            {'degats': 75, 'attaque': 'Écume', 'type': 'Eau'},
            {'degats': 85, 'attaque': 'Hydrocanon', 'type': 'Eau'}
        ], 'precision': [100, 100, 100, 100],
        'vitesse': 43, 'esquive': 60, 'portee': [1, 2, 1, 2]
    },
    'Carabaffe': {
        'PV': 59, 'DEF': 63, 'type': 'Eau', 'ATK': [
            {'degats': 65, 'attaque': 'Pistolet à O', 'type': 'Eau'},
            {'degats': 75, 'attaque': 'Griffe', 'type': 'Normal'},
            {'degats': 85, 'attaque': 'Écume', 'type': 'Eau'},
            {'degats': 100, 'attaque': 'Hydrocanon', 'type': 'Eau'}
        ], 'precision': [100, 100, 100, 100],
        'vitesse': 58, 'esquive': 65, 'portee': [1, 2, 1, 2]
    },
    'Tortank': {
        'PV': 79, 'DEF': 83, 'type': 'Eau', 'ATK': [
            {'degats': 85, 'attaque': 'Pistolet à O', 'type': 'Eau'},
            {'degats': 95, 'attaque': 'Griffe', 'type': 'Normal'},
            {'degats': 110, 'attaque': 'Écume', 'type': 'Eau'},
            {'degats': 125, 'attaque': 'Hydrocanon', 'type': 'Eau'}
        ], 'precision': [100, 100, 100, 100],
        'vitesse': 78, 'esquive': 70, 'portee': [1, 2, 1, 2]
    },
    'Chenipan': {
        'PV': 45, 'DEF': 30, 'type': 'Insecte', 'ATK': [
            {'degats': 30, 'attaque': 'Picpic', 'type': 'Insecte'},
            {'degats': 35, 'attaque': 'Griffe', 'type': 'Normal'},
            {'degats': 40, 'attaque': 'Rugissement', 'type': 'Normal'},
            {'degats': 45, 'attaque': 'Cocooning', 'type': 'Insecte'}
        ], 'precision': [100, 100, 100, 100],
        'vitesse': 35, 'esquive': 50, 'portee': [1, 1, 1, 1]
    },
    'Chrysacier': {
        'PV': 50, 'DEF': 50, 'type': 'Insecte', 'ATK': [
            {'degats': 40, 'attaque': 'Picpic', 'type': 'Insecte'},
            {'degats': 45, 'attaque': 'Griffe', 'type': 'Normal'},
            {'degats': 50, 'attaque': 'Rugissement', 'type': 'Normal'},
            {'degats': 55, 'attaque': 'Cocooning', 'type': 'Insecte'}
        ], 'precision': [100, 100, 100, 100],
        'vitesse': 30, 'esquive': 50, 'portee': [1, 1, 1, 1]
    },
    'Papilusion': {
        'PV': 60, 'DEF': 55, 'type': 'Insecte Vol', 'ATK': [
            {'degats': 50, 'attaque': 'Éboulis', 'type': 'Insecte'},
            {'degats': 65, 'attaque': 'Dard-Venin', 'type': 'Insecte Poison'},
            {'degats': 70, 'attaque': 'Baiser', 'type': 'Normal'},
            {'degats': 75, 'attaque': 'Ultralaser', 'type': 'Normal'}
        ], 'precision': [100, 100, 100, 100],
        'vitesse': 80, 'esquive': 75, 'portee': [1, 2, 1, 2]
    },
    'Aspicot': {
        'PV': 40, 'DEF': 35, 'type': 'Insecte Poison', 'ATK': [
            {'degats': 40, 'attaque': 'Dard-Venin', 'type': 'Insecte Poison'},
            {'degats': 50, 'attaque': 'Morsure', 'type': 'Normal'},
            {'degats': 60, 'attaque': 'Griffe', 'type': 'Normal'},
            {'degats': 70, 'attaque': 'Dard', 'type': 'Insecte'}
        ], 'precision': [100, 100, 100, 100],
        'vitesse': 55, 'esquive': 45, 'portee': [1, 1, 1, 1]
    },
    'Coconfort': {
        'PV': 45, 'DEF': 50, 'type': 'Insecte Poison', 'ATK': [
            {'degats': 40, 'attaque': 'Dard-Venin', 'type': 'Insecte Poison'},
            {'degats': 60, 'attaque': 'Griffe', 'type': 'Normal'},
            {'degats': 50, 'attaque': 'Morsure', 'type': 'Normal'},
            {'degats': 70, 'attaque': 'Cocooning', 'type': 'Insecte Poison'}
        ], 'precision': [100, 100, 100, 100],
        'vitesse': 35, 'esquive': 60, 'portee': [1, 1, 1, 1]
    },
    'Dardargnan': {
        'PV': 65, 'DEF': 90, 'type': 'Insecte Poison', 'ATK': [
            {'degats': 65, 'attaque': 'Dard-Venin', 'type': 'Insecte Poison'},
            {'degats': 75, 'attaque': 'Griffe', 'type': 'Normal'},
            {'degats': 80, 'attaque': 'Morsure', 'type': 'Normal'},
            {'degats': 90, 'attaque': 'Éviscération', 'type': 'Insecte'}
        ], 'precision': [100, 100, 100, 100],
        'vitesse': 100, 'esquive': 60, 'portee': [1, 1, 1, 1]
    },
    'Roucoul': {
        'PV': 40, 'DEF': 30, 'type': 'Normal Vol', 'ATK': [
            {'degats': 50, 'attaque': 'Pico', 'type': 'Normal'},
            {'degats': 55, 'attaque': 'Vol', 'type': 'Vol'},
            {'degats': 60, 'attaque': 'Griffe', 'type': 'Normal'},
            {'degats': 65, 'attaque': 'Rugissement', 'type': 'Normal'}
        ], 'precision': [100, 100, 100, 100],
        'vitesse': 60, 'esquive': 50, 'portee': [1, 2, 1, 2]
    }
}
class Unit:
    """Classe pour représenter une unité."""

    def __init__(self, x, y, PV, ATK, team):
        """Construit une unité avec une position, des PV, une puissance d'attaque et une équipe."""
        self.x = x
        self.y = y
        self.PV = PV
        self.ATK = ATK
        self.team = team  # 'player' ou 'enemy'
        self.is_selected = False

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy

    def attack(self, target, attack_index):
        """Attaque une unité cible."""
        attack = self.ATK[attack_index]
        damage = attack['degats']
        target.PV -= damage
        print(f"{self.team} {self.__class__.__name__} attaque {target.__class__.__name__} avec {attack['attaque']} pour {damage} dégâts.")

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)


class Pokemon(Unit):
    """Classe pour représenter un Pokémon, dérivée de la classe Unit."""

    def __init__(self, name, x, y, PV, DEF, ATK, precision, vitesse, esquive, portee, type_pokemon, icon_path):
        """Construit un Pokémon avec ses attributs spécifiques."""
        super().__init__(x, y, PV, ATK, 'player')  # On utilise l'ATK
        self.name = name
        self.DEF = DEF
        self.precision = precision
        self.vitesse = vitesse
        self.esquive = esquive
        self.portee = portee
        self.type_pokemon = type_pokemon
        
        # Charger l'icône avec gestion des erreurs
        try:
            original_icon = pygame.image.load(icon_path)  # Charger l'icône
            self.icon = pygame.transform.scale(original_icon, (CELL_SIZE, CELL_SIZE))  # Redimensionner à CELL_SIZE x CELL_SIZE
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image {icon_path}: {e}")

    def draw(self, screen):
        """Dessine le Pokémon sur l'écran avec son icône."""
        super().draw(screen)
        screen.blit(self.icon, (self.x * CELL_SIZE, self.y * CELL_SIZE))  # Dessine l'icône


class Game:
    """Classe pour représenter le jeu."""

    def __init__(self, screen):
        """Construit le jeu avec la surface de la fenêtre."""
        self.screen = screen
        self.player_units = self.create_team('player')
        self.enemy_units = self.create_team('enemy')
        self.obstacles = self.generate_obstacles()

    def create_team(self, team):
        """Crée une équipe de Pokémon à partir des positions spécifiées."""
        positions = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)] if team == 'player' else [(13, 13), (13, 14), (14, 13), (14, 14), (15, 13), (15, 14)]
        units = []
        for idx, (x, y) in enumerate(positions):
            name = list(pokemon_db.keys())[idx]
            data = pokemon_db[name]
            icon_path = os.path.join("icons", f"{name.lower()}.png")  # Path to icon
            units.append(Pokemon(name, x, y, data['PV'], data['DEF'], data['ATK'], data['precision'],
                                 data['vitesse'], data['esquive'], data['portee'], data['type'], icon_path))
        return units

    def generate_obstacles(self):
        """Génère des obstacles aléatoires sur la carte."""
        obstacles = []
        for _ in range(random.randint(10, 20)):
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            # Randomly choose between water and lava
            if random.choice([True, False]):
                obstacles.append({'x': x, 'y': y, 'type': 'water'})
            else:
                obstacles.append({'x': x, 'y': y, 'type': 'lava'})
        return obstacles

    def draw(self):
        """Dessine les unités, les obstacles et le plateau sur l'écran."""
        self.screen.fill(WHITE)  # Remplir le fond de jeu en blanc
        for obs in self.obstacles:
            if obs['type'] == 'water':
                self.screen.blit(pygame.image.load("obstacles/eau.png"), (obs['x'] * CELL_SIZE, obs['y'] * CELL_SIZE))
            elif obs['type'] == 'lava':
                self.screen.blit(pygame.image.load("obstacles/lava.png"), (obs['x'] * CELL_SIZE, obs['y'] * CELL_SIZE))

        # Dessiner les bordures
        for x in range(GRID_SIZE + 1):
            self.screen.blit(pygame.image.load("obstacles/grass.png"), (x * CELL_SIZE, 0))  # Haut
            self.screen.blit(pygame.image.load("obstacles/grass.png"), (x * CELL_SIZE, GRID_SIZE * CELL_SIZE - CELL_SIZE))  # Bas
        for y in range(GRID_SIZE + 1):
            self.screen.blit(pygame.image.load("obstacles/grass.png"), (0, y * CELL_SIZE))  # Gauche
            self.screen.blit(pygame.image.load("obstacles/grass.png"), (GRID_SIZE * CELL_SIZE - CELL_SIZE, y * CELL_SIZE))  # Droit

        # Dessiner les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        pygame.display.flip()


def main():
    """Point d'entrée principal du jeu."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jeu de Pokémon")
    clock = pygame.time.Clock()
    game = Game(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.draw()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()