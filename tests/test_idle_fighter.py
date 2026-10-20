import pytest

from classes import Character
from functions import PRESETS, choose_character, create_character, fight


@pytest.mark.parametrize("spec", list(PRESETS))
def test_create_character_uses_preset_stats(spec):
    player = create_character(spec)
    assert isinstance(player, Character)
    assert player.spec == spec
    for stat, value in PRESETS[spec].items():
        assert getattr(player, stat) == value


def test_create_character_is_case_insensitive():
    assert create_character("  mage ").name == "Perry Hotter"


def test_create_character_rejects_unknown_class():
    with pytest.raises(ValueError, match="Unknown class"):
        create_character("Wizard")


def test_presets_are_new_objects():
    first = create_character("Tank")
    first.health = 0
    assert create_character("Tank").health == 150


def test_choose_character_asks_again_after_invalid_input(monkeypatch, capsys):
    answers = iter(["Wizard", "Ranged"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    assert choose_character().name == "Robin Hoodie"
    assert "Please choose from predefined classes!" in capsys.readouterr().out


def make_boss() -> Character:
    return Character("Orange Cat", "Boss", 3, 2, 0.2, 150, 100, 150, 0.2, 0.2, 0.2)


def test_fight_player_wins():
    player = create_character("Mage")
    enemy = make_boss()
    assert fight(player, enemy) == "player"
    assert enemy.health <= 0 < player.health


def test_fight_enemy_wins():
    weakling = Character("Weakling", "Test", 1, 1, 0, 3, 0, 0, 0, 0, 0)
    assert fight(weakling, make_boss()) == "enemy"


def test_fight_draw_after_turn_limit():
    pacifist = Character("Pacifist", "Test", 0, 1, 0, 1000, 0, 0, 0, 0, 0)
    assert fight(pacifist, make_boss()) == "draw"
