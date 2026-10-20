import json
import random

import pytest

import main
from enemies import BOSS, ENEMY_GROWTH, MINI_BOSS, NORMAL, enemy_type, make_enemy, rewards, stage_kind
from game import RETRY_AFTER_WINS, StageResult, advance, play_stage, retry_now
from hero import Hero
from savegame import OFFLINE_CAP_SECONDS, SECONDS_PER_KILL, load_game, offline_rewards, save_game
from shop import UPGRADES, autobuy, buy, cost
from tactics import Tactics, auto_chooser

# ---------------------------------------------------------------- enemies


@pytest.mark.parametrize(("stage", "kind"), [
    (1, NORMAL), (4, NORMAL), (5, MINI_BOSS), (10, BOSS), (15, MINI_BOSS), (20, BOSS), (25, MINI_BOSS), (31, NORMAL),
])
def test_every_5th_stage_is_a_mini_boss_and_every_10th_a_boss(stage, kind):
    assert stage_kind(stage) == kind


@pytest.mark.parametrize(("stage", "name"), [
    (5, "Stone Golem"), (15, "Swamp Witch"), (25, "Stone Golem"),
    (10, "Orange Cat"), (20, "Ember Dragon"), (30, "Old Lich"), (40, "Orange Cat"),
])
def test_bosses_come_in_a_fixed_order(stage, name):
    assert enemy_type(stage, random.Random(0)).name == name


def test_enemies_get_stronger_every_stage():
    cat_10, cat_40 = make_enemy(10, random.Random(0)), make_enemy(40, random.Random(0))
    assert cat_40.stats.health == pytest.approx(cat_10.stats.health * ENEMY_GROWTH ** 30)
    assert cat_40.stats.damage > cat_10.stats.damage


def test_bosses_give_bigger_rewards():
    assert rewards(10)[0] > rewards(9)[0] * 5
    assert rewards(10, NORMAL)[0] < rewards(10)[0]

# ---------------------------------------------------------------- hero and shop


def test_gain_levels_up_and_keeps_leftover_xp():
    hero = Hero("Tank")
    needed = hero.xp_needed()
    levels = hero.gain(gold=10, xp=needed + 3)
    assert (levels, hero.level, hero.xp, hero.gold) == (1, 2, 3, 10)


def test_gain_can_level_up_several_times():
    assert Hero("Tank").gain(0, 10_000) > 1


def test_levels_and_upgrades_improve_stats():
    base = Hero("Mage").stats()
    hero = Hero("Mage", level=5, upgrades={"damage": 2, "crit": 3})
    stats = hero.stats()
    assert stats.damage > base.damage * 1.2
    assert stats.crit_chance == pytest.approx(base.crit_chance + 0.06)
    assert stats.health > base.health


def test_upgrades_get_more_expensive():
    assert cost("damage", 0) < cost("damage", 1) < cost("damage", 5)


def test_maxed_upgrade_has_no_price():
    assert cost("crit", UPGRADES["crit"].max_level) is None


def test_buy_needs_enough_gold():
    hero = Hero("Melee", gold=cost("damage", 0) - 1)
    assert not buy(hero, "damage")
    hero.gold += 1
    assert buy(hero, "damage")
    assert (hero.gold, hero.upgrades) == (0, {"damage": 1})


def test_autobuy_buys_cheapest_until_broke():
    hero = Hero("Melee", gold=100)
    bought = autobuy(hero)
    assert bought and hero.gold < min(cost(key, hero.upgrades.get(key, 0)) for key in UPGRADES)

# ---------------------------------------------------------------- progression


def won(stage):
    return StageResult(stage, stage_kind(stage), "Goblin", won=True, turns=3)


def lost(stage):
    return StageResult(stage, stage_kind(stage), "Orange Cat", won=False, turns=9)


def test_winning_moves_to_the_next_stage():
    hero = Hero("Melee", stage=3)
    advance(hero, won(3))
    assert (hero.stage, hero.best_stage) == (4, 3)


def test_losing_falls_back_and_retries_after_farming():
    hero = Hero("Melee", stage=10, best_stage=9)
    advance(hero, lost(10))
    assert (hero.stage, hero.retry_stage) == (9, 10)

    for _ in range(RETRY_AFTER_WINS - 1):
        advance(hero, won(9))
        assert hero.stage == 9  # farming, not advancing
    advance(hero, won(9))
    assert (hero.stage, hero.retry_stage) == (10, None)


def test_retry_now_skips_the_rest_of_farming():
    hero = Hero("Melee", stage=10)
    advance(hero, lost(10))
    retry_now(hero)
    assert (hero.stage, hero.retry_stage, hero.farm_wins) == (10, None, 0)


def test_stage_one_defeat_stays_on_stage_one():
    hero = Hero("Melee")
    advance(hero, lost(1))
    assert hero.stage == 1


def test_play_stage_gives_rewards_for_a_win():
    hero = Hero("Mage")
    result = play_stage(hero, random.Random(1), lambda kind: auto_chooser(Tactics(), kind))
    assert result.won
    assert (hero.gold, result.gold) == (rewards(1)[0], rewards(1)[0])
    assert hero.stage == 1  # play_stage doesn't move the hero, advance() does

# ---------------------------------------------------------------- saving


def test_save_and_load_round_trip(tmp_path):
    path = tmp_path / "save.json"
    hero = Hero("Debuffer", level=7, gold=123, stage=12, best_stage=11, upgrades={"damage": 3},
                carried_mana=12.5, tactics=Tactics(skill_policy="bosses only", defend_below=0.25, autobuy=True))
    save_game(hero, path)
    loaded = load_game(path)
    assert loaded == hero


def test_load_without_a_save_returns_none(tmp_path):
    assert load_game(tmp_path / "missing.json") is None


@pytest.mark.parametrize("content", ["not json", json.dumps({"version": 99, "hero": {}}),
                                     json.dumps({"version": 1, "hero": {"spec": "Wizard"}})])
def test_damaged_save_raises_a_clear_error(tmp_path, content):
    path = tmp_path / "save.json"
    path.write_text(content)
    with pytest.raises(ValueError):
        load_game(path)


def test_offline_rewards_are_capped():
    hero = Hero("Tank", best_stage=10, last_seen=0)
    gold_8h, _, seconds = offline_rewards(hero, now=OFFLINE_CAP_SECONDS)
    gold_2d, _, _ = offline_rewards(hero, now=OFFLINE_CAP_SECONDS * 6)
    assert seconds == OFFLINE_CAP_SECONDS and gold_2d == gold_8h > 0


def test_offline_rewards_farm_normal_enemies_not_the_boss():
    hero = Hero("Tank", best_stage=10, last_seen=0)
    gold, _, _ = offline_rewards(hero, now=SECONDS_PER_KILL)
    assert gold == round(rewards(10, NORMAL)[0] * 0.5)


def test_no_offline_rewards_for_a_short_break_or_a_new_hero():
    assert offline_rewards(Hero("Tank", best_stage=5, last_seen=0), now=SECONDS_PER_KILL - 1)[0] == 0
    assert offline_rewards(Hero("Tank", last_seen=0), now=OFFLINE_CAP_SECONDS)[0] == 0

# ---------------------------------------------------------------- input


def test_choose_class_asks_again_after_invalid_input(monkeypatch, capsys):
    answers = iter(["Wizard", "ranged"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    assert main.choose_class() == "Ranged"
    assert "Please choose from predefined classes!" in capsys.readouterr().out
