"""Stats, the playable classes and the Fighter used in combat."""
from __future__ import annotations

import random
from dataclasses import dataclass, field, replace

from abilities import Ability, AimedShot, Backstab, Cleave, Fireball, Heal, ShieldWall, Weaken


@dataclass(frozen=True)
class Stats:
    """Maximum values and per-turn regeneration of a fighter."""

    damage: float
    crit_chance: float      # 0.25 = 25% chance per hit
    crit_multiplier: float  # damage multiplier on a critical hit
    health: float
    mana: float
    shield: float           # absorbs damage before health
    health_regen: float     # per turn
    mana_regen: float
    shield_regen: float

    def scaled(self, damage: float = 1, defence: float = 1, regen: float = 1) -> Stats:
        """Return a copy with damage, health/shield and regeneration multiplied."""
        return replace(self, damage=self.damage * damage, health=self.health * defence, shield=self.shield * defence,
                       health_regen=self.health_regen * regen, shield_regen=self.shield_regen * regen)


@dataclass(frozen=True)
class HeroClass:
    name: str      # character name
    stats: Stats
    ability: Ability


# Starting stats per class
CLASSES = {
    "Melee":    HeroClass("Sir Smacks-a-Lot", Stats(16,   0.20, 3,   110, 50,  50,  1.5, 1.5, 1),   Cleave()),
    "Ranged":   HeroClass("Robin Hoodie",     Stats(20,   0.25, 3.5, 50,  75,  50,  0.7, 1,   0.7), AimedShot()),
    "Tank":     HeroClass("Captain Bulwark",  Stats(7.5,  0.15, 4.5, 150, 25,  150, 2,   1.5, 2),   ShieldWall()),
    "Support":  HeroClass("Medic Molly",      Stats(15,   0.35, 2.5, 75,  75,  100, 1.5, 2,   1),   Heal()),
    "Assassin": HeroClass("Mister Ladybug",   Stats(35,   0.45, 4,   40,  75,  30,  1,   1.5, 1),   Backstab()),
    "Mage":     HeroClass("Perry Hotter",     Stats(25,   0.55, 2.5, 40,  100, 150, 1,   2,   2),   Fireball()),
    "Debuffer": HeroClass("Asmodeus",         Stats(17.5, 0.40, 3,   75,  75,  100, 0.5, 1,   0.5), Weaken()),
}


def find_class(spec: str) -> str:
    """Return the class name matching spec (case-insensitive). Raises ValueError if unknown."""
    spec = spec.strip().capitalize()
    if spec not in CLASSES:
        raise ValueError(f"Unknown class '{spec}'. Choose from: {', '.join(CLASSES)}")
    return spec


@dataclass
class Fighter:
    """A hero or enemy during one fight. Starts with full health, shield and mana."""

    name: str
    stats: Stats
    ability: Ability | None = None
    health: float = field(init=False)
    shield: float = field(init=False)
    mana: float = field(init=False)
    defending: bool = field(default=False, init=False)
    damage_multiplier: float = field(default=1.0, init=False)  # lowered by Weaken

    def __post_init__(self) -> None:
        self.health = self.stats.health
        self.shield = self.stats.shield
        self.mana = self.stats.mana

    @property
    def alive(self) -> bool:
        return self.health > 0

    def can_use_ability(self) -> bool:
        return self.ability is not None and self.mana >= self.ability.cost

    def attack(self, target: Fighter, rng: random.Random, multiplier: float = 1, crit_bonus: float = 0,
               always_crit: bool = False, ignore_shield: bool = False) -> tuple[float, bool]:
        """Hit the target. Returns (damage dealt, whether it was a critical hit)."""
        damage = self.stats.damage * self.damage_multiplier * multiplier
        crit = always_crit or rng.random() < self.stats.crit_chance + crit_bonus
        if crit:
            damage *= self.stats.crit_multiplier
        return target.take_damage(damage, ignore_shield), crit

    def take_damage(self, amount: float, ignore_shield: bool = False) -> float:
        """Lose shield first, then health. Defending halves the damage. Returns the damage taken."""
        if self.defending:
            amount *= 0.5
        remaining = amount
        if not ignore_shield:
            absorbed = min(self.shield, remaining)
            self.shield -= absorbed
            remaining -= absorbed
        self.health = max(0.0, self.health - remaining)
        return amount

    def heal(self, amount: float) -> float:
        """Restore health up to the maximum. Returns how much was healed."""
        healed = min(amount, self.stats.health - self.health)
        self.health += healed
        return healed

    def restore_shield(self, amount: float) -> float:
        restored = min(amount, self.stats.shield - self.shield)
        self.shield += restored
        return restored

    def restore_mana(self, amount: float) -> float:
        restored = min(amount, self.stats.mana - self.mana)
        self.mana += restored
        return restored

    def regenerate(self) -> None:
        """End of turn regeneration of health, shield and mana."""
        if self.alive:
            self.heal(self.stats.health_regen)
            self.restore_shield(self.stats.shield_regen)
            self.restore_mana(self.stats.mana_regen)
