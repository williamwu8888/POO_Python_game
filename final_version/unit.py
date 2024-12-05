import pygame
from board import GRID_ROWS, GRID_COLS, CELL_SIZE
from skill import Skill

class BaseUnit:
    def __init__(self, x, y, health, attack_power, defense, team, skills=[], is_selected=False, speed=1):
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

    def move(self, dx, dy, board):
        """Déplacement avec vérifications."""
        new_x = self.x + dx
        new_y = self.y + dy
        if (0 <= new_x < GRID_COLS and 0 <= new_y < GRID_ROWS and
            board.cells[new_y][new_x].unit is None and
            board.cells[new_y][new_x].type != "obstacle"):
            distance = abs(dx) + abs(dy)
            if distance <= self.speed:
                board.remove_unit(self)
                self.x = new_x
                self.y = new_y
                board.add_unit(self)

    def attack(self, target, game):
        """Attaque basique."""
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

    def draw(self, screen):
        """Dessine l'unité avec la barre de vie."""
        color = (0, 0, 255) if self.team == 'player' else (255, 0, 0)

        # Dessiner le cercle représentant l'unité
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), 15)

        # Dessiner la barre de vie
        bar_width = CELL_SIZE - 10
        bar_height = 10
        bar_x = self.x * CELL_SIZE + 5
        bar_y = self.y * CELL_SIZE + CELL_SIZE - 15

        # Affichage de la barre et des HP
        hp_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(bar_width * hp_ratio), bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)
        font = pygame.font.Font(None, 14)
        hp_text = font.render(f"{self.health}/{self.max_health}", True, (0, 0, 0))
        text_x = bar_x + (bar_width - hp_text.get_width()) // 2
        text_y = bar_y + (bar_height - hp_text.get_height()) // 2
        screen.blit(hp_text, (text_x, text_y))

class WarriorUnit(BaseUnit):
    def __init__(self, x, y, team):
        super().__init__(x, y, health=40, attack_power=7, defense=5, team=team, speed=2)

class ArcherUnit(BaseUnit):
    def __init__(self, x, y, team):
        super().__init__(x, y, health=25, attack_power=5, defense=2, team=team, speed=3)
        self.skills = [Skill("Arrow Shot", 10, 3, 0.9, 1)]

class MageUnit(BaseUnit):
    def __init__(self, x, y, team):
        super().__init__(x, y, health=20, attack_power=8, defense=1, team=team, speed=2)
        self.skills = [Skill("Fireball", 15, 2, 0.8, 1)]