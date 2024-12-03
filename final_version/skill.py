import random

class Skill:
    def __init__(self, name, power, range, accuracy, area_of_effect):
        self.name = name
        self.power = power
        self.range = range
        self.accuracy = accuracy
        self.area_of_effect = area_of_effect

    def use(self, attacker, target, game):
        if abs(attacker.x - target.x) + abs(attacker.y - target.y) > self.range:
            print(f"{self.name} échoue : cible hors de portée.")
            return

        if random.random() < self.accuracy:
            damage = self.calculate_damage(attacker, target)
            print(f"{attacker.team} unit uses {self.name} on {target.team}, dealing {damage} damage.")
            target.receive_damage(damage, game)
        else:
            print(f"{attacker.team} unit missed with {self.name}!")

    def calculate_damage(self, attacker, target):
        return max(0, self.power + attacker.attack_power - target.defense)
