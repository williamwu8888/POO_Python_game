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
            print(f"{attacker.team.capitalize()} unit ({attacker.__class__.__name__}) uses {self.name} on "
                  f"{target.team.capitalize()} unit ({target.__class__.__name__}), dealing {damage} damage.")
            target.receive_damage(damage, game)
        else:
            print(f"{attacker.team.capitalize()} unit ({attacker.__class__.__name__}) missed with {self.name}!")

    def calculate_damage(self, attacker, target):
        return max(0, self.power + attacker.attack_power - target.defense)

class Stun(Skill):
    def __init__(self, name, power, range, accuracy):
        super().__init__(name, power, range, accuracy, area_of_effect=1)

    def use(self, attacker, target, game):
        if random.random() < self.accuracy:
            damage = self.calculate_damage(attacker, target)
            print(f"{attacker.team.capitalize()} unit ({attacker.__class__.__name__}) uses {self.name} on "
                  f"{target.team.capitalize()} unit ({target.__class__.__name__}), dealing {damage} damage and stunning!")
            target.receive_damage(damage, game)
            target.stunned = True  # Apply the stun effect
        else:
            print(f"{attacker.team.capitalize()} unit ({attacker.__class__.__name__}) missed with {self.name}!")


class BuffSkill(Skill):
    def __init__(self, name, stat_to_buff, buff_amount, range):
        super().__init__(name, power=0, range=range, accuracy=1, area_of_effect=1)
        self.stat_to_buff = stat_to_buff
        self.buff_amount = buff_amount

    def use(self, caster, target, game):
        # Apply the buff only if the target is a teammate
        if target.team == caster.team:
            # Print with more detailed information about the caster, target, and stat being buffed
            print(f"{caster.team.capitalize()} unit ({caster.__class__.__name__}) buffs "
                  f"{target.team.capitalize()} unit ({target.__class__.__name__})'s "
                  f"{self.stat_to_buff} by {self.buff_amount}.")
            
            # Apply the buff
            setattr(target, self.stat_to_buff, getattr(target, self.stat_to_buff) + self.buff_amount)
        else:
            print(f"{caster.team.capitalize()} unit ({caster.__class__.__name__}) cannot buff "
                  f"{target.team.capitalize()} unit ({target.__class__.__name__}) as they are an enemy.")


class DebuffSkill(Skill):
    def __init__(self, name, stat_to_debuff, debuff_amount, range):
        super().__init__(name, power=0, range=range, accuracy=1, area_of_effect=1)
        self.stat_to_debuff = stat_to_debuff
        self.debuff_amount = debuff_amount

    def use(self, caster, target, game):
        setattr(target, self.stat_to_debuff, getattr(target, self.stat_to_debuff) + self.debuff_amount)
        print(f"{caster.team.capitalize()} unit ({caster.__class__.__name__}) debuffs "
              f"{target.team.capitalize()} unit ({target.__class__.__name__})'s "
              f"{self.stat_to_debuff} by {self.debuff_amount}.")


class FireballSkill(Skill):
    def __init__(self, name, power, range, accuracy):
        super().__init__(name, power, range, accuracy, area_of_effect=2)

    def use(self, attacker, target, game):
        if random.random() < self.accuracy:
            damage = self.calculate_damage(attacker, target)
            print(f"{attacker.team.capitalize()} unit ({attacker.__class__.__name__}) casts {self.name} on "
                  f"{target.team.capitalize()} unit ({target.__class__.__name__}), dealing {damage} damage.")
            target.receive_damage(damage, game)
        else:
            print(f"{attacker.team.capitalize()} unit ({attacker.__class__.__name__}) missed with {self.name}!")


class ArrowShot(Skill):
    def __init__(self, name, power, range, accuracy):
        super().__init__(name, power, range, accuracy, area_of_effect=1)

    def use(self, attacker, target, game):
        if random.random() < self.accuracy:
            damage = self.calculate_damage(attacker, target)
            print(f"{attacker.team.capitalize()} unit ({attacker.__class__.__name__}) shoots {self.name} at "
                  f"{target.team.capitalize()} unit ({target.__class__.__name__}), dealing {damage} damage.")
            target.receive_damage(damage, game)
        else:
            print(f"{attacker.team.capitalize()} unit ({attacker.__class__.__name__}) missed with {self.name}!")


class HealSkill(Skill):
    def __init__(self, name, healing_amount, range, accuracy):
        super().__init__(name, healing_amount, range, accuracy, area_of_effect=1)

    def use(self, healer, target, game):
        if random.random() < self.accuracy:
            healing = self.power
            target.health = min(target.max_health, target.health + healing)
            print(f"{healer.team.capitalize()} unit ({healer.__class__.__name__}) heals "
                  f"{target.team.capitalize()} unit ({target.__class__.__name__}) for {healing} HP.")

class FireballSkill(Skill):
    def __init__(self, name, power, range, accuracy):
        super().__init__(name, power, range, accuracy, area_of_effect=2)  # Area of effect set to 2

    def use(self, attacker, target, game):
        if random.random() < self.accuracy:
            damage = self.calculate_damage(attacker, target)
            print(f"{attacker.team.capitalize()} unit ({attacker.__class__.__name__}) casts {self.name} on "
                  f"{target.team.capitalize()} unit ({target.__class__.__name__}), dealing {damage} damage.")
            target.receive_damage(damage, game)
        else:
            print(f"{attacker.team.capitalize()} unit ({attacker.__class__.__name__}) missed with {self.name}!")

class HealAllSkill(HealSkill):
    def __init__(self, name, healing_amount, range, accuracy):
        super().__init__(name, healing_amount, range, accuracy)

    def use(self, healer, target, game):
        # Heal all units in range, including the healer if desired
        if random.random() < self.accuracy:
            healing = self.power
            # Heal all units in range
            healed_units = []
            for unit in game.board.units_in_range(healer, self.range):  # Assuming you have a method like this
                unit.health = min(unit.max_health, unit.health + healing)
                healed_units.append(unit)

            for unit in healed_units:
                print(f"{healer.team.capitalize()} unit ({healer.__class__.__name__}) heals "
                      f"{unit.team.capitalize()} unit ({unit.__class__.__name__}) for {healing} HP.")
        else:
            print(f"{healer.team.capitalize()} unit ({healer.__class__.__name__}) missed with {self.name}!")

