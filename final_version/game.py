import random
import pygame
from board import Board
from unit import *
from skill import *
from board import GRID_ROWS, GRID_COLS, CELL_SIZE
from wall import generate_walls, draw_walls
from river import generate_rivers, draw_rivers
from bush import generate_bushes, draw_bushes

clock = pygame.time.Clock()

class Game:
    def __init__(self, screen, mode='PVE'):
        self.screen = screen
        self.mode = mode

        self.board = Board(GRID_ROWS, GRID_COLS)

        self.player_units = [
            WarriorUnit(0, (GRID_ROWS-6)//2, 'player'),
            KnightUnit(0, (GRID_ROWS-6)//2 + 1, 'player'),
            ArcherUnit(0, (GRID_ROWS-6)//2 +2, 'player'),
            MageUnit(0, (GRID_ROWS-6)//2 +3, 'player'),
            HealerUnit(0, (GRID_ROWS-6)//2 +4, 'player'),
            SupportUnit(0, (GRID_ROWS-6)//2 +5, 'player')
        ]

        self.enemy_units = [
            WarriorUnit(GRID_COLS - 1, (GRID_ROWS-6)//2, 'enemy' if mode == 'PVE' else 'player2'),
            KnightUnit(GRID_COLS - 1, (GRID_ROWS-6)//2 +1, 'enemy' if mode == 'PVE' else 'player2'),
            ArcherUnit(GRID_COLS - 1, (GRID_ROWS-6)//2 +2, 'enemy' if mode == 'PVE' else 'player2'),
            MageUnit(GRID_COLS - 1, (GRID_ROWS-6)//2 +3, 'enemy' if mode == 'PVE' else 'player2'),
            HealerUnit(GRID_COLS - 1, (GRID_ROWS-6)//2 +4, 'enemy' if mode == 'PVE' else 'player2'),
            SupportUnit(GRID_COLS - 1, (GRID_ROWS-6)//2 +5, 'enemy' if mode == 'PVE' else 'player2')
        ]



        self.walls = generate_walls(
            self.board,
            [(unit.x, unit.y) for unit in self.player_units],
            [(unit.x, unit.y) for unit in self.enemy_units])

        self.rivers = generate_rivers(
            self.board,
            [(unit.x, unit.y) for unit in self.player_units],
            [(unit.x, unit.y) for unit in self.enemy_units]
        )


        self.rivers = generate_rivers(
            self.board,
            [(unit.x, unit.y) for unit in self.player_units],
            [(unit.x, unit.y) for unit in self.enemy_units]
        )

        self.bushes = generate_bushes(
            self.board,
            [(unit.x, unit.y) for unit in self.player_units],
            [(unit.x, unit.y) for unit in self.enemy_units],
            [(wall.x, wall.y) for wall in self.walls],
            [(river.x, river.y) for river in self.rivers]
        )

        # Ajouter les unités au plateau
        for unit in self.player_units + self.enemy_units:
            self.board.add_unit(unit)

        self.current_team = 'player'

    def flip_display(self):
        self.screen.fill((0, 0, 0))
        self.board.display(self.screen)
        draw_rivers(self.screen, self.board, CELL_SIZE)
        draw_walls(self.screen, self.board, CELL_SIZE)
        draw_bushes(self.screen, self.board, CELL_SIZE)
        pygame.display.flip()

    def handle_turn(self):
        if self.mode == 'PVE':
            self.handle_player_turn()
            self.handle_enemy_turn()
        elif self.mode == 'PVP':
            if self.current_team == 'player':
                self.handle_player_turn()
                self.current_team = 'player2'
            elif self.current_team == 'player2':
                self.handle_team_turn(self.enemy_units)
                self.current_team = 'player'

    def handle_player_turn(self):
        self.handle_team_turn(self.player_units)

    def handle_team_turn(self, team_units):
        for selected_unit in team_units:
            if selected_unit.stunned:
                selected_unit.end_turn()  # Fin du tour, réinitialiser le stun
                continue

            has_acted = False
            moves_left = selected_unit.speed
            selected_unit.is_selected = True
            current_x, current_y = selected_unit.x, selected_unit.y  # Position temporaire
            self.flip_display()

            while not has_acted:
                for event in pygame.event.get():
                    self.display_movement_radius(selected_unit, moves_left)
                    pygame.draw.rect(
                        self.screen,
                        (0, 255, 0),  # Vert pour la position temporaire
                        (current_x * CELL_SIZE, current_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                        2
                    )
                    pygame.display.flip()

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1

                        # Calculer la nouvelle position temporaire
                        new_x = current_x + dx
                        new_y = current_y + dy
                        distance = abs(new_x - selected_unit.x) + abs(new_y - selected_unit.y)

                        if self.board.is_traversable(new_x, new_y,current_x, current_y, selected_unit) and distance <= moves_left:
                            print(f"Moving to ({new_x}, {new_y})")
                            current_x, current_y = new_x, new_y
                            self.flip_display()
                            self.display_movement_radius(selected_unit, moves_left)
                            pygame.draw.rect(
                                self.screen,
                                (0, 255, 0),
                                (current_x * CELL_SIZE, current_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                                2
                            )
                            pygame.display.flip()
                        else: 
                            print(f"Cannot move to ({new_x}, {new_y}): traversable={self.board.is_traversable(new_x, new_y,current_x, current_y, selected_unit)}")
                            print(f"Cannot move to ({new_x}, {new_y}): traversable={self.board.is_traversable(new_x, new_y,current_x, current_y, selected_unit)}")
                            new_x,new_y = current_x,current_y # Retourner la position cible à la position actuelle pour éviter de pas pouvoir se bouger

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        if self.board.is_another_unit(current_x, current_y,selected_unit):
                            self.board.remove_unit(selected_unit)
                            selected_unit.x, selected_unit.y = current_x, current_y
                            self.board.add_unit(selected_unit)
                            self.flip_display()

                            available_skills = self.get_available_skills(selected_unit)
                            if available_skills:
                                chosen_skill = self.display_skill_menu(selected_unit, available_skills)

                                if isinstance(chosen_skill, HealSkill):  # Check for HealSkill class
                                    # Get all possible heal targets (teammates within range)
                                    heal_targets = self.get_heal_targets(selected_unit)
                                    healable_targets = [target for target in heal_targets
                                                        if self.board.cells[target[1]][target[0]].unit.health < self.board.cells[target[1]][target[0]].unit.max_health]
                                    if healable_targets:
                                        self.display_attack_radius(selected_unit, chosen_skill.range)

                                        # Wait for player to select a target
                                        target_chosen = False
                                        current_target_idx = 0  # Cursor index for the selected target

                                        valid_targets = healable_targets  # Filter for healable targets

                                        while not target_chosen:
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:
                                                    pygame.quit()
                                                    exit()

                                                if event.type == pygame.KEYDOWN:
                                                    if event.key == pygame.K_DOWN:
                                                        current_target_idx = (current_target_idx + 1) % len(valid_targets)
                                                    elif event.key == pygame.K_UP:
                                                        current_target_idx = (current_target_idx - 1) % len(valid_targets)

                                                    if event.key == pygame.K_SPACE:
                                                        target_x, target_y = valid_targets[current_target_idx]
                                                        target_unit = self.board.cells[target_y][target_x].unit
                                                        if target_unit:
                                                            print(f"Healing {target_unit.team} unit.")
                                                            chosen_skill.use(selected_unit, target_unit, self)
                                                            target_chosen = True
                                                            self.flip_display()

                                            self.display_attack_radius(selected_unit, chosen_skill.range)
                                            pygame.draw.rect(
                                                self.screen,
                                                (0, 0, 255),  # Blue to indicate the selected target
                                                (valid_targets[current_target_idx][0] * CELL_SIZE,
                                                 valid_targets[current_target_idx][1] * CELL_SIZE,
                                                 CELL_SIZE, CELL_SIZE),
                                                3  # Outline thickness for the cursor
                                            )
                                            pygame.display.flip()
                                            clock.tick(30)

                                elif isinstance(chosen_skill, BuffSkill):  # Check for BuffSkill
                                    # Get teammates within the buff's range
                                    buffable_targets = self.get_buffable_targets(selected_unit, chosen_skill)
                                    
                                    if buffable_targets:
                                        # Clear the previously selected unit's highlight by redrawing it in its normal state
                                        self.display_buff_radius(selected_unit, chosen_skill.range)

                                        # Wait for player to select a target
                                        target_chosen = False
                                        current_target_idx = 0  # Target selection cursor

                                        # Filter the valid targets (teammates in range)
                                        valid_targets = [target for target in buffable_targets
                                                        if abs(target[0] - selected_unit.x) + abs(target[1] - selected_unit.y) <= chosen_skill.range]

                                        # Show the valid buffable targets within range
                                        while not target_chosen:
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:
                                                    pygame.quit()
                                                    exit()

                                                if event.type == pygame.KEYDOWN:
                                                    if event.key == pygame.K_DOWN:
                                                        current_target_idx = (current_target_idx + 1) % len(valid_targets)  # Move to next target
                                                    elif event.key == pygame.K_UP:
                                                        current_target_idx = (current_target_idx - 1) % len(valid_targets)  # Move to previous target

                                                    # Select a target with K_SPACE
                                                    if event.key == pygame.K_SPACE:
                                                        target_x, target_y = valid_targets[current_target_idx]
                                                        target_unit = self.board.cells[target_y][target_x].unit
                                                        if target_unit:
                                                            print(f"Buffing {target_unit.team} unit.")
                                                            chosen_skill.use(selected_unit, target_unit, self)
                                                            target_chosen = True

                                            # Redraw the buff range with the selected target
                                            self.display_buff_radius(selected_unit, chosen_skill.range)

                                            # Redraw the selected target with a blue outline
                                            pygame.draw.rect(
                                                self.screen,
                                                (0, 0, 255),  # Blue to indicate the selected target
                                                (valid_targets[current_target_idx][0] * CELL_SIZE,
                                                valid_targets[current_target_idx][1] * CELL_SIZE,
                                                CELL_SIZE, CELL_SIZE),
                                                3  # Outline thickness for the cursor
                                            )

                                            # Refresh the display once at the end of the loop iteration
                                            pygame.display.flip()
                                            clock.tick(30)

                                    else:
                                        print("No valid teammates to buff.")

                                elif isinstance(chosen_skill, DebuffSkill):  # Check for DebuffSkill class
                                    # Get enemies within the debuff's range
                                    debuffable_targets = self.get_attackable_targets(selected_unit, chosen_skill)
                                    
                                    if debuffable_targets:
                                        # Display the debuff range
                                        self.display_attack_radius(selected_unit, chosen_skill.range)

                                        # Wait for player to select a target
                                        target_chosen = False
                                        current_target_idx = 0  # Target selection cursor

                                        # Filter the valid targets (enemies in range)
                                        valid_targets = [target for target in debuffable_targets
                                                        if abs(target[0] - selected_unit.x) + abs(target[1] - selected_unit.y) <= chosen_skill.range]

                                        # Show the valid debuffable targets within range
                                        while not target_chosen:
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:
                                                    pygame.quit()
                                                    exit()

                                                if event.type == pygame.KEYDOWN:
                                                    if event.key == pygame.K_DOWN:
                                                        current_target_idx = (current_target_idx + 1) % len(valid_targets)  # Move to next target
                                                    elif event.key == pygame.K_UP:
                                                        current_target_idx = (current_target_idx - 1) % len(valid_targets)  # Move to previous target

                                                    # Select a target with K_SPACE
                                                    if event.key == pygame.K_SPACE:
                                                        target_x, target_y = valid_targets[current_target_idx]
                                                        target_unit = self.board.cells[target_y][target_x].unit
                                                        if target_unit:
                                                            print(f"{selected_unit.team.capitalize()} unit ({selected_unit.__class__.__name__}) debuffs "
                                                                f"{target_unit.team.capitalize()} unit ({target_unit.__class__.__name__})'s "
                                                                f"{chosen_skill.stat_to_debuff} by {chosen_skill.debuff_amount}.")
                                                            chosen_skill.use(selected_unit, target_unit, self)
                                                            target_chosen = True
                                                            self.flip_display()

                                            # Redraw the debuff range with the selected target
                                            self.display_attack_radius(selected_unit, chosen_skill.range)
                                            pygame.draw.rect(
                                                self.screen,
                                                (255, 0, 0),  # Red to indicate the selected target
                                                (valid_targets[current_target_idx][0] * CELL_SIZE,
                                                valid_targets[current_target_idx][1] * CELL_SIZE,
                                                CELL_SIZE, CELL_SIZE),
                                                3  # Outline thickness for the cursor
                                            )
                                            pygame.display.flip()
                                            clock.tick(30)
                                            
                                    else:
                                        print("No valid enemies to debuff.")

                                elif (isinstance(chosen_skill, FireballSkill)): # Si le skill c'est fireball il augmente l'aire d'attaque
                                    # Filtrer les ennemis dans la portée
                                    attackable_targets = self.get_attackable_targets(selected_unit, chosen_skill)

                                    if attackable_targets :
                                        # Affiche la portée d'attaque
                                        self.display_attack_radius(selected_unit, chosen_skill.range)

                                        # Attente du joueur pour choisir la cible (au clavier)
                                        target_chosen = False
                                        current_target_idx = 0  # Index du curseur de la cible sélectionnée

                                        # Filtrer les ennemis à portée
                                        valid_targets = [target for target in attackable_targets
                                                        if abs(target[0] - selected_unit.x) + abs(target[1] - selected_unit.y) <= chosen_skill.range]

                                        # Afficher les allies à portée
                                        while not target_chosen:
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:
                                                    pygame.quit()
                                                    exit()

                                                if event.type == pygame.KEYDOWN:
                                                    # Déplacer le curseur sur les cibles à portée
                                                    if event.key == pygame.K_DOWN:
                                                        current_target_idx = (current_target_idx + 1) % len(valid_targets)
                                                    elif event.key == pygame.K_UP:
                                                        current_target_idx = (current_target_idx - 1) % len(valid_targets)

                                                    # Sélectionner une cible avec K_SPACE
                                                    if event.key == pygame.K_SPACE:
                                                        
                                                        target_x, target_y = valid_targets[current_target_idx]                                                        
                                                        target_unit = self.board.cells[target_y][target_x].unit
                                                        if target_unit:
                                                            print(f"Using {chosen_skill.name} on {target_unit.team} unit.")
                                                            chosen_skill.use(selected_unit, target_unit, self)
                                                            target_chosen = True
                                                            self.flip_display()

                                                        if ((target_x+1 >= 0) and ((target_x+1) < GRID_COLS) and (target_y >= 0) and (target_y < GRID_ROWS)):
                                                            #print(target_x+1)
                                                            target1 = self.board.cells[target_y][target_x+1].unit
                                                            if target1:
                                                                print(f"Using {chosen_skill.name} on {target_unit.team} unit.")
                                                                chosen_skill.use(selected_unit, target1, self)
                                                                self.flip_display()

                                                        if (target_x+1 >= 0 and target_x+1 < GRID_COLS and target_y+1 >= 0 and target_y+1 < GRID_ROWS):
                                                            target2 = self.board.cells[target_y+1][target_x+1].unit
                                                            if target2:
                                                                print(f"Using {chosen_skill.name} on {target_unit.team} unit.")
                                                                chosen_skill.use(selected_unit, target2, self)
                                                                self.flip_display()

                                                        if (target_x >= 0 and target_x < GRID_COLS and target_y+1 >= 0 and target_y+1 < GRID_ROWS):
                                                            target3 = self.board.cells[target_y+1][target_x].unit
                                                            if target3:
                                                                print(f"Using {chosen_skill.name} on {target_unit.team} unit.")
                                                                chosen_skill.use(selected_unit, target3, self)
                                                                self.flip_display()
                                                        

                                            # Redessiner la portée avec la cible sélectionnée
                                            self.display_attack_radius(selected_unit, chosen_skill.range)
                                            pygame.draw.rect(
                                                self.screen,
                                                (0, 0, 255),  # Bleu pour indiquer la cible sélectionnée
                                                (valid_targets[current_target_idx][0] * CELL_SIZE,
                                                valid_targets[current_target_idx][1] * CELL_SIZE,
                                                CELL_SIZE*2, CELL_SIZE*2),
                                                3  # Épaisseur du contour pour le curseur
                                            )
                                            pygame.display.flip()

                                elif not isinstance(chosen_skill, (HealSkill, BuffSkill, DebuffSkill)):  # Handle non-heal/buff/debuff skills
                                    # Filtrer les ennemis dans la portée
                                    attackable_targets = self.get_attackable_targets(selected_unit, chosen_skill)

                                    if attackable_targets :
                                        # Affiche la portée d'attaque
                                        self.display_attack_radius(selected_unit, chosen_skill.range)

                                        # Attente du joueur pour choisir la cible (au clavier)
                                        target_chosen = False
                                        current_target_idx = 0  # Index du curseur de la cible sélectionnée

                                        # Filtrer les ennemis à portée
                                        valid_targets = [target for target in attackable_targets
                                                        if abs(target[0] - selected_unit.x) + abs(target[1] - selected_unit.y) <= chosen_skill.range]

                                        # Afficher les ennemis à portée
                                        while not target_chosen:
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:
                                                    pygame.quit()
                                                    exit()

                                                if event.type == pygame.KEYDOWN:
                                                    # Déplacer le curseur sur les cibles à portée
                                                    if event.key == pygame.K_DOWN:
                                                        current_target_idx = (current_target_idx + 1) % len(valid_targets)
                                                    elif event.key == pygame.K_UP:
                                                        current_target_idx = (current_target_idx - 1) % len(valid_targets)

                                                    # Sélectionner une cible avec K_SPACE
                                                    if event.key == pygame.K_SPACE:
                                                        target_x, target_y = valid_targets[current_target_idx]
                                                        target_unit = self.board.cells[target_y][target_x].unit
                                                        if target_unit:
                                                            print(f"Using {chosen_skill.name} on {target_unit.team} unit.")
                                                            chosen_skill.use(selected_unit, target_unit, self)
                                                            target_chosen = True
                                                            self.flip_display()

                                            # Redessiner la portée avec la cible sélectionnée
                                            self.display_attack_radius(selected_unit, chosen_skill.range)
                                            pygame.draw.rect(
                                                self.screen,
                                                (0, 0, 255),  # Bleu pour indiquer la cible sélectionnée
                                                (valid_targets[current_target_idx][0] * CELL_SIZE,
                                                valid_targets[current_target_idx][1] * CELL_SIZE,
                                                CELL_SIZE, CELL_SIZE),
                                                3  # Épaisseur du contour pour le curseur
                                            )
                                            pygame.display.flip()
                                            clock.tick(30)

                                else:
                                    print("No skills available.")
                            has_acted = True
                            selected_unit.is_selected = False
                        else:
                            print("Cannot move to wall position!")

            # Vérifier les conditions de victoire/défaite
            if not self.enemy_units:
                break

    def handle_enemy_turn(self):
        for enemy in self.enemy_units:
            if enemy.stunned:
                print(f"{enemy.team} unit is stunned and cannot act this turn.")
                enemy.end_turn()  # Fin du tour, réinitialiser le stun
                continue
            # Vérifie qu'il reste des cibles disponibles
            if not self.player_units:
                return

            # Sélectionne une cible valide
            target = random.choice(self.player_units)

            # Se rapproche de la cible dans les limites de la vitesse
            moves_left = enemy.speed
            while moves_left > 0:
                dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
                dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0

                # Vérifie si le mouvement est valide
                distance = abs(dx) + abs(dy)
                new_x = enemy.x + dx
                new_y = enemy.y + dy

                if (0 <= new_x < GRID_COLS and
                    0 <= new_y < GRID_ROWS and
                    self.board.cells[new_y][new_x].type != "wall" and
                    self.board.cells[new_y][new_x].unit is None):
                    self.board.remove_unit(enemy)
                    enemy.x, enemy.y = new_x, new_y
                    self.board.add_unit(enemy)
                    moves_left -= 1
                    self.flip_display()
                else:
                    # Si le mouvement n'est pas valide, casse la boucle
                    break

            # Vérifie si l'ennemi est adjacent à la cible pour attaquer
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target, self)  # Passe le jeu pour gérer les unités mortes
                self.flip_display()

                # Si la cible est morte, retire-la
                if target.health <= 0:
                    self.player_units.remove(target)
                    self.board.remove_unit(target)
            
            # Vérifier les conditions de victoire/défaite
            if not self.player_units:
                break

    def get_attackable_targets(self, unit):
        """Retourne les cases où l'unité peut attaquer (en fonction des compétences)."""
        attackable_targets = []
        for skill in unit.skills:
            # Utiliser la portée de la compétence, pas de l'unité
            range_ = skill.range
            for dx in range(-range_, range_ + 1):  # Vérifie la portée de l'attaque
                for dy in range(-range_, range_ + 1):
                    target_x = unit.x + dx
                    target_y = unit.y + dy
                    if (0 <= target_x < GRID_COLS and 0 <= target_y < GRID_ROWS):
                        # Vérifie si une unité ennemie se trouve sur la case
                        target_unit = self.board.cells[target_y][target_x].unit
                        if target_unit and target_unit.team != unit.team:
                            attackable_targets.append((target_x, target_y))
        return attackable_targets
    
    def get_heal_targets(self, unit):
        """Return a list of teammates that can be healed by the skill."""
        heal_targets = []
        for dx in range(-1, 2):  # Adjust range as needed
            for dy in range(-1, 2):
                target_x = unit.x + dx
                target_y = unit.y + dy
                if (0 <= target_x < GRID_COLS and 0 <= target_y < GRID_ROWS):
                    target_unit = self.board.cells[target_y][target_x].unit
                    if target_unit and target_unit.team == unit.team and target_unit != unit:  # Ensure it's a teammate
                        heal_targets.append((target_x, target_y))
        return heal_targets
    
    def get_buffable_targets(self, unit, skill):
        """Return a list of teammates that can be buffed by the skill."""
        buffable_targets = []
        for dx in range(-skill.range, skill.range + 1):  # Adjust range as needed
            for dy in range(-skill.range, skill.range + 1):
                target_x = unit.x + dx
                target_y = unit.y + dy
                distance = abs(dx) + abs(dy)

                if (0 <= target_x < GRID_COLS and 0 <= target_y < GRID_ROWS and distance <= skill.range):
                    target_unit = self.board.cells[target_y][target_x].unit
                    if target_unit and target_unit.team == unit.team and target_unit != unit:  # Ensure it's a teammate
                        buffable_targets.append((target_x, target_y))
        
        return buffable_targets

    def display_attack_radius(self, unit, radius):
        """Affiche les cases accessibles autour de l'unité sélectionnée, mais seulement celles occupées par des ennemis."""

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                target_x = unit.x + dx
                target_y = unit.y + dy
                distance = abs(dx) + abs(dy)

                # Vérifie si la case cible est dans les limites et dans la portée d'attaque
                if (0 <= target_x < GRID_COLS and
                    0 <= target_y < GRID_ROWS and
                    distance <= radius):
                    
                    target_unit = self.board.cells[target_y][target_x].unit

                    # Vérifie si la case contient une unité ennemie
                    if target_unit and target_unit.team != unit.team:
                        # Dessiner un contour pour les cases contenant une cible ennemie
                        pygame.draw.rect(
                            self.screen,
                            (255, 0, 0),  # Rouge pour indiquer les cibles ennemies à portée
                            (target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                            2  # Épaisseur du contour
                        )

    def get_available_skills(self, unit):
        available_skills = []
        for skill in unit.skills:
            # If the skill is a healing skill, we check if there are any valid teammates in range
            if isinstance(skill, HealSkill):
                # Filter for teammates within range who are not at full health
                heal_targets = self.get_heal_targets(unit)
                healable_targets = [target for target in heal_targets
                                    if self.board.cells[target[1]][target[0]].unit.health < self.board.cells[target[1]][target[0]].unit.max_health]
                if healable_targets:  # If there are teammates to heal
                    available_skills.append(skill)

            # If the skill is a buffing skill, we check if there are any valid teammates in range
            elif isinstance(skill, BuffSkill):
                # Filter for teammates within range
                buffable_targets = self.get_buffable_targets(unit, skill)
                if buffable_targets:  # If there are teammates to buff
                    available_skills.append(skill)

            # If the skill is a damage skill, we check for enemies in range
            elif isinstance(skill, Skill):
                has_target = any(
                    abs(unit.x - enemy.x) + abs(unit.y - enemy.y) <= skill.range
                    for enemy in (self.enemy_units if unit.team == 'player' else self.player_units)
                )
                if has_target:
                    available_skills.append(skill)

        return available_skills

    def get_attackable_targets(self, unit, skill):
        return [
            (enemy.x, enemy.y)
            for enemy in (self.enemy_units if unit.team == 'player' else self.player_units)
            if abs(unit.x - enemy.x) + abs(unit.y - enemy.y) <= skill.range
        ]


    def display_attack_radius(self, unit, radius):
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                target_x = unit.x + dx
                target_y = unit.y + dy
                distance = abs(dx) + abs(dy)
                if self.board.is_traversable(target_x, target_y, unit.x, unit.y, unit) and distance <= radius:

                    pygame.draw.rect(
                        self.screen,
                        (100, 100, 255),  # Bleu clair pour afficher la portée
                        (target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                        2
                    )


    def display_skill_menu(self, unit, available_skills):
            """
            Affiche le menu des compétences disponibles pour une unité sélectionnée,
            avec des boutons de taille définie et des textes centrés.
            """
            font = pygame.font.Font(None, 36)
            skill_buttons = []

            # Dimensions fixes des boutons
            button_width = 300  # Largeur du bouton
            button_height = 60  # Hauteur du bouton
            vertical_spacing = 10  # Espacement vertical entre les boutons

            # Initialisation des boutons et calcul de leur position
            for i, skill in enumerate(available_skills):
                button_x = 10 
                button_y = 500 + i * (button_height + vertical_spacing)
                button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                skill_buttons.append((button_rect, skill))

            button_areas = [button_rect for button_rect, _ in skill_buttons] 

            while True:
                mouse_pos = pygame.mouse.get_pos()

                for button_rect, skill in skill_buttons:

                    if button_rect.collidepoint(mouse_pos):
                        button_color = (250, 250, 205, 10)
                    else:
                        button_color = (135, 206, 250, 10)

                    # Créer une surface semi-transparente pour le bouton
                    button_surface = pygame.Surface((button_rect.width, button_rect.height), pygame.SRCALPHA)
                    button_surface.fill(button_color)

                    # Effacer et redessiner le bouton
                    self.screen.blit(button_surface, (button_rect.x, button_rect.y))

                    # Centrer le texte sur le bouton
                    text_surface = font.render(f"{skill.name}: Range {skill.range}", True, (0, 0, 0))
                    text_x = button_rect.x + (button_rect.width - text_surface.get_width()) // 2
                    text_y = button_rect.y + (button_rect.height - text_surface.get_height()) // 2
                    self.screen.blit(text_surface, (text_x, text_y))

                # Mettre à jour uniquement les zones des boutons
                pygame.display.update(button_areas)

                # Gestion des événements utilisateur
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Clic gauche
                            for button_rect, skill in skill_buttons:
                                if button_rect.collidepoint(mouse_pos):
                                    return skill  # Retourner la compétence sélectionnée
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        return None  # Quitter le menu si "Échap" est pressé

    def handle_attack(self, unit, skill, targets):
        if isinstance(skill):
            target_chosen = False
            current_target_idx = 0

            while not target_chosen:
                # Afficher la portée de la compétence
                self.display_attack_radius(unit, skill.range)

                # Dessiner les cases valides et mettre en évidence la cible actuelle
                for i, target in enumerate(targets):
                    if i == current_target_idx:  # Mettre en évidence la cible actuelle
                        pygame.draw.rect(
                            self.screen,
                            (0, 255, 255),  # Cyan pour la cible actuelle
                            (target[0] * CELL_SIZE, target[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                            3
                        )
                    else:  # Effacer la mise en évidence précédente
                        pygame.draw.rect(
                            self.screen,
                            (0, 0, 0),  # Noir pour réinitialiser
                            (target[0] * CELL_SIZE, target[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                            3
                        )
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            current_target_idx = (current_target_idx + 1) % len(targets)  # Passer à la cible suivante
                        elif event.key == pygame.K_UP:
                            current_target_idx = (current_target_idx - 1) % len(targets)  # Passer à la cible précédente
                        elif event.key == pygame.K_SPACE:  # Confirmer la cible
                            target_x, target_y = targets[current_target_idx]
                            # Ici, aucune modification du type "river" ou des propriétés de cellule
                            target_chosen = True
                        elif event.key == pygame.K_ESCAPE:  # Annuler
                            return
            return





    def display_movement_radius(self, unit, radius):
        """Affiche les cases accessibles autour de l'unité sélectionnée."""
        
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                target_x = unit.x + dx
                target_y = unit.y + dy
                distance = abs(dx) + abs(dy)

                # Vérifie si la case cible est dans les limites et accessible
                if (0 <= target_x < GRID_COLS and
                    0 <= target_y < GRID_ROWS and
                    distance <= radius and
                    self.board.cells[target_y][target_x].type != "obstacle" and
                    self.board.cells[target_y][target_x].unit is None):
                    
                    # Dessiner un contour pour les cases accessibles
                    pygame.draw.rect(
                        self.screen,
                        (100, 100, 255),  # Couleur bleue pour indiquer les cases accessibles
                        (target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                        2
                    )
    

    def display_buff_radius(self, unit, radius):
        """Displays the range of the buff skill around the selected unit."""
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                target_x = unit.x + dx
                target_y = unit.y + dy
                distance = abs(dx) + abs(dy)

                if self.board.is_traversable(target_x, target_y, unit.x, unit.y, unit) and distance <= radius:
                    pygame.draw.rect(
                        self.screen,
                        (0, 255, 0),  # Green to show the buffable area
                        (target_x * CELL_SIZE, target_y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                        2
                    )
        pygame.display.flip()