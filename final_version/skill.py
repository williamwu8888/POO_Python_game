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

class DamageSkill(Skill):
    def __init__(self, name, power, range, accuracy, area_of_effect):
        super().__init__(name, power, range, accuracy, area_of_effect)

    def use(self, attacker, target, game):
        if random.random() < self.accuracy:
            damage = self.calculate_damage(attacker, target)
            print(f"{attacker.team} unit uses {self.name} on {target.team}, dealing {damage} damage.")
            target.receive_damage(damage, game)
        else:
            print(f"{attacker.team} unit missed with {self.name}!")

class ShieldBash(Skill):
    def __init__(self, name, power, range, accuracy):
        super().__init__(name, power, range, accuracy, area_of_effect=1)

    def use(self, attacker, target, game):
        if random.random() < self.accuracy:
            damage = self.calculate_damage(attacker, target)
            print(f"{attacker.team} unit uses {self.name} on {target.team}, dealing {damage} damage and stunning!")
            target.receive_damage(damage, game)
            target.stunned = True  # Applique l'effet de stun
        else:
            print(f"{attacker.team} unit missed with {self.name}!")


class BuffSkill(Skill):
    def __init__(self, name, stat_to_buff, buff_amount, range):
        super().__init__(name, power=0, range=range, accuracy=1, area_of_effect=1)
        self.stat_to_buff = stat_to_buff
        self.buff_amount = buff_amount

    def use(self, caster, target, game):
        setattr(target, self.stat_to_buff, getattr(target, self.stat_to_buff) + self.buff_amount)
        print(f"{caster.team} unit buffs {target.team} unit's {self.stat_to_buff} by {self.buff_amount}.")

class FireballSkill(Skill):
    def __init__(self, name, power, range, accuracy):
        super().__init__(name, power, range, accuracy, area_of_effect=2)

    def use(self, attacker, target, game):
        if random.random() < self.accuracy:
            damage = self.calculate_damage(attacker, target)
            print(f"{attacker.team} unit casts {self.name} on {target.team}, dealing {damage} damage.")
            target.receive_damage(damage, game)
        else:
            print(f"{attacker.team} unit missed with {self.name}!")

class ArrowShot(Skill):
    def __init__(self, name, power, range, accuracy):
        super().__init__(name, power, range, accuracy, area_of_effect=1)

    def use(self, attacker, target, game):
        if random.random() < self.accuracy:
            damage = self.calculate_damage(attacker, target)
            print(f"{attacker.team} unit shoots {self.name} at {target.team}, dealing {damage} damage.")
            target.receive_damage(damage, game)
        else:
            print(f"{attacker.team} unit missed with {self.name}!")

class HealSkill(Skill):
    def __init__(self, name, healing_amount, range, accuracy):
        super().__init__(name, healing_amount, range, accuracy, area_of_effect=1)

    def use(self, healer, target, game):
        if random.random() < self.accuracy:
            healing = self.power
            target.health = min(target.max_health, target.health + healing)
            print(f"{healer.team} unit heals {target.team} unit for {healing} HP.")
