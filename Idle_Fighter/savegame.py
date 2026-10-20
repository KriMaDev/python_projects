"""Save the hero to a JSON file and work out what was earned while the game was closed."""
from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, fields
from pathlib import Path

from characters import CLASSES
from enemies import NORMAL, rewards
from hero import Hero
from tactics import Tactics

SAVE_VERSION = 1
DEFAULT_SAVE = Path(__file__).resolve().parent / "savegame.json"

OFFLINE_CAP_SECONDS = 8 * 60 * 60  # earn for at most 8 hours away
SECONDS_PER_KILL    = 30           # offline the hero beats one normal enemy every 30 seconds...
OFFLINE_EFFICIENCY  = 0.5          # ...for half the usual reward


def save_game(hero: Hero, path: Path = DEFAULT_SAVE) -> None:
    """Write the hero to disk. Writes to a temporary file first so a crash can't corrupt the save."""
    hero.last_seen = time.time()
    data = {"version": SAVE_VERSION, "hero": asdict(hero)}
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    os.replace(temp, path)


def load_game(path: Path = DEFAULT_SAVE) -> Hero | None:
    """Load the hero from disk, or None if there is no save. Raises ValueError for a damaged save file."""
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("version") != SAVE_VERSION:
            raise ValueError(f"unsupported save version {data.get('version')}")
        known = {f.name for f in fields(Hero)}
        hero = Hero(**{key: value for key, value in data["hero"].items() if key in known})
        hero.tactics = Tactics(**hero.tactics) if isinstance(hero.tactics, dict) else Tactics()
        if hero.spec not in CLASSES:
            raise ValueError(f"unknown class {hero.spec!r}")
        return hero
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as e:
        raise ValueError(f"{path} is damaged ({e})") from e


def offline_rewards(hero: Hero, now: float | None = None) -> tuple[int, int, float]:
    """Gold, XP and seconds earned while away: half rewards for normal enemies of the best cleared stage."""
    away = (time.time() if now is None else now) - hero.last_seen
    seconds = min(max(away, 0.0), OFFLINE_CAP_SECONDS)
    kills = int(seconds // SECONDS_PER_KILL)
    if kills == 0 or hero.best_stage == 0:
        return 0, 0, seconds
    gold, xp = rewards(hero.best_stage, NORMAL)
    return round(kills * gold * OFFLINE_EFFICIENCY), round(kills * xp * OFFLINE_EFFICIENCY), seconds
