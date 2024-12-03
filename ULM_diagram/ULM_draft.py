from plantuml import PlantUML

uml_code = """
@startuml
class Skill {
  - power: int
  - range: int
  - accuracy: float
  - area_of_effect: int
  + use(attacker: Unit, target: Unit): void
  + calculate_damage(attacker: Unit, target: Unit): int
}

class Unit {
  - x: int
  - y: int
  - health: int
  - attack_power: int
  - defense: int
  - team: string
  - skills: List<Skill>
  - is_selected: bool
  + move(dx: int, dy: int): void
  + attack(target: Unit): void
  + receive_damage(damage: int): void
  + draw(screen: pygame.Surface): void
}

class Cell {
  - type: string
  - unit: Unit
  + __str__(): string
}

class Board {
  - cells: List<List<Cell>]
  + display(screen: pygame.Surface): void
  + add_unit(unit: Unit): void
  + remove_unit(unit: Unit): void
}

class Game {
  - screen: pygame.Surface
  - player_units: List<Unit>
  - enemy_units: List<Unit>
  - board: Board
  + handle_player_turn(): void
  + handle_enemy_turn(): void
  + flip_display(): void
}

Skill --> Unit : uses
Unit --> Board : moves on
Board --> Cell : contains
Game --> Board : uses
@enduml
"""

# Save the UML code in a file
with open("game_diagram_en.uml", "w") as file:
    file.write(uml_code)

# Create an instance of PlantUML and generate the diagram
plantuml = PlantUML(url='http://www.plantuml.com/plantuml/img/')
plantuml.processes_file('game_diagram_en.uml')  # Generates the diagram from the .uml file