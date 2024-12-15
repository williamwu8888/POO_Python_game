import pygame
from board import GRID_ROWS, GRID_COLS, CELL_SIZE
from skill import *

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

        # Ajuster le nom de l'icône en fonction de l'équipe
        if team == 'player2':  # PVP mode: player2 uses enemy icon
            icon_filename = f"{icon_path}_enemy.png"
        else:  # PVE mode: enemy uses enemy icon, player uses player icon
            icon_filename = f"{icon_path}_{team}.png"

        selected_filename = f"{icon_path}_selected.png"

        # Charger les icônes

        self.icon = pygame.image.load(f'final_version/unit_icons/{icon_filename}')
        self.icon = pygame.transform.scale(self.icon, (CELL_SIZE, CELL_SIZE))
        self.selected_icon = pygame.image.load(f'final_version/unit_icons/{selected_filename}')
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

import pygame
from board import GRID_ROWS, GRID_COLS, CELL_SIZE
from skill import Skill  # Using the existing Skill class

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

        # Adjust icon based on team
        if team == 'player2':  # PVP mode: player2 uses enemy icon
            icon_filename = f"{icon_path}_enemy.png"
        else:  # PVE mode: player uses player icon, enemy uses enemy icon
            icon_filename = f"{icon_path}_{team}.png"

        selected_filename = f"{icon_path}_selected.png"

        # Load icons
        self.icon = pygame.image.load(f'final_version/unit_icons/{icon_filename}')
        self.icon = pygame.transform.scale(self.icon, (CELL_SIZE, CELL_SIZE))
        self.selected_icon = pygame.image.load(f'final_version/unit_icons/{selected_filename}')
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
        """Basic attack."""
        if self.stunned:
            print(f"{self.team} unit is stunned and cannot attack this turn.")
            return  # If the unit is stunned, it cannot attack

        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            skill = self.skills[0] if self.skills else None
            if skill:
                skill.use(self, target, game)

    def receive_damage(self, damage, game):
        """Reduces health and handles defeat."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            game.board.remove_unit(self)
            if self.team == 'player':
                game.player_units.remove(self)
            elif self.team == 'enemy':
                game.enemy_units.remove(self)

    def end_turn(self):
        """Reset status effects at the end of the turn."""
        self.stunned = False  # Reset stun at the end of the turn

    def draw(self, screen):
        """Draw the unit with health bar and icon."""
        # Select icon (normal or selected)
        icon_to_draw = self.selected_icon if self.is_selected else self.icon
        screen.blit(icon_to_draw, (self.x * CELL_SIZE, self.y * CELL_SIZE))

        # Draw health bar
        bar_width = CELL_SIZE - 10
        bar_height = 10
        bar_x = self.x * CELL_SIZE + 5
        bar_y = self.y * CELL_SIZE + CELL_SIZE - 15

        # Display health bar
        hp_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(bar_width * hp_ratio), bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)

        # Health points text
        font = pygame.font.Font(None, 14)
        hp_text = font.render(f"{self.health}/{self.max_health}", True, (0, 0, 0))
        text_x = bar_x + (bar_width - hp_text.get_width()) // 2
        text_y = bar_y + (bar_height - hp_text.get_height()) // 2
        screen.blit(hp_text, (text_x, text_y))


class WarriorUnit(BaseUnit):
    def __init__(self, x, y, team):
        super().__init__(x, y, health=100, attack_power=12, defense=15, team=team, icon_path='guerrier', speed=8)
        self.skills = [
            Skill("Cleave", power=12, range=1, accuracy=1, area_of_effect=1),
            Stun("Taunt", power=0, range=2, accuracy=1)
        ]

    def attack(self, target, game):
        """Override attack method to handle cleave"""
        if self.stunned:
            print(f"{self.team} unit is stunned and cannot attack this turn.")
            return  # If the unit is stunned, it cannot attack

        # Cleave skill logic (can attack multiple units if adjacent)
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            cleave_skill = next((skill for skill in self.skills if skill.name == "Cleave"), None)
            if cleave_skill:
                cleave_skill.use(self, target, game)

class KnightUnit(BaseUnit):
    def __init__(self, x, y, team):
        super().__init__(x, y, health=45, attack_power=8, defense=6, team=team, icon_path='chevalier', speed=10)
        self.skills = [
            Stun("Shield Bash", power=12, range=1, accuracy=0.85),
            Skill("Shield Slam", power=15, range=1, accuracy=1, area_of_effect=1)
        ]
    
    def move(self, dx, dy, board):
        new_x, new_y = self.x + dx, self.y + dy
        if not (0 <= new_x < GRID_COLS and 0 <= new_y < GRID_ROWS):
            return

        if board.is_traversable(new_x, new_y, self.x, self.y):
            distance = abs(dx) + abs(dy)
            if distance <= self.speed:
                board.remove_unit(self)
                self.x, self.y = new_x, new_y
                board.add_unit(self)
                print(f"Knight moved to ({self.x}, {self.y}).")

class ArcherUnit(BaseUnit):
    def __init__(self, x, y, team):
        super().__init__(x, y, health=50, attack_power=18, defense=3, team=team, icon_path='archer', speed=11)
        self.skills = [
            Skill("Precise Shot", power=12, range=4, accuracy=1, area_of_effect=1),
            Skill("Strong Shot", power=18, range=4, accuracy=0.75, area_of_effect=1)
        ]

class MageUnit(BaseUnit):
    def __init__(self, x, y, team):
        super().__init__(x, y, health=36, attack_power=16, defense=2, team=team, icon_path='mage', speed=10)
        self.skills = [Skill("Fireball", 20, 3, 0.9, 1),  # Fireball with higher power
                       BuffSkill("Magic Shield", "defense", buff_amount=5, range=3),  # Magic Shield (buffs defense)
                       BuffSkill("Speed Boost", "speed", buff_amount=1, range=3)]  # Speed Boost added

class HealerUnit(BaseUnit):
    def __init__(self, x, y, team):
        super().__init__(x, y, health=42, attack_power=6, defense=6, team=team, icon_path='soigneur', speed=10)
        self.skills = [HealSkill("Heal", healing_amount=15, range=4, accuracy=1),
                       HealAllSkill("Heal All", healing_amount=10, range=4, accuracy=0.8)]  # HealAllSkill added

class SupportUnit(BaseUnit):
    def __init__(self, x, y, team):
        super().__init__(x, y, health=38, attack_power=6, defense=6, team=team, icon_path='support', speed=10)
        self.skills = [BuffSkill("Power Boost", "attack_power", buff_amount=5, range=3),
                       DebuffSkill("Power Decrease", "attack_power", debuff_amount=-5, range=3),  # Debuff skill added
                       DebuffSkill("Armor Break", "defense", debuff_amount=-3, range=3)]  # ArmorBreakSkill added
