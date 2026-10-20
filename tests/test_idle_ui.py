import re

import pytest

import ui
from characters import CLASSES, Fighter
from game import StageResult
from hero import Hero


def plain(text: str) -> str:
    """Remove colour codes."""
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


@pytest.mark.parametrize(("current", "maximum", "filled"), [
    (0, 100, 0), (100, 100, 10), (50, 100, 5), (150, 100, 10), (-5, 100, 0), (10, 0, 0),
])
def test_bar(current, maximum, filled):
    assert ui.bar(current, maximum) == ui.FULL * filled + ui.EMPTY * (10 - filled)


@pytest.mark.parametrize(("stage", "expected"), [
    (1, "MINI BOSS Stone Golem on stage 5 (4 to go)"),
    (5, "MINI BOSS Stone Golem this stage!"),
    (6, "BOSS Orange Cat on stage 10 (4 to go)"),
    (16, "BOSS Ember Dragon on stage 20 (4 to go)"),
])
def test_next_boss(stage, expected):
    assert plain(ui.next_boss(stage)) == expected


def test_result_line():
    assert "in 1 turn " in plain(ui.result_line(StageResult(1, "normal", "Wolf", won=True, turns=1, gold=8, xp=5)))
    win = plain(ui.result_line(StageResult(10, "boss", "Orange Cat", won=True, turns=12, gold=281, xp=176, levels_gained=3)))
    assert "VICTORY in 12 turns" in win and "+281 gold" in win and "LEVEL UP! x3" in win
    assert plain(ui.result_line(StageResult(10, "boss", "Orange Cat", won=False, turns=9))).startswith("DEFEATED by Orange Cat")


def test_turn_line_shows_both_fighters_and_events():
    hero = Fighter("Perry Hotter", CLASSES["Mage"].stats, CLASSES["Mage"].ability)
    enemy = Fighter("Goblin", CLASSES["Melee"].stats)
    line = plain(ui.turn_line(3, hero, enemy, ["Fireball 37 CRIT!", "Goblin: Hit 5"]))
    assert line.startswith(" T3 ")
    assert "Fireball 37 CRIT! · Goblin: Hit 5" in line
    assert "40/40" in line and "mp" in line   # hero health and mana
    assert "110/110" in line                  # enemy health


def test_header_mentions_farming():
    hero = Hero("Tank", stage=9, retry_stage=10, gold=55)
    text = plain(ui.header(hero))
    assert "Stage 9" in text and "55 gold" in text and "retry stage 10" in text


@pytest.mark.parametrize(("seconds", "text"), [(45, "45 seconds"), (60, "1 minute"), (150, "2 minutes"), (7980, "2h 13m")])
def test_duration(seconds, text):
    assert ui.duration(seconds) == text
