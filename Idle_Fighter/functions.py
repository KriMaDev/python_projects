from classes import *

# ===================================================================
#                                                           FUNCTIONS
# ===================================================================

def chooseCharacter():
    specs_arr = ["Melee", "Ranged", "Tank", "Support", "Assassin", "Mage", "Debuffer"]
    spec = ""
    try:
        while (spec not in specs_arr):
            spec   = str(input(f"Select a class:\n{specs_arr}\n: "))
            if (spec in specs_arr):
                match spec:
                    case "Melee":
                        name      = "Sir Smacks-a-Lot"
                        spec      = "Melee"
                        damage    = 15
                        crit_chan = 0.15
                        crit_rate = 3
                        health    = 100
                        mana      = 50
                        shield    = 50
                        h_regen   = 1
                        m_regen   = 0.5
                        s_regen   = 1
                    case "Ranged":
                        name      = "Robin Hoodie"
                        spec      = "Ranged"
                        damage    = 20
                        crit_chan = 0.25
                        crit_rate = 3.5
                        health    = 50
                        mana      = 75
                        shield    = 50
                        h_regen   = 0.7
                        m_regen   = 1
                        s_regen   = 0.7
                    case "Tank":
                        name      = "Captain Bulwark"
                        spec      = "Tank"
                        damage    = 7.5
                        crit_chan = 0.15
                        crit_rate = 4.5
                        health    = 150
                        mana      = 25
                        shield    = 150
                        h_regen   = 2
                        m_regen   = 1.5
                        s_regen   = 2
                    case "Support":
                        name      = "Medic Molly"
                        spec      = "Support"
                        damage    = 12
                        crit_chan = 0.35
                        crit_rate = 2.5
                        health    = 75
                        mana      = 75
                        shield    = 100
                        h_regen   = 1.5
                        m_regen   = 1.5
                        s_regen   = 1
                    case "Assassin":
                        name      = "Mister Ladybug"
                        spec      = "Assassin"
                        damage    = 35
                        crit_chan = 0.45
                        crit_rate = 4
                        health    = 25
                        mana      = 75
                        shield    = 25
                        h_regen   = 1
                        m_regen   = 1
                        s_regen   = 1
                    case "Mage":
                        name      = "Perry Hotter"
                        spec      = "Mage"
                        damage    = 25
                        crit_chan = 0.55
                        crit_rate = 2.5
                        health    = 25
                        mana      = 100
                        shield    = 150
                        h_regen   = 1
                        m_regen   = 2
                        s_regen   = 2
                    case "Debuffer":
                        name      = "Asmodeus"
                        spec      = "Debuffer"
                        damage    = 17.5
                        crit_chan = 0.40
                        crit_rate = 3
                        health    = 75
                        mana      = 75
                        shield    = 100
                        h_regen   = 0.5
                        m_regen   = 1
                        s_regen   = 0.5
                    case _:
                        print("The class you selected is invalid.")
                player = Character(name, spec, damage, crit_rate, crit_chan, health, mana, shield, h_regen, m_regen, s_regen)
                return player
            else:
                print("Please choose from predefined classes!")
    except:
        print("Invalid input.")