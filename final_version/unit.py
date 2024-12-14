import pygame
from board import GRID_ROWS, GRID_COLS, CELL_SIZE
from skill import Skill, HealSkill, BuffSkill, PlaceRiverSkill

import os
print("Répertoire courant :", os.getcwd())


class BaseUnit:
    def __init__(self, x, y, health, attack_power, defense, team, icon_path, skills=[], is_selected=False, speed=1):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.defense = defense
        self.team = team
        self.skills = skills
        self.is_selected = is_selected
        self.speed = speed
        self.stunned = False

        # Charger les icônes normales et "sélectionnées"
        icon_filename = f"{icon_path}_{team}.png"
        selected_filename = f"{icon_path}_selected.png"
        self.icon = pygame.image.load(f'unit_icons/{icon_filename}')
        self.icon = pygame.transform.scale(self.icon, (CELL_SIZE, CELL_SIZE))
        self.selected_icon = pygame.image.load(f'unit_icons/{selected_filename}')
        self.selected_icon = pygame.transform.scale(self.selected_icon, (CELL_SIZE, CELL_SIZE))

    def move(self, dx, dy, board):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < GRID_COLS and 0 <= new_y < GRID_ROWS:
            target_cell = board.cells[new_y][new_x]
            print(f"Essai de déplacement vers ({new_x}, {new_y}) - Traversable: {target_cell.traversable}, Type: {target_cell.type}")
            if target_cell.traversable:
                distance = abs(dx) + abs(dy)
                if distance <= self.speed:
                    board.remove_unit(self)
                    self.x = new_x
                    self.y = new_y
                    board.add_unit(self)
                    print(f"{self.team} unit moved to ({self.x}, {self.y}).")
            else:
                print(f"Unit cannot move to ({new_x}, {new_y}) - not traversable.")

    def attack(self, target, game):
        """Attaque basique."""
        if self.stunned:
            print(f"{self.team} unit is stunned and cannot attack this turn.")
            return  # Si l'unité est stun, elle ne peut pas attaquer

        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            skill = self.skills[0] if self.skills else None
            if skill:
                skill.use(self, target, game)

    def receive_damage(self, damage, game):
        """Réduction de vie et gestion de la défaite."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            game.board.remove_unit(self)
            if self.team == 'player':
                game.player_units.remove(self)
            elif self.team == 'enemy':
                game.enemy_units.remove(self)

    def end_turn(self):
        """Réinitialise les effets de statut à la fin du tour."""
        self.stunned = False  # Réinitialise le stun à la fin du tour

    def draw(self, screen):
        """Dessine l'unité avec la barre de vie et l'icône adaptée."""
        # Choisir l'icône normale ou "sélectionnée"
        icon_to_draw = self.selected_icon if self.is_selected else self.icon
        screen.blit(icon_to_draw, (self.x * CELL_SIZE, self.y * CELL_SIZE))

        # Dessiner la barre de vie
        bar_width = CELL_SIZE - 10
        bar_height = 10
        bar_x = self.x * CELL_SIZE + 5
        bar_y = self.y * CELL_SIZE + CELL_SIZE - 15

        # Affichage de la barre de vie
        hp_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(bar_width * hp_ratio), bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)

        # Texte des points de vie
        font = pygame.font.Font(None, 14)
        hp_text = font.render(f"{self.health}/{self.max_health}", True, (0, 0, 0))
        text_x = bar_x + (bar_width - hp_text.get_width()) // 2
        text_y = bar_y + (bar_height - hp_text.get_height()) // 2
        screen.blit(hp_text, (text_x, text_y))

class WarriorUnit(BaseUnit):
    def __init__(self, x, y, team):
        super().__init__(x, y, health=60, attack_power=6, defense=10, team=team, icon_path='guerrier', speed=2)

class KnightUnit(BaseUnit):
    def __init__(self, x, y, team):
        super().__init__(x, y, health=45, attack_power=8, defense=6, team=team, icon_path='chevalier', speed=4)
        self.skills = [Skill("Shield Bash", 12, 1, 0.85, 1)]  # Attaque à courte portée avec effet de stun (dépend de la compétence)
    
    def move(self, dx, dy, board):
        """
        Déplace l'unité selon les coordonnées fournies (dx, dy) si la case cible est traversable.
        """
        if self.stunned:
            return  # L'unité est étourdie et ne peut pas se déplacer

        # Calcul des nouvelles coordonnées
        new_x, new_y = self.x + dx, self.y + dy

        # Vérification des limites de la grille
        if not (0 <= new_x < GRID_COLS and 0 <= new_y < GRID_ROWS):
            return  # Les coordonnées sont hors de la grille

        # Récupération de la cellule cible
        target_cell = board.cells[new_y][new_x]
        distance = abs(dx) + abs(dy)

        # Vérification des conditions de déplacement
        if (target_cell.type == "river" or target_cell.traversable) and distance <= self.speed:
            board.remove_unit(self)
            self.x, self.y = new_x, new_y
            board.add_unit(self)


class ArcherUnit(BaseUnit):
    def __init__(self, x, y, team):
        super().__init__(x, y, health=40, attack_power=16, defense=2, team=team, icon_path='archer', speed=3)
        self.skills = [Skill("Arrow Shot", 10, 3, 0.9, 1)]

class MageUnit(BaseUnit):
    def __init__(self, x, y, team):
        super().__init__(x, y, health=36, attack_power=16, defense=2, team=team, icon_path='mage', speed=3)
        self.skills = [Skill("Fireball", 15, 2, 0.8, 1)]

class HealerUnit(BaseUnit):
    def __init__(self, x, y, team):
        super().__init__(x, y, health=42, attack_power=6, defense=6, team=team, icon_path='soigneur', speed=3)
        self.skills = [HealSkill("Heal", 15, 1, 0.95)]

class SupportUnit(BaseUnit):
    def __init__(self, x, y, team):
        icon = pygame.image.load('unit_icons/support.png')
        icon = pygame.transform.scale(icon, (CELL_SIZE, CELL_SIZE))
        super().__init__(x, y, health=38, attack_power=6, defense=6, team=team, icon=icon, speed=3)
        self.skills = [
            BuffSkill("Power Boost", "attack_power", 3, 3),
            PlaceRiverSkill("Place River", range=1, accuracy=1)  # Ajoute la compétence pour placer une rivière
        ]

    def move(self, dx, dy, board):
        if self.stunned:  # Vérifie si l'unité est étourdie
            print(f"{self.team} unit is stunned and cannot move this turn.")
            return

        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < GRID_COLS and 0 <= new_y < GRID_ROWS:  # Vérifie que la position est valide
            target_cell = board.cells[new_y][new_x]
            if target_cell.type != "wall" and target_cell.unit is None:  # Vérifie que la case est libre
                distance = abs(dx) + abs(dy)
                if distance <= self.speed:  # Vérifie que le mouvement est dans la portée de vitesse
                    board.remove_unit(self)  # Retire l'unité de l'ancienne position
                    self.x = new_x
                    self.y = new_y
                    board.add_unit(self)  # Ajoute l'unité à la nouvelle position

                    # Après chaque déplacement, permet de placer une rivière
                    print("Sélectionnez une case adjacente pour placer une rivière (ou appuyez sur Échap pour annuler) :")
                    adjacent_cells = [(self.x + dx, self.y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
                    valid_cells = [cell for cell in adjacent_cells if 0 <= cell[0] < GRID_COLS and 0 <= cell[1] < GRID_ROWS \
                                   and board.cells[cell[1]][cell[0]].unit is None and board.cells[cell[1]][cell[0]].type != "wall"]
                    if valid_cells:
                        # Dessine les options de placement
                        for cell in valid_cells:
                            pygame.draw.rect(
                                board.screen,
                                (0, 255, 255),
                                (cell[0] * CELL_SIZE, cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                                2
                            )
                        pygame.display.flip()

                        placing = True
                        while placing:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    mouse_x, mouse_y = pygame.mouse.get_pos()
                                    target_x = mouse_x // CELL_SIZE
                                    target_y = mouse_y // CELL_SIZE
                                    if (target_x, target_y) in valid_cells:
                                        board.cells[target_y][target_x].type = "river"
                                        board.cells[target_y][target_x].traversable = False
                                        print(f"Rivière placée à ({target_x}, {target_y}).")
                                        placing = False
                                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                    placing = False


