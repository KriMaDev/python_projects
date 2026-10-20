"""Terminal output: HP bars, one compact line per turn and coloured results."""
from __future__ import annotations

import random
import sys

from colorama import Fore, Style, just_fix_windows_console

from characters import Fighter
from enemies import BOSS, MINI_BOSS, enemy_type, stage_kind
from game import StageResult
from hero import Hero

FULL, EMPTY = "█", "░"
RESET = Style.RESET_ALL
KIND_STYLE = {BOSS: (Fore.LIGHTMAGENTA_EX, "BOSS"), MINI_BOSS: (Fore.LIGHTYELLOW_EX, "MINI BOSS")}


def setup_terminal() -> None:
    """Enable colours on Windows and make sure the bar characters can be printed (also when piped)."""
    global FULL, EMPTY
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        FULL, EMPTY = "#", "-"
    just_fix_windows_console()


def bar(current: float, maximum: float, width: int = 10) -> str:
    """A bar like █████░░░ showing current out of maximum."""
    filled = 0 if maximum <= 0 else round(width * min(max(current, 0), maximum) / maximum)
    return FULL * filled + EMPTY * (width - filled)


def status(fighter: Fighter, color: str) -> str:
    """Health bar with numbers, plus shield and mana if the fighter has them."""
    text = f"{color}{bar(fighter.health, fighter.stats.health)}{RESET} {fighter.health:>4.0f}/{fighter.stats.health:<4.0f}"
    if fighter.stats.shield:
        text += f" {Fore.CYAN}{fighter.shield:>3.0f}sh{RESET}"
    if fighter.ability:
        text += f" {Fore.BLUE}{fighter.mana:>3.0f}mp{RESET}"
    return text


def highlight(event: str) -> str:
    return f"{Fore.LIGHTYELLOW_EX}{event}{RESET}" if "CRIT" in event else event


def turn_line(turn: int, hero: Fighter, enemy: Fighter, events: list[str]) -> str:
    """One line per turn: your bars | what happened | the enemy's bars."""
    happened = " · ".join(highlight(event) for event in events)
    # pad on the visible text length, colour codes don't take up space
    padding = " " * max(0, 44 - len(" · ".join(events)))
    return f" T{turn:<3}{status(hero, Fore.GREEN)} │ {happened}{padding} │ {status(enemy, Fore.RED)}"


def stage_banner(stage: int, kind: str, hero: Fighter, enemy: Fighter) -> str:
    color, label = KIND_STYLE.get(kind, (Fore.WHITE, "Stage"))
    title = f" Stage {stage} · {label} · {enemy.name} " if kind in KIND_STYLE else f" Stage {stage} · {enemy.name} "
    return f"\n{color}{title:─^60}{RESET}"


def result_line(result: StageResult) -> str:
    if not result.won:
        return f"{Fore.RED}DEFEATED{RESET} by {result.enemy} after {result.turns} turns."
    turns = f"{result.turns} turn{'s' if result.turns != 1 else ''}"
    text = f"{Fore.GREEN}VICTORY{RESET} in {turns}  {Fore.YELLOW}+{result.gold} gold{RESET}  +{result.xp} XP"
    if result.levels_gained:
        text += f"  {Fore.LIGHTGREEN_EX}LEVEL UP!{RESET}" + (f" x{result.levels_gained}" if result.levels_gained > 1 else "")
    return text


def duration(seconds: float) -> str:
    """Readable duration: '45 seconds', '1 minute', '2h 13m'."""
    minutes = int(seconds // 60)
    if minutes == 0:
        return f"{int(seconds)} seconds"
    if minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    return f"{minutes // 60}h {minutes % 60:02d}m"


def next_boss(stage: int) -> str:
    """Describe the next mini boss or boss, e.g. 'MINI BOSS Stone Golem on stage 5 (2 to go)'."""
    ahead = next(n for n in range(5) if stage_kind(stage + n) in KIND_STYLE)
    color, label = KIND_STYLE[stage_kind(stage + ahead)]
    name = enemy_type(stage + ahead, random.Random()).name  # (mini) bosses don't depend on the RNG
    when = "this stage!" if ahead == 0 else f"on stage {stage + ahead} ({ahead} to go)"
    return f"{color}{label} {name}{RESET} {when}"


def header(hero: Hero) -> str:
    """Top line of the main menu."""
    kind = KIND_STYLE.get(stage_kind(hero.stage), (Fore.WHITE, ""))[1]
    farming = f"  {Fore.YELLOW}farming, retry stage {hero.retry_stage} soon{RESET}" if hero.retry_stage else ""
    return (f"\n{Style.BRIGHT}Stage {hero.stage}{RESET}{' (' + kind + ')' if kind else ''}"
            f"  ·  Lv {hero.level} {hero.name}  ·  {Fore.YELLOW}{hero.gold} gold{RESET}"
            f"  ·  XP {Fore.LIGHTBLUE_EX}{bar(hero.xp, hero.xp_needed(), 10)}{RESET} {hero.xp}/{hero.xp_needed()}"
            f"\nNext: {next_boss(hero.stage)}{farming}")
