"""Special abilities. Every class (and some enemies) has one, paid for with mana."""
from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from characters import Fighter


class Ability:
    """Base class: subclasses set name, cost and description and implement use()."""

    name: str = "Ability"
    cost: float = 0
    description: str = ""

    def useful(self, user: Fighter, target: Fighter) -> bool:
        """Whether using the ability now makes sense (e.g. no healing at full health)."""
        return True

    def use(self, user: Fighter, target: Fighter, rng: random.Random) -> str:
        """Apply the effect and return a short description of what happened."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"


def hit_text(name: str, damage: float, crit: bool) -> str:
    return f"{name} {damage:.0f}" + (" CRIT!" if crit else "")


class Cleave(Ability):
    name, cost, description = "Cleave", 20, "Hit for double damage"

    def use(self, user, target, rng):
        damage, crit = user.attack(target, rng, multiplier=2)
        return hit_text(self.name, damage, crit)


class AimedShot(Ability):
    name, cost, description = "Aimed Shot", 25, "1.5x damage with +50% crit chance"

    def use(self, user, target, rng):
        damage, crit = user.attack(target, rng, multiplier=1.5, crit_bonus=0.5)
        return hit_text(self.name, damage, crit)


class ShieldWall(Ability):
    name, cost, description = "Shield Wall", 15, "Restore half of your maximum shield"

    def useful(self, user, target):
        return user.shield < user.stats.shield * 0.5

    def use(self, user, target, rng):
        restored = user.restore_shield(user.stats.shield * 0.5)
        return f"{self.name} +{restored:.0f} shield"


class Heal(Ability):
    name, cost, description = "Heal", 25, "Restore 35% of your maximum health"

    def useful(self, user, target):
        return user.health < user.stats.health * 0.7

    def use(self, user, target, rng):
        healed = user.heal(user.stats.health * 0.35)
        return f"{self.name} +{healed:.0f} HP"


class Backstab(Ability):
    name, cost, description = "Backstab", 30, "A guaranteed critical hit"

    def use(self, user, target, rng):
        damage, _ = user.attack(target, rng, always_crit=True)
        return hit_text(self.name, damage, True)


class Fireball(Ability):
    name, cost, description = "Fireball", 30, "1.5x damage that ignores shields"

    def use(self, user, target, rng):
        damage, crit = user.attack(target, rng, multiplier=1.5, ignore_shield=True)
        return hit_text(self.name, damage, crit)


class Weaken(Ability):
    name, cost, description = "Weaken", 20, "Normal hit, and the target deals 20% less damage (stacks to -50%)"
    MIN_MULTIPLIER = 0.5

    def useful(self, user, target):
        return target.damage_multiplier > self.MIN_MULTIPLIER

    def use(self, user, target, rng):
        damage, crit = user.attack(target, rng)
        target.damage_multiplier = max(self.MIN_MULTIPLIER, target.damage_multiplier * 0.8)
        return hit_text(self.name, damage, crit) + " (-20% dmg)"
