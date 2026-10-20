# Idle Fighter

A small text-based auto battler and my first object-oriented Python project. Pick a class and your
character fights the **Orange Cat** boss turn by turn until one of you drops (or 49 turns pass).

| File | What it contains |
|---|---|
| `main.py` | Entry point: choose a class, start the fight |
| `classes.py` | The `Character` class with all combat stats |
| `functions.py` | Class presets, `create_character()`, the interactive class picker and `fight()` |

Only the Python standard library is used, so there is nothing to install.

## How to run

From the repository root:

```bash
python Idle_Fighter/main.py               # pick a class interactively
python Idle_Fighter/main.py --class mage  # skip the question (not case-sensitive)
python Idle_Fighter/main.py --help
```

## Classes

| Class | Character | Damage | Health | Shield | Mana |
|---|---|---|---|---|---|
| Melee | Sir Smacks-a-Lot | 15 | 100 | 50 | 50 |
| Ranged | Robin Hoodie | 20 | 50 | 50 | 75 |
| Tank | Captain Bulwark | 7.5 | 150 | 150 | 25 |
| Support | Medic Molly | 12 | 75 | 100 | 75 |
| Assassin | Mister Ladybug | 35 | 25 | 25 | 75 |
| Mage | Perry Hotter | 25 | 25 | 150 | 100 |
| Debuffer | Asmodeus | 17.5 | 75 | 100 | 75 |

Every class also has critical hit and regeneration stats. These are defined but not used in fights yet.

## Example output

```text
$ python Idle_Fighter/main.py
Select a class:
['Melee', 'Ranged', 'Tank', 'Support', 'Assassin', 'Mage', 'Debuffer']
: Tank
Inflicted 7.5 Damage to the enemy!
Enemy health is now 142.5HP!
Enemy has inflicted 3 Damage to you!
Your health is now 147HP!
...
Inflicted 7.5 Damage to the enemy!
Enemy health is now 0.0HP!
Enemy has been defeated! You survived with 93HP left!
```

## Planned

- Use critical hits, shields and regeneration in the fight
- Let the `attack`, `defend` and `regen` methods do real work instead of placeholders
