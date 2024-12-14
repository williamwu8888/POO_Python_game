from plantuml import PlantUML

# Définition du diagramme UML
uml_code = """
@startuml
' Grouper les classes similaires pour réduire la largeur
package "Unités" {
  class Unit {
    - x: int
    - y: int
    - health: int
    - attack_power: int
    - defense: int
    - team: string
    - skills: List<Skill>
    + move(dx: int, dy: int): void
    + attack(target: Unit): void
  }

  class WarriorUnit {
    + __init__(x: int, y: int, team: string): void
  }

  class KnightUnit {
    + __init__(x: int, y: int, team: string): void
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

  Unit <|-- WarriorUnit
  Unit <|-- KnightUnit
  Unit <|-- ArcherUnit
  Unit <|-- MageUnit
  Unit <|-- HealerUnit
  Unit <|-- SupportUnit
}

package "Compétences" {
  class Skill {
    - name: string
    - power: int
    - range: int
    - accuracy: float
    + use(attacker: Unit, target: Unit): void
  }

  class DamageSkill
  class HealSkill
  class BuffSkill

  Skill <|-- DamageSkill
  Skill <|-- HealSkill
  Skill <|-- BuffSkill
}

package "Plateau" {
  class Cell {
    - type: string
    - unit: Unit
  }

  class Board {
    - cells: List<List<Cell>>
    + add_unit(unit: Unit): void
    + remove_unit(unit: Unit): void
  }

  class Wall {
    - x: int
    - y: int
    - traversable: bool
    + __init__(x: int, y: int, board: Board): void
  }

  Board --> Cell : contains
  Board --> Wall : has
}

package "Jeu" {
  class Game {
    - screen: pygame.Surface
    - player_units: List<Unit>
    - enemy_units: List<Unit>
    - board: Board
    + handle_player_turn(): void
    + handle_enemy_turn(): void
  }

  Game --> Board : uses
  Game --> Wall : contains
}
@enduml
"""

# Sauvegarde du code UML dans un fichier
with open("game_diagram.uml", "w") as file:
    file.write(uml_code)

# Création de l'instance PlantUML et génération du diagramme
plantuml = PlantUML(url='http://www.plantuml.com/plantuml/img/')
plantuml.processes_file('game_diagram.uml')  # Génère le diagramme à partir du fichier UML
