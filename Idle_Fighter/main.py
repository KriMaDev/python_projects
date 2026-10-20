"""Idle Fighter: an idle auto battler. Your hero fights stage after stage on their own,
earning gold and XP. Every 5th stage is a mini boss and every 10th a boss."""
import argparse
import random
import time
from pathlib import Path

from characters import CLASSES, Fighter, find_class
from combat import ATTACK, SKILL
from enemies import BOSS, MINI_BOSS
from game import StageResult, advance, play_stage, retry_now
from hero import Hero
from savegame import DEFAULT_SAVE, load_game, offline_rewards, save_game
from shop import UPGRADES, autobuy, buy, cost

# ===================================================================
#                                                              OUTPUT
# ===================================================================

def print_start(stage: int, kind: str, hero: Fighter, enemy: Fighter) -> None:
    label = {BOSS: "BOSS", MINI_BOSS: "MINI BOSS"}.get(kind, "Enemy")
    print(f"\n--- Stage {stage}: {label} {enemy.name} ({enemy.health:.0f} HP, {enemy.shield:.0f} shield) ---")


def print_turn(turn: int, hero: Fighter, enemy: Fighter, events: list[str]) -> None:
    print(f"T{turn:<3} {' | '.join(events):<45} You {hero.health:.0f} HP  {enemy.name} {enemy.health:.0f} HP")


def print_result(result: StageResult) -> None:
    if result.won:
        text = f"Won in {result.turns} turns: +{result.gold} gold, +{result.xp} XP"
        if result.levels_gained:
            text += f", LEVEL UP x{result.levels_gained}!"
        print(text)
    else:
        print(f"Defeated by {result.enemy} after {result.turns} turns.")

# ===================================================================
#                                                            GAMEPLAY
# ===================================================================

def auto_action(hero: Fighter, enemy: Fighter) -> str:
    """Use the ability whenever it is affordable and useful, otherwise attack."""
    if hero.can_use_ability() and hero.ability.useful(hero, enemy):
        return SKILL
    return ATTACK


def run_fights(hero: Hero, rng: random.Random, save_path: Path, count: int | None = None,
               speed: float = 0.25, buy_upgrades: bool = False) -> None:
    """Fight stage after stage until `count` fights are done (forever if None) or Ctrl+C is pressed."""
    def on_turn(turn: int, fighter: Fighter, enemy: Fighter, events: list[str]) -> None:
        print_turn(turn, fighter, enemy, events)
        time.sleep(speed)

    fights = 0
    try:
        while count is None or fights < count:
            result = play_stage(hero, rng, auto_action, on_start=print_start, on_turn=on_turn)
            print_result(result)
            print(advance(hero, result))
            if buy_upgrades and (bought := autobuy(hero)):
                print(f"Bought: {', '.join(bought)}")
            save_game(hero, save_path)  # autosave after every fight
            fights += 1
    except KeyboardInterrupt:
        print("\nPaused.")
    save_game(hero, save_path)


def choose_class() -> str:
    """Ask for a class until a valid one is entered."""
    while True:
        try:
            return find_class(input(f"Choose a class:\n{list(CLASSES)}\n: "))
        except ValueError:
            print("Please choose from predefined classes!")

# ===================================================================
#                                                               MENUS
# ===================================================================

def shop_menu(hero: Hero) -> None:
    """Show the upgrades and buy what the player picks."""
    keys = list(UPGRADES)
    while True:
        print(f"\nShop - you have {hero.gold} gold")
        for number, key in enumerate(keys, start=1):
            level = hero.upgrades.get(key, 0)
            price = cost(key, level)
            print(f" {number}. {UPGRADES[key].name:<11} Lv {level:<3} {UPGRADES[key].description:<26} "
                  f"{'MAX' if price is None else f'{price} gold'}")
        choice = input("Number to buy, [A]uto-buy cheapest, Enter to go back\n: ").strip().lower()
        if not choice:
            return
        if choice == "a":
            bought = autobuy(hero)
            print(f"Bought: {', '.join(bought)}" if bought else "You can't afford anything yet.")
        elif choice.isdigit() and 1 <= int(choice) <= len(keys):
            key = keys[int(choice) - 1]
            print(f"Bought {UPGRADES[key].name}!" if buy(hero, key) else "Not enough gold (or maxed out).")
        else:
            print("Unknown choice.")


def print_hero(hero: Hero) -> None:
    stats, ability = hero.stats(), CLASSES[hero.spec].ability
    print(f"\n{hero.name} - level {hero.level} {hero.spec}  (best stage cleared: {hero.best_stage})\n"
          f"Damage {stats.damage:.1f}   Crit {stats.crit_chance:.0%} x{stats.crit_multiplier}\n"
          f"Health {stats.health:.0f}   Shield {stats.shield:.0f}   Mana {stats.mana:.0f}\n"
          f"Regen per turn: {stats.health_regen:.1f} HP, {stats.shield_regen:.1f} shield, {stats.mana_regen:.1f} mana\n"
          f"Ability: {ability.name} ({ability.cost} mana) - {ability.description}")


def main_menu(hero: Hero, rng: random.Random, save_path: Path, speed: float) -> None:
    while True:
        print(f"\n=== Stage {hero.stage} | Lv {hero.level} {hero.name} | {hero.gold} gold | "
              f"XP {hero.xp}/{hero.xp_needed()} ===")
        choice = input("[F]ight  [S]hop  [H]ero  [Q]uit\n: ").strip().lower()
        if choice == "f":
            if hero.retry_stage is not None:
                print(retry_now(hero))
            print("Fighting... press Ctrl+C to pause.")
            run_fights(hero, rng, save_path, speed=speed)
        elif choice == "s":
            shop_menu(hero)
            save_game(hero, save_path)
        elif choice == "h":
            print_hero(hero)
        elif choice == "q":
            return
        else:
            print("Unknown choice.")

# ===================================================================
#                                                                MAIN
# ===================================================================

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--class", dest="spec", type=str.capitalize, choices=list(CLASSES),
                        help="class for a new hero (asked interactively if omitted)")
    parser.add_argument("--new", action="store_true", help="start a new hero (overwrites the save file)")
    parser.add_argument("--save", type=Path, default=DEFAULT_SAVE, help="save file (default: %(default)s)")
    parser.add_argument("--speed", type=float, default=0.25, help="seconds per turn (default: 0.25, 0 = instant)")
    parser.add_argument("--fights", type=int, help="fight this many stages without the menu, then save and quit")
    parser.add_argument("--autobuy", action="store_true", help="with --fights: buy the cheapest upgrades after every fight")
    parser.add_argument("--seed", type=int, help="random seed, for reproducible runs")
    args = parser.parse_args()
    rng = random.Random(args.seed)

    try:
        hero = None if args.new else load_game(args.save)
    except ValueError as e:
        print(f"Can't load the save: {e}\nStart over with --new.")
        return

    try:
        if hero is None:
            hero = Hero(args.spec or choose_class())
            print(f"A new hero is born: {hero.name} the {hero.spec}!")
        else:
            if args.spec:
                print("A save already exists, so --class is ignored. Use --new to start over.")
            gold, xp, seconds = offline_rewards(hero)
            if gold:
                levels = hero.gain(gold, xp)
                print(f"While you were away for {seconds / 60:.0f} minutes, {hero.name} earned {gold} gold and {xp} XP"
                      + (f" and gained {levels} level(s)!" if levels else "."))
        save_game(hero, args.save)

        if args.fights:
            run_fights(hero, rng, args.save, count=args.fights, speed=args.speed, buy_upgrades=args.autobuy)
            print(f"\nStage {hero.stage}, best {hero.best_stage}, level {hero.level}, {hero.gold} gold. Saved.")
        else:
            main_menu(hero, rng, args.save, args.speed)
    except (EOFError, KeyboardInterrupt):
        print()
    if hero is not None:
        save_game(hero, args.save)
        print("Game saved. Bye!")


if __name__ == "__main__":
    main()
