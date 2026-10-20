"""Idle Fighter: pick a class and watch your character fight the Orange Cat boss."""
import argparse

from classes import Character
from functions import PRESETS, choose_character, create_character, fight

# ===================================================================
#                                                                MAIN
# ===================================================================

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--class", dest="spec", type=str.capitalize, choices=list(PRESETS),
                        help="class to play (asked interactively if omitted)")
    args = parser.parse_args()

    try:
        player = create_character(args.spec) if args.spec else choose_character()
    except (EOFError, KeyboardInterrupt):
        print("\nNo class chosen. Bye!")
        return
    enemy  = Character("Orange Cat", "Boss", 3, 2, 0.2, 150, 100, 150, 0.2, 0.2, 0.2)
    fight(player, enemy)


if __name__ == "__main__":
    main()
