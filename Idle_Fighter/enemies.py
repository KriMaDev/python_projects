"""Enemy roster. Every 5th stage is a mini boss, every 10th a boss, and enemies get stronger each stage."""
from __future__ import annotations

import random
from dataclasses import dataclass

from abilities import Ability, Backstab, Fireball, Heal, ShieldWall, Weaken
from characters import Fighter, Stats

NORMAL, MINI_BOSS, BOSS = "normal", "mini boss", "boss"

ENEMY_GROWTH  = 1.11   # enemy damage, health and shield per stage
REWARD_GROWTH = 1.15   # gold and XP per stage
REWARD_MULTIPLIER = {NORMAL: 1, MINI_BOSS: 4, BOSS: 10}


@dataclass(frozen=True)
class EnemyType:
    name: str
    stats: Stats  # at stage 1
    ability: Ability | None = None


#                              damage crit  x    health mana shield h_reg m_reg s_reg
NORMAL_ENEMIES = [
    EnemyType("Goblin",      Stats(5,   0.10, 2,   45,   0,   0,    0,    0,    0)),
    EnemyType("Slime",       Stats(3,   0.05, 2,   80,   0,   0,    1,    0,    0)),
    EnemyType("Skeleton",    Stats(4,   0.10, 2,   35,   0,   30,   0,    0,    0)),
    EnemyType("Wolf",        Stats(6,   0.25, 2,   35,   0,   0,    0,    0,    0)),
]
MINI_BOSSES = [
    EnemyType("Stone Golem", Stats(5,   0.10, 2,   90,   30,  90,   0,    1,    0),   ShieldWall()),
    EnemyType("Swamp Witch", Stats(7,   0.20, 2.5, 100,  50,  20,   0,    2,    0),   Heal()),
]
BOSSES = [
    EnemyType("Orange Cat",  Stats(7,   0.20, 2,   160,  60,  90,   0.5,  2,    0.5), Backstab()),
    EnemyType("Ember Dragon", Stats(7,  0.15, 2,   190,  60,  60,   0,    1,    0),   Fireball()),
    EnemyType("Old Lich",    Stats(6,   0.20, 2,   170,  80,  80,   1,    2,    1),   Weaken()),
]


def stage_kind(stage: int) -> str:
    """Every 10th stage is a boss, every other 5th stage a mini boss."""
    if stage % 10 == 0:
        return BOSS
    if stage % 5 == 0:
        return MINI_BOSS
    return NORMAL


def enemy_type(stage: int, rng: random.Random) -> EnemyType:
    """Normal enemies are random. Mini bosses and bosses take turns in a fixed order."""
    kind = stage_kind(stage)
    if kind == BOSS:
        return BOSSES[(stage // 10 - 1) % len(BOSSES)]
    if kind == MINI_BOSS:
        return MINI_BOSSES[(stage // 10) % len(MINI_BOSSES)]
    return rng.choice(NORMAL_ENEMIES)


def make_enemy(stage: int, rng: random.Random) -> Fighter:
    """Create the enemy for a stage, scaled up from its stage 1 stats."""
    template = enemy_type(stage, rng)
    scale = ENEMY_GROWTH ** (stage - 1)
    return Fighter(template.name, template.stats.scaled(damage=scale, defence=scale, regen=scale), template.ability)


def rewards(stage: int, kind: str | None = None) -> tuple[int, int]:
    """Gold and XP for beating an enemy on a stage (by default the stage's own enemy kind)."""
    multiplier = REWARD_MULTIPLIER[kind or stage_kind(stage)] * REWARD_GROWTH ** (stage - 1)
    return round(8 * multiplier), round(5 * multiplier)
