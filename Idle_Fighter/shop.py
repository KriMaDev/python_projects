"""Upgrades the hero can buy with gold. Each level costs more than the last."""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from characters import Stats

if TYPE_CHECKING:
    from hero import Hero


@dataclass(frozen=True)
class Upgrade:
    name: str
    description: str
    base_cost: int
    cost_growth: float
    max_level: int | None = None


UPGRADES = {
    "damage": Upgrade("Sharpen",    "+10% damage",                 15, 1.45),
    "health": Upgrade("Armor",      "+10% max health",             15, 1.45),
    "shield": Upgrade("Barrier",    "+10% max shield",             15, 1.45),
    "crit":   Upgrade("Focus",      "+2% crit chance",             25, 1.6, max_level=15),
    "mana":   Upgrade("Meditation", "+0.5 mana regen per turn",    20, 1.5, max_level=10),
}


def cost(key: str, level: int) -> int | None:
    """Gold needed to buy the next level of an upgrade, or None if it is maxed out."""
    upgrade = UPGRADES[key]
    if upgrade.max_level is not None and level >= upgrade.max_level:
        return None
    return round(upgrade.base_cost * upgrade.cost_growth ** level)


def apply_upgrades(stats: Stats, upgrades: dict[str, int]) -> Stats:
    """Return the stats with all bought upgrade levels applied."""
    return replace(
        stats,
        damage=stats.damage * 1.1 ** upgrades.get("damage", 0),
        health=stats.health * 1.1 ** upgrades.get("health", 0),
        shield=stats.shield * 1.1 ** upgrades.get("shield", 0),
        crit_chance=stats.crit_chance + 0.02 * upgrades.get("crit", 0),
        mana_regen=stats.mana_regen + 0.5 * upgrades.get("mana", 0),
    )


def buy(hero: Hero, key: str) -> bool:
    """Buy one level of an upgrade if the hero can afford it. Returns whether it was bought."""
    price = cost(key, hero.upgrades.get(key, 0))
    if price is None or hero.gold < price:
        return False
    hero.gold -= price
    hero.upgrades[key] = hero.upgrades.get(key, 0) + 1
    return True


def autobuy(hero: Hero) -> list[str]:
    """Keep buying the cheapest affordable upgrade. Returns the names of everything bought."""
    bought = []
    while True:
        prices = {key: cost(key, hero.upgrades.get(key, 0)) for key in UPGRADES}
        affordable = {key: price for key, price in prices.items() if price is not None and price <= hero.gold}
        if not affordable:
            return bought
        key = min(affordable, key=affordable.get)
        buy(hero, key)
        bought.append(UPGRADES[key].name)
