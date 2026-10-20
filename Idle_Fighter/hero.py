"""The player's hero: everything that is kept between fights and saved to disk."""
from __future__ import annotations

import time
from dataclasses import dataclass, field

from characters import CLASSES, Fighter, Stats
from shop import apply_upgrades

XP_BASE, XP_GROWTH = 20, 1.3
LEVEL_BONUS = 1.05  # damage, health and shield multiplier per hero level


@dataclass
class Hero:
    spec: str                      # class name, e.g. "Mage"
    level: int = 1
    xp: int = 0
    gold: int = 0
    stage: int = 1                 # stage the next fight takes place on
    best_stage: int = 0            # highest stage cleared
    retry_stage: int | None = None  # stage lost on, retried after farming
    farm_wins: int = 0
    upgrades: dict[str, int] = field(default_factory=dict)
    last_seen: float = field(default_factory=time.time)

    @property
    def name(self) -> str:
        return CLASSES[self.spec].name

    def xp_needed(self) -> int:
        """XP needed to reach the next hero level."""
        return round(XP_BASE * XP_GROWTH ** (self.level - 1))

    def gain(self, gold: int, xp: int) -> int:
        """Add gold and XP and level up as often as the XP allows. Returns the number of levels gained."""
        self.gold += gold
        self.xp += xp
        levels = 0
        while self.xp >= self.xp_needed():
            self.xp -= self.xp_needed()
            self.level += 1
            levels += 1
        return levels

    def stats(self) -> Stats:
        """Class stats boosted by hero level and bought upgrades."""
        bonus = LEVEL_BONUS ** (self.level - 1)
        return apply_upgrades(CLASSES[self.spec].stats.scaled(damage=bonus, defence=bonus), self.upgrades)

    def make_fighter(self) -> Fighter:
        """A fresh, fully healed Fighter for the next fight."""
        return Fighter(self.name, self.stats(), CLASSES[self.spec].ability)
