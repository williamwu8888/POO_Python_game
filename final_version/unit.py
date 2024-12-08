import pygame
from board import GRID_ROWS, GRID_COLS, CELL_SIZE
from skill import Skill, HealSkill, BuffSkill

import os
print("Répertoire courant :", os.getcwd())


class BaseUnit:
    def __init__(self, x, y, health, attack_power, defense, team, icon, skills=[], is_selected=False, speed=1):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.attack_power = attack_power
        self.defense = defense
        self.team = team
        self.skills = skills
        self.is_selected = is_selected
        self.icon = icon
        self.speed = speed
        self.stunned = False

    def move(self, dx, dy, board):
        """Déplacement avec vérifications."""

        if self.stunned:
            print(f"{self.team} unit is stunned and cannot move this turn.")
            return  # Si l'unité est stun, elle ne peut pas se déplacer
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
        """Dessine l'unité avec la barre de vie."""
        color = (0, 0, 255) if self.team == 'player' else (255, 0, 0)

        # Dessiner le cercle représentant l'unité
        screen.blit(self.icon, (self.x * CELL_SIZE, self.y * CELL_SIZE))

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
        icon = pygame.image.load('unit_icons/guerrier.png')
        icon = pygame.transform.scale(icon, (CELL_SIZE, CELL_SIZE))
        super().__init__(x, y, health=40, attack_power=7, defense=5, team=team, icon=icon, speed=2)

class KnightUnit(BaseUnit):
    def __init__(self, x, y, team):
        icon = pygame.image.load('unit_icons/chevalier.png')
        icon = pygame.transform.scale(icon, (CELL_SIZE, CELL_SIZE))
        super().__init__(x, y, health=50, attack_power=10, defense=8, team=team, icon=icon, speed=10)
        self.skills = [Skill("Shield Bash", 12, 1, 0.85, 1)]  # Attaque à courte portée avec effet de stun (dépend de la compétence)

class ArcherUnit(BaseUnit):
    def __init__(self, x, y, team):
        icon = pygame.image.load('unit_icons/archer.png')
        icon = pygame.transform.scale(icon, (CELL_SIZE, CELL_SIZE))
        super().__init__(x, y, health=25, attack_power=5, defense=2, team=team, icon=icon, speed=3)
        self.skills = [Skill("Arrow Shot", 10, 3, 0.9, 1)]

class MageUnit(BaseUnit):
    def __init__(self, x, y, team):
        icon = pygame.image.load('unit_icons/mage.png')
        icon = pygame.transform.scale(icon, (CELL_SIZE, CELL_SIZE))
        super().__init__(x, y, health=20, attack_power=8, defense=1, team=team, icon=icon, speed=2)
        self.skills = [Skill("Fireball", 15, 2, 0.8, 1)]

class HealerUnit(BaseUnit):
    def __init__(self, x, y, team):
        icon = pygame.image.load('unit_icons/soigneur.png')
        icon = pygame.transform.scale(icon, (CELL_SIZE, CELL_SIZE))
        super().__init__(x, y, health=30, attack_power=4, defense=3, team=team, icon=icon, speed=2)
        self.skills = [HealSkill("Heal", 15, 1, 0.95)]

class SupportUnit(BaseUnit):
    def __init__(self, x, y, team):
        icon = pygame.image.load('unit_icons/support.png')
        icon = pygame.transform.scale(icon, (CELL_SIZE, CELL_SIZE))
        super().__init__(x, y, health=25, attack_power=6, defense=4, team=team, icon=icon, speed=2)
        self.skills = [BuffSkill("Power Boost", "attack_power", 3, 3)]
