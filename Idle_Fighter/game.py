"""The idle loop: fight a stage, collect rewards, push forward or fall back and farm."""
from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass

from characters import Fighter
from combat import ActionChooser, TurnCallback, fight
from enemies import make_enemy, rewards, stage_kind
from hero import Hero

RETRY_AFTER_WINS = 5  # after a defeat, farm the previous stage this many times before retrying

# Gets the enemy kind (normal, mini boss, boss) and returns how the hero picks actions in that fight
ChooserFactory = Callable[[str], ActionChooser]
# Gets (stage, kind, hero, enemy) before the fight starts
StartCallback = Callable[[int, str, Fighter, Fighter], None]


@dataclass
class StageResult:
    stage: int
    kind: str
    enemy: str
    won: bool
    turns: int
    gold: int = 0
    xp: int = 0
    levels_gained: int = 0


def play_stage(hero: Hero, rng: random.Random, chooser_for: ChooserFactory,
               on_start: StartCallback | None = None, on_turn: TurnCallback | None = None) -> StageResult:
    """Fight the enemy of the hero's current stage and hand out the rewards. Does not move the hero."""
    stage, kind = hero.stage, stage_kind(hero.stage)
    fighter, enemy = hero.make_fighter(), make_enemy(stage, rng)
    if on_start:
        on_start(stage, kind, fighter, enemy)

    outcome = fight(fighter, enemy, rng, chooser_for(kind), on_turn)
    hero.after_fight(fighter, outcome.won)
    result = StageResult(stage, kind, enemy.name, outcome.won, outcome.turns)
    if outcome.won:
        result.gold, result.xp = rewards(stage)
        result.levels_gained = hero.gain(result.gold, result.xp)
    return result


def advance(hero: Hero, result: StageResult) -> str:
    """Move the hero after a fight and describe where they go next.

    Win: go to the next stage (or keep farming). Loss: fall back one stage and farm it
    RETRY_AFTER_WINS times, then retry the stage that was lost.
    """
    if not result.won:
        hero.retry_stage = max(hero.retry_stage or 0, result.stage)
        hero.farm_wins = 0
        hero.stage = max(1, result.stage - 1)
        return f"Falling back to stage {hero.stage} to farm. Retrying stage {hero.retry_stage} after {RETRY_AFTER_WINS} wins."

    hero.best_stage = max(hero.best_stage, result.stage)
    if hero.retry_stage is None:
        hero.stage = result.stage + 1
        return f"On to stage {hero.stage}."

    hero.farm_wins += 1
    if hero.farm_wins >= RETRY_AFTER_WINS:
        return retry_now(hero)
    return f"Farming: retrying stage {hero.retry_stage} in {RETRY_AFTER_WINS - hero.farm_wins} wins."


def retry_now(hero: Hero) -> str:
    """Stop farming and go straight back to the stage that was lost (e.g. after buying upgrades)."""
    if hero.retry_stage is not None:
        hero.stage, hero.retry_stage, hero.farm_wins = hero.retry_stage, None, 0
    return f"Retrying stage {hero.stage}!"
