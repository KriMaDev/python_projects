# Idle Fighter

An idle auto battler for the terminal. Your hero fights stage after stage on their own, earning gold
and XP. Every **5th stage is a mini boss** and every **10th a boss**. When a boss is too strong, the
hero falls back a stage and farms gold until they are ready to try again. You make the decisions between
fights: what to buy, how your hero should fight, and whether you want to take control in boss fights
yourself.

This started as my first object-oriented Python project (pick a class, watch one fight) and grew into
a small game with a combat engine, progression, save games and a test suite.

## Setup

From the repository root, with your virtual environment active (see the [main README](../README.md#setup)):

```bash
pip install -r Idle_Fighter/requirements.txt
```

## How to run

```bash
python Idle_Fighter/main.py                    # continue your saved hero, or create one
python Idle_Fighter/main.py --new --class mage # start over with a new Mage
python Idle_Fighter/main.py --speed 0          # no delay between turns
python Idle_Fighter/main.py --fights 50 --autobuy --speed 0   # fight 50 stages unattended, then quit
python Idle_Fighter/main.py --help
```

| Option | Meaning |
|---|---|
| `--class NAME` | Class for a new hero (asked if omitted) |
| `--new` | Start a new hero, replacing the save |
| `--speed SECONDS` | Delay per turn, default `0.25`. Use `0` for instant fights |
| `--fights N` | Fight N stages without the menu, then save and quit |
| `--autobuy` | Turn on auto-buying upgrades after every fight (stored in your tactics) |
| `--save PATH` | Use a different save file (default `Idle_Fighter/savegame.json`) |
| `--seed N` | Fixed random seed, so a run can be repeated exactly |

In the menu, **[F]ight** keeps fighting until you press **Ctrl+C**, which pauses and returns to the menu.
The game saves after every fight and when you quit.

## How it plays

- **Combat:** hero and enemy take turns. Shields absorb damage before health, hits can be critical,
  and health, shield and mana regenerate a little every turn.
- **Abilities:** each class has one, paid for with mana. Mana carries over between fights (+10% after a
  win, full after a defeat), so it's worth deciding when to spend it.
- **Stages:** enemies get stronger every stage. Stages 5, 15, 25… are mini bosses (Stone Golem, Swamp Witch)
  and stages 10, 20, 30… are bosses (Orange Cat, Ember Dragon, Old Lich). Bosses use abilities too.
- **Defeat:** you fall back one stage and farm it. After 5 wins the hero retries the stage they lost on.
  Starting **[F]ight** from the menu retries straight away, for example after shopping.
- **Rewards:** gold and XP grow every stage. Mini bosses give 4× and bosses 10×. XP raises your hero
  level (+5% damage, health and shield per level).
- **Offline progress:** when you come back, the hero has kept farming. You get half rewards, for up to 8 hours.

### Your decisions

| Where | What you decide |
|---|---|
| **[S]hop** | Spend gold on Sharpen (+10% damage), Armor (+10% health), Barrier (+10% shield), Focus (+2% crit) or Meditation (+0.5 mana regen). Each level costs more |
| **[T]actics** | Use the ability *always*, *on bosses only* (save mana) or *never*. Defend when health is below 25% or 50% (halves damage, restores mana). Auto-buy upgrades |
| **Manual control** | A tactics option: you choose **attack / skill / defend** every turn, but only in mini boss and boss fights |

In an idle game the hero fights alone, so most decisions are standing orders (tactics) and upgrades. Turn by
turn control is kept for boss fights, where it matters most.

## Classes

| Class | Character | Ability (mana) | Plays like |
|---|---|---|---|
| Melee | Sir Smacks-a-Lot | Cleave (20): double damage | Sturdy all-rounder |
| Ranged | Robin Hoodie | Aimed Shot (25): 1.5× damage, +50% crit chance | Fragile, big crits |
| Tank | Captain Bulwark | Shield Wall (15): restore half your shield | Slow, very hard to kill |
| Support | Medic Molly | Heal (25): restore 35% health | Outlasts enemies |
| Assassin | Mister Ladybug | Backstab (30): guaranteed critical hit | Glass cannon |
| Mage | Perry Hotter | Fireball (30): 1.5× damage, ignores shields | Burns through shielded bosses |
| Debuffer | Asmodeus | Weaken (20): hit, and the enemy deals 20% less damage (to −50%) | Makes bosses harmless |

The stats are balanced with a simulation, so every class can clear stage 30 when it buys upgrades.
Tank and Mage get there fastest, Melee and Ranged slowest.

## Example output

```text
Stage 10 (BOSS)  ·  Lv 4 Perry Hotter  ·  176 gold  ·  XP ███████░░░ 31/44
Next: BOSS Orange Cat this stage!
[F]ight  [S]hop  [T]actics  [H]ero  [Q]uit
: f
─────────────── Stage 10 · BOSS · Orange Cat ───────────────
 T1  ██████████   46/46   140sh  10mp │ Fireball 43 · Orange Cat: Backstab 36 CRIT!  │ █████████░  367/409  230sh  32mp
 T2  ██████████   46/46   106sh  12mp │ Hit 72 CRIT! · Orange Cat: Backstab 36 CRIT! │ █████████░  368/409  159sh   4mp
 ...
 T11 ██░░░░░░░░   10/46     2sh  30mp │ Hit 29 · Orange Cat: Hit 18                  │ ████░░░░░░  159/409    1sh  22mp
 T12 ░░░░░░░░░░    0/46     0sh   0mp │ Fireball 109 CRIT! · Orange Cat: Hit 18      │ █░░░░░░░░░   51/409    3sh  24mp
DEFEATED by Orange Cat after 12 turns.
Falling back to stage 9 to farm. Retrying stage 10 after 5 wins.
```

Each line shows **your** health bar, shield (`sh`) and mana (`mp`), then what happened, then the enemy's
bars. In the terminal, health bars are green and red and critical hits are yellow.

## Code structure

| File | What it contains |
|---|---|
| `main.py` | Entry point: arguments, menus, the fight loop |
| `characters.py` | `Stats` and `Fighter` dataclasses, the seven classes |
| `abilities.py` | `Ability` base class and one subclass per ability |
| `combat.py` | Turn-based fight logic. Pure functions with a seedable RNG, output goes through a callback |
| `enemies.py` | Enemy roster, stage types (normal / mini boss / boss), scaling and rewards |
| `hero.py` | The saved hero: level, XP, gold, stage, upgrades, tactics |
| `game.py` | One stage of play, and the push / fall back / farm / retry rules |
| `shop.py` | Upgrades and their costs |
| `tactics.py` | Standing orders and manual control |
| `savegame.py` | JSON save file (written safely via a temporary file) and offline rewards |
| `ui.py` | HP bars, turn lines, banners and the menu header |

The game logic never prints anything itself. That keeps it testable: the tests in
[`tests/`](../tests/) fight with a fixed seed or a fake random generator.

## Planned

- More enemy types and abilities for regular enemies
- Prestige: restart at stage 1 with a permanent bonus
- Equipment drops from bosses
