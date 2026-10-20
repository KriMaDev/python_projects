from classes import Character

# ===================================================================
#                                                             PRESETS
# ===================================================================

# Starting stats per class
PRESETS = {
    "Melee":    dict(name="Sir Smacks-a-Lot", damage=15,   crit_chan=0.15, crit_rate=3,   health=100, mana=50,  shield=50,  h_regen=1,   m_regen=0.5, s_regen=1),
    "Ranged":   dict(name="Robin Hoodie",     damage=20,   crit_chan=0.25, crit_rate=3.5, health=50,  mana=75,  shield=50,  h_regen=0.7, m_regen=1,   s_regen=0.7),
    "Tank":     dict(name="Captain Bulwark",  damage=7.5,  crit_chan=0.15, crit_rate=4.5, health=150, mana=25,  shield=150, h_regen=2,   m_regen=1.5, s_regen=2),
    "Support":  dict(name="Medic Molly",      damage=12,   crit_chan=0.35, crit_rate=2.5, health=75,  mana=75,  shield=100, h_regen=1.5, m_regen=1.5, s_regen=1),
    "Assassin": dict(name="Mister Ladybug",   damage=35,   crit_chan=0.45, crit_rate=4,   health=25,  mana=75,  shield=25,  h_regen=1,   m_regen=1,   s_regen=1),
    "Mage":     dict(name="Perry Hotter",     damage=25,   crit_chan=0.55, crit_rate=2.5, health=25,  mana=100, shield=150, h_regen=1,   m_regen=2,   s_regen=2),
    "Debuffer": dict(name="Asmodeus",         damage=17.5, crit_chan=0.40, crit_rate=3,   health=75,  mana=75,  shield=100, h_regen=0.5, m_regen=1,   s_regen=0.5),
}

# ===================================================================
#                                                           FUNCTIONS
# ===================================================================

def create_character(spec: str) -> Character:
    """Create the preset character for a class name (case-insensitive). Raises ValueError if unknown."""
    spec = spec.strip().capitalize()
    if spec not in PRESETS:
        raise ValueError(f"Unknown class '{spec}'. Choose from: {', '.join(PRESETS)}")
    return Character(spec=spec, **PRESETS[spec])


def choose_character() -> Character:
    """Ask for a class until a valid one is entered and return its character."""
    while True:
        spec = input(f"Select a class:\n{list(PRESETS)}\n: ")
        try:
            return create_character(spec)
        except ValueError:
            print("Please choose from predefined classes!")


def fight(player: Character, enemy: Character) -> str:
    """Let the player and enemy take turns hitting each other. Returns 'player', 'enemy' or 'draw'."""
    turn = 2
    while player.health > 0 and enemy.health > 0 and turn <= 50:
        if (turn % 2 == 0):
            caused_dmg = player.damage
            enemy.health -= caused_dmg
            print(f"Inflicted {caused_dmg} Damage to the enemy!")
            print(f"Enemy health is now {enemy.health}HP!")
        else:
            caused_dmg = enemy.damage
            player.health -= caused_dmg
            print(f"Enemy has inflicted {caused_dmg} Damage to you!")
            print(f"Your health is now {player.health}HP!")
        turn += 1

    if (player.health <= 0 and enemy.health > 0):
        print(f"You have been defeated! Enemy still has {enemy.health}HP left!")
        return "enemy"
    elif (enemy.health <= 0 and player.health > 0):
        print(f"Enemy has been defeated! You survived with {player.health}HP left!")
        return "player"
    print(f"Draw! Nobody won within the turn limit. Enemy has {enemy.health}HP and you have {player.health}HP left.")
    return "draw"
