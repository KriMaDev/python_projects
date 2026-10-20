import pytest

import main
from abilities import Cleave, Heal
from characters import Fighter, Stats
from combat import ATTACK, DEFEND, SKILL
from enemies import BOSS, MINI_BOSS, NORMAL
from hero import MANA_AFTER_WIN, Hero
from tactics import SKILL_ALWAYS, SKILL_BOSSES, SKILL_NEVER, Tactics, auto_chooser, manual_action


def make(health=100, mana=50, ability=None):
    return Fighter("Test", Stats(10, 0.2, 2, health, mana, 0, 0, 0, 0), ability)


@pytest.mark.parametrize(("policy", "kind", "expected"), [
    (SKILL_ALWAYS, NORMAL, SKILL),
    (SKILL_BOSSES, NORMAL, ATTACK),   # saves mana for the boss
    (SKILL_BOSSES, MINI_BOSS, SKILL),
    (SKILL_BOSSES, BOSS, SKILL),
    (SKILL_NEVER, BOSS, ATTACK),
])
def test_skill_policy(policy, kind, expected):
    choose = auto_chooser(Tactics(skill_policy=policy), kind)
    assert choose(make(ability=Cleave()), make()) == expected


def test_skill_is_skipped_when_not_useful():
    choose = auto_chooser(Tactics(), NORMAL)
    assert choose(make(ability=Heal()), make()) == ATTACK  # full health, no need to heal


def test_skill_is_skipped_without_mana():
    hero = make(ability=Cleave())
    hero.mana = 0
    assert auto_chooser(Tactics(), NORMAL)(hero, make()) == ATTACK


def test_defend_when_health_is_low_but_never_twice_in_a_row():
    choose = auto_chooser(Tactics(skill_policy=SKILL_NEVER, defend_below=0.5), NORMAL)
    hero = make(health=100)
    assert choose(hero, make()) == ATTACK
    hero.health = 40
    assert choose(hero, make()) == DEFEND
    hero.defending = True  # defended last turn
    assert choose(hero, make()) == ATTACK


def test_manual_action_reads_the_players_choice(monkeypatch, capsys):
    hero = make(ability=Cleave())
    hero.mana = 0
    answers = iter(["s", "x", "d"])  # skill without mana, nonsense, defend
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    assert manual_action(hero, make()) == DEFEND
    assert "Not enough mana" in capsys.readouterr().out


def test_manual_control_only_in_boss_fights_and_only_when_interactive():
    tactics = Tactics(manual_bosses=True)
    assert main.chooser_factory(tactics, interactive=True)(BOSS) is manual_action
    assert main.chooser_factory(tactics, interactive=True)(NORMAL) is not manual_action
    assert main.chooser_factory(tactics, interactive=False)(BOSS) is not manual_action


def test_mana_carries_over_after_a_win_and_refills_after_a_defeat():
    hero = Hero("Mage")
    fighter = hero.make_fighter()
    fighter.mana = 20
    hero.after_fight(fighter, won=True)
    assert hero.carried_mana == pytest.approx(20 + fighter.stats.mana * MANA_AFTER_WIN)
    assert hero.make_fighter().mana == pytest.approx(hero.carried_mana)

    hero.after_fight(fighter, won=False)
    assert hero.make_fighter().mana == fighter.stats.mana


def test_next_option_cycles():
    assert main.next_option(("a", "b", "c"), "c") == "a"
    assert main.next_option(("a", "b"), "unknown") == "a"
