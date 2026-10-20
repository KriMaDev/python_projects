"""The player's decisions: standing orders the hero follows every turn, or manual control in boss fights."""
from __future__ import annotations

from dataclasses import dataclass

from characters import Fighter
from combat import ATTACK, DEFEND, SKILL, ActionChooser
from enemies import BOSS, MINI_BOSS

SKILL_ALWAYS, SKILL_BOSSES, SKILL_NEVER = "always", "bosses only", "never"
SKILL_POLICIES = (SKILL_ALWAYS, SKILL_BOSSES, SKILL_NEVER)
DEFEND_THRESHOLDS = (0.0, 0.25, 0.5)  # share of max health; 0 = never defend


@dataclass
class Tactics:
    skill_policy: str = SKILL_ALWAYS
    defend_below: float = 0.0      # defend when health drops below this share of max health
    manual_bosses: bool = False    # choose every action yourself in (mini) boss fights
    autobuy: bool = False          # buy the cheapest upgrades after every fight


def is_boss_fight(kind: str) -> bool:
    return kind in (BOSS, MINI_BOSS)


def auto_chooser(tactics: Tactics, kind: str) -> ActionChooser:
    """Build the per-turn decision rule for a fight against an enemy of this kind."""
    use_skill = tactics.skill_policy == SKILL_ALWAYS or (tactics.skill_policy == SKILL_BOSSES and is_boss_fight(kind))

    def choose(hero: Fighter, enemy: Fighter) -> str:
        if use_skill and hero.can_use_ability() and hero.ability.useful(hero, enemy):
            return SKILL
        # Never defend twice in a row, or a hurt hero would stall until the turn limit
        if not hero.defending and hero.health < tactics.defend_below * hero.stats.health:
            return DEFEND
        return ATTACK

    return choose


def manual_action(hero: Fighter, enemy: Fighter) -> str:
    """Ask the player for this turn's action."""
    ability = hero.ability
    while True:
        answer = input(f"  [A]ttack  [S] {ability.name} ({ability.cost:.0f} mana, you have {hero.mana:.0f})  "
                       f"[D]efend: ").strip().lower()
        if answer in ("", "a"):
            return ATTACK
        if answer == "d":
            return DEFEND
        if answer == "s":
            if hero.can_use_ability():
                return SKILL
            print("  Not enough mana!")
