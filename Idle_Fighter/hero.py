"""The player's hero: everything that is kept between fights and saved to disk."""
from __future__ import annotations

import time
from dataclasses import dataclass, field

from characters import CLASSES, Fighter, Stats
from shop import apply_upgrades
from tactics import Tactics

XP_BASE, XP_GROWTH = 20, 1.3
LEVEL_BONUS = 1.05  # damage, health and shield multiplier per hero level
MANA_AFTER_WIN = 0.1  # share of max mana restored after each win (mana carries over between fights)


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
    carried_mana: float | None = None  # mana left from the last fight, None = full
    upgrades: dict[str, int] = field(default_factory=dict)
    tactics: Tactics = field(default_factory=Tactics)
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
        """A Fighter for the next fight: full health and shield, mana carried over from the last fight."""
        fighter = Fighter(self.name, self.stats(), CLASSES[self.spec].ability)
        if self.carried_mana is not None:
            fighter.mana = min(self.carried_mana, fighter.stats.mana)
        return fighter

    def after_fight(self, fighter: Fighter, won: bool) -> None:
        """Keep the mana left after a win (plus a little rest). A defeat means a full recovery."""
        if won:
            self.carried_mana = min(fighter.stats.mana, fighter.mana + fighter.stats.mana * MANA_AFTER_WIN)
        else:
            self.carried_mana = None
