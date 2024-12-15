from plantuml import PlantUML

# Définition du diagramme UML
uml_code = """
@startuml
' Forcer une disposition verticale (Top to Bottom)
skinparam layoutPadding 10
skinparam classFontSize 12
skinparam classFontName "Arial"

' Forcer l'alignement de tous les éléments verticalement
left to right direction

' Package "Unités" placé en haut
package "Unités" {
  class BaseUnit {
    - x: int
    - y: int
    - health: int
    - max_health: int
    - attack_power: int
    - defense: int
    - team: string
    - skills: List<Skill>
    - is_selected: bool
    - speed: int
    - stunned: bool
    + move(dx: int, dy: int, board: Board): void
    + attack(target: Unit, game: Game): void
    + receive_damage(damage: int, game: Game): void
    + end_turn(): void
    + draw(screen: pygame.Surface): void
  }

  class WarriorUnit {
    + __init__(x: int, y: int, team: string): void
    + attack(target: Unit, game: Game): void
  }

  class KnightUnit {
    + __init__(x: int, y: int, team: string): void
    + move(dx: int, dy: int, board: Board): void
  }

  class ArcherUnit {
    + __init__(x: int, y: int, team: string): void
  }

  class MageUnit {
    + __init__(x: int, y: int, team: string): void
  }

  class HealerUnit {
    + __init__(x: int, y: int, team: string): void
  }

  class SupportUnit {
    + __init__(x: int, y: int, team: string): void
  }

  BaseUnit <|-- WarriorUnit
  BaseUnit <|-- KnightUnit
  BaseUnit <|-- ArcherUnit
  BaseUnit <|-- MageUnit
  BaseUnit <|-- HealerUnit
  BaseUnit <|-- SupportUnit
}

' Package "Compétences" en dessous de "Unités"
package "Compétences" {
  class Skill {
    - name: string
    - power: int
    - range: int
    - accuracy: float
    + use(attacker: Unit, target: Unit, game: Game): void
  }

  class Stun {
    + use(attacker: Unit, target: Unit, game: Game): void
  }

  class BuffSkill {
    - stat_to_buff: string
    - buff_amount: int
    + use(caster: Unit, target: Unit, game: Game): void
  }

  class HealSkill {
    - healing_amount: int
    + use(healer: Unit, target: Unit, game: Game): void
  }

  class DebuffSkill {
    - stat_to_debuff: string
    - debuff_amount: int
    + use(caster: Unit, target: Unit, game: Game): void
  }

  class FireballSkill {
    + use(attacker: Unit, target: Unit, game: Game): void
  }

  Skill <|-- Stun
  Skill <|-- BuffSkill
  Skill <|-- HealSkill
  Skill <|-- DebuffSkill
  Skill <|-- FireballSkill
}

' Package Plateau
package "Plateau" {
  class Cell {
    - type: string
    - unit: Unit
    - traversable: bool
    + __str__(): string
  }

  class Board {
    - cells: List<List<Cell>>
    + add_unit(unit: Unit): void
    + remove_unit(unit: Unit): void
    + is_traversable(x: int, y: int, x0: int, y0: int, unit: Unit): bool
    + is_another_unit(x: int, y: int, selected_unit: Unit): bool
    + display(screen: pygame.Surface): void
  }

  class Wall {
    - x: int
    - y: int
    - traversable: bool
    + __init__(x: int, y: int, board: Board): void
  }

  class River {
    - x: int
    - y: int
    - traversable: bool
    + __init__(x: int, y: int, board: Board): void
  }

  class Bush {
    - x: int
    - y: int
    + __init__(x: int, y: int, board: Board): void
  }

  Board --> Cell : contains
  Board --> Wall : has
  Board --> River : has
}

' Package Jeu
package "Jeu" {
  class Game {
    - screen: pygame.Surface
    - player_units: List<Unit>
    - enemy_units: List<Unit>
    - board: Board
    + handle_turn(): void
    + handle_player_turn(): void
    + handle_enemy_turn(): void
  }

  Game --> Board : uses
  Game --> Wall : contains
  Game --> River : contains
  Game --> Bush : contains
}

@enduml

"""

# Sauvegarde du code UML dans un fichier
with open("game_diagram.uml", "w") as file:
    file.write(uml_code)

# Création de l'instance PlantUML et génération du diagramme
plantuml = PlantUML(url='http://www.plantuml.com/plantuml/img/')
plantuml.processes_file('game_diagram.uml')  # Génère le diagramme à partir du fichier UML
