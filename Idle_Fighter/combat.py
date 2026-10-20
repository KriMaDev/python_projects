"""Turn-based fight between two Fighters. Pure logic: printing happens through the on_turn callback."""
from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass

from characters import Fighter

MAX_TURNS = 100  # a fight that takes longer counts as lost

ATTACK, SKILL, DEFEND = "attack", "skill", "defend"

# Gets (actor, opponent) and returns ATTACK, SKILL or DEFEND
ActionChooser = Callable[[Fighter, Fighter], str]
# Gets (turn, hero, enemy, what happened this turn)
TurnCallback = Callable[[int, Fighter, Fighter, list[str]], None]


@dataclass
class FightResult:
    won: bool
    turns: int


def enemy_action(enemy: Fighter, hero: Fighter) -> str:
    """Enemies use their ability whenever they can and it helps, otherwise they attack."""
    if enemy.can_use_ability() and enemy.ability.useful(enemy, hero):
        return SKILL
    return ATTACK


def take_turn(actor: Fighter, target: Fighter, action: str, rng: random.Random) -> str:
    """Perform one action and describe it."""
    actor.defending = False
    if action == SKILL and actor.can_use_ability():
        actor.mana -= actor.ability.cost
        return actor.ability.use(actor, target, rng)
    if action == DEFEND:
        actor.defending = True
        actor.restore_mana(actor.stats.mana * 0.2)
        return "Defend"
    damage, crit = actor.attack(target, rng)
    return f"Hit {damage:.0f}" + (" CRIT!" if crit else "")


def fight(hero: Fighter, enemy: Fighter, rng: random.Random, choose_action: ActionChooser,
          on_turn: TurnCallback | None = None) -> FightResult:
    """Hero and enemy take turns (hero first) until one falls or MAX_TURNS pass."""
    for turn in range(1, MAX_TURNS + 1):
        events = [take_turn(hero, enemy, choose_action(hero, enemy), rng)]
        if enemy.alive:
            events.append(f"{enemy.name}: {take_turn(enemy, hero, enemy_action(enemy, hero), rng)}")
            hero.regenerate()
            enemy.regenerate()
        if on_turn:
            on_turn(turn, hero, enemy, events)
        if not enemy.alive:
            return FightResult(won=True, turns=turn)
        if not hero.alive:
            return FightResult(won=False, turns=turn)
    return FightResult(won=False, turns=MAX_TURNS)
