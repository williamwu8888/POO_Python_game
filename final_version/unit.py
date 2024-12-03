import pygame

class Unit:
    def __init__(self, x, y, health, attack_power, defense, team, skills=[], is_selected=False, speed=1):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health  # HP maximum de l'unité
        self.attack_power = attack_power
        self.defense = defense
        self.team = team  # 'player' ou 'enemy'
        self.skills = skills
        self.is_selected = is_selected
        self.speed = speed  # Vitesse de déplacement (cases par tour)

    def move(self, dx, dy, board):
        """Move unit on the board."""
        new_x = self.x + dx
        new_y = self.y + dy

        # Vérifie que le déplacement respecte la vitesse et que la case cible est vide
        if 0 <= new_x < 8 and 0 <= new_y < 8 and board.cells[new_y][new_x].unit is None:
            distance = abs(dx) + abs(dy)
            if distance <= self.speed:  # Vérifie que le déplacement est dans la limite de la vitesse
                board.remove_unit(self)  # Supprime l'unité de sa position actuelle
                self.x = new_x
                self.y = new_y
                board.add_unit(self)  # Ajoute l'unité à la nouvelle position

    def attack(self, target, game):
        """Attack another unit."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            skill = self.skills[0] if self.skills else None  # Use the first skill available
            if skill:
                skill.use(self, target, game)  # Passe 'game' pour gérer les unités vaincues


    def receive_damage(self, damage, game):
        """Reduce unit's health based on received damage and handle defeat."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print(f"{self.team} unit has been defeated!")

            # Retirer l'unité du plateau et de la liste de l'équipe
            game.board.remove_unit(self)
            if self.team == 'player':
                game.player_units.remove(self)
            elif self.team == 'enemy':
                game.enemy_units.remove(self)

    def draw(self, screen):
        """Dessine l'unité sur l'écran, avec une barre de vie."""
        # Définir la couleur en fonction de l'équipe (bleu pour le joueur, rouge pour l'ennemi)
        color = (0, 0, 255) if self.team == 'player' else (255, 0, 0)

        # Dessiner le cercle représentant l'unité
        pygame.draw.circle(screen, color, (self.x * 60 + 30, self.y * 60 + 30), 20)

        # Dessiner la barre de vie
        max_bar_width = 50  # Largeur maximale de la barre
        bar_height = 5      # Hauteur de la barre
        bar_x = self.x * 60 + 5  # Position x de la barre
        bar_y = self.y * 60 + 50  # Position y de la barre (au-dessous de l'unité)

        # Calculer la largeur proportionnelle aux HP restants
        hp_ratio = self.health / self.max_health
        bar_width = int(max_bar_width * hp_ratio)

        # Dessiner le contour de la barre
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, max_bar_width, bar_height), 1)

        # Dessiner la partie remplie (points de vie restants)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width, bar_height))
