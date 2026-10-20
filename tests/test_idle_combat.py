import random

import pytest

from abilities import AimedShot, Backstab, Cleave, Fireball, Heal, ShieldWall, Weaken
from characters import CLASSES, Fighter, Stats, find_class
from combat import ATTACK, DEFEND, MAX_TURNS, SKILL, enemy_action, fight, take_turn


class FixedRng(random.Random):
    """random() always returns the same value: 0.0 crits every time, 0.99 never crits."""

    def __init__(self, value: float) -> None:
        super().__init__()
        self.value = value

    def random(self) -> float:
        return self.value


ALWAYS_CRIT, NEVER_CRIT = FixedRng(0.0), FixedRng(0.99)


def make(damage=10, health=100, shield=0, mana=50, crit_chance=0.2, crit_multiplier=3, regen=0.0, ability=None):
    stats = Stats(damage, crit_chance, crit_multiplier, health, mana, shield, regen, regen, regen)
    return Fighter("Test", stats, ability)


def test_find_class_is_case_insensitive():
    assert find_class(" mage ") == "Mage"
    with pytest.raises(ValueError, match="Unknown class"):
        find_class("Wizard")


@pytest.mark.parametrize("spec", list(CLASSES))
def test_every_class_has_an_affordable_ability(spec):
    hero_class = CLASSES[spec]
    assert hero_class.stats.mana >= hero_class.ability.cost


def test_shield_absorbs_damage_before_health():
    target = make(health=100, shield=30)
    target.take_damage(50)
    assert (target.shield, target.health) == (0, 80)


def test_ignore_shield_goes_straight_to_health():
    target = make(health=100, shield=30)
    target.take_damage(50, ignore_shield=True)
    assert (target.shield, target.health) == (30, 50)


def test_defending_halves_damage():
    target = make(health=100)
    target.defending = True
    assert target.take_damage(40) == 20
    assert target.health == 80


def test_health_never_goes_below_zero():
    target = make(health=10)
    target.take_damage(500)
    assert target.health == 0 and not target.alive


def test_critical_hits_multiply_damage():
    attacker, target = make(damage=10, crit_multiplier=3), make(health=100)
    assert attacker.attack(target, ALWAYS_CRIT) == (30, True)
    assert attacker.attack(target, NEVER_CRIT) == (10, False)


def test_regeneration_is_capped_at_maximum():
    fighter = make(health=100, shield=20, mana=50, regen=5)
    fighter.health, fighter.shield, fighter.mana = 98, 0, 49
    fighter.regenerate()
    assert (fighter.health, fighter.shield, fighter.mana) == (100, 5, 50)


def test_cleave_hits_for_double_damage():
    user, target = make(damage=10), make(health=100)
    Cleave().use(user, target, NEVER_CRIT)
    assert target.health == 80


def test_aimed_shot_adds_crit_chance():
    user, target = make(damage=10, crit_chance=0.25, crit_multiplier=2), make(health=100)
    AimedShot().use(user, target, FixedRng(0.6))  # 0.6 < 0.25 + 0.5, so it crits
    assert target.health == 100 - 10 * 1.5 * 2


def test_backstab_always_crits():
    user, target = make(damage=10, crit_chance=0, crit_multiplier=4), make(health=100)
    Backstab().use(user, target, NEVER_CRIT)
    assert target.health == 60


def test_fireball_ignores_shield():
    user, target = make(damage=10), make(health=100, shield=100)
    Fireball().use(user, target, NEVER_CRIT)
    assert (target.shield, target.health) == (100, 85)


def test_heal_restores_health_and_is_only_useful_when_hurt():
    user = make(health=100)
    assert not Heal().useful(user, user)
    user.health = 20
    assert Heal().useful(user, user)
    Heal().use(user, user, NEVER_CRIT)
    assert user.health == 55


def test_shield_wall_restores_half_the_shield():
    user = make(shield=100)
    user.shield = 10
    ShieldWall().use(user, user, NEVER_CRIT)
    assert user.shield == 60


def test_weaken_stacks_down_to_half_damage():
    user, target = make(), make(health=1000)
    for _ in range(5):
        Weaken().use(user, target, NEVER_CRIT)
    assert target.damage_multiplier == Weaken.MIN_MULTIPLIER
    assert not Weaken().useful(user, target)


def test_skill_costs_mana_and_falls_back_to_attack_without_it():
    user, target = make(damage=10, mana=20, ability=Cleave()), make(health=100)
    assert take_turn(user, target, SKILL, NEVER_CRIT) == "Cleave 20"
    assert user.mana == 0
    assert take_turn(user, target, SKILL, NEVER_CRIT) == "Hit 10"


def test_defend_restores_mana_until_next_turn():
    user, target = make(mana=50), make()
    user.mana = 0
    take_turn(user, target, DEFEND, NEVER_CRIT)
    assert user.defending and user.mana == 10
    take_turn(user, target, ATTACK, NEVER_CRIT)
    assert not user.defending


def test_enemy_uses_ability_only_when_useful():
    enemy = make(ability=Heal())
    assert enemy_action(enemy, make()) == ATTACK
    enemy.health = 10
    assert enemy_action(enemy, make()) == SKILL


def test_fight_hero_wins_and_reports_every_turn():
    hero, enemy = make(damage=30, health=100), make(damage=5, health=60)
    turns = []
    result = fight(hero, enemy, NEVER_CRIT, lambda h, e: ATTACK, on_turn=lambda t, h, e, events: turns.append(events))
    assert result.won and result.turns == 2
    assert turns[0] == ["Hit 30", "Test: Hit 5"]
    assert turns[1] == ["Hit 30"]  # the enemy is down and doesn't hit back


def test_fight_enemy_wins():
    result = fight(make(damage=1, health=10), make(damage=50), NEVER_CRIT, lambda h, e: ATTACK)
    assert not result.won


def test_fight_that_takes_too_long_is_lost():
    result = fight(make(damage=0), make(damage=0), NEVER_CRIT, lambda h, e: ATTACK)
    assert not result.won and result.turns == MAX_TURNS


def test_fight_is_reproducible_with_a_seed():
    def run():
        hero = Fighter("Mage", CLASSES["Mage"].stats, CLASSES["Mage"].ability)
        enemy = Fighter("Golem", Stats(8, 0.1, 2, 200, 0, 100, 0, 0, 0))
        return fight(hero, enemy, random.Random(42), lambda h, e: SKILL if h.can_use_ability() else ATTACK)
    assert run() == run()
