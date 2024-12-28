class Character:
    def __init__(self, name, spec, damage, crit_rate, health, mana, shield, h_regen, m_regen, s_regen):
        self.name        = name
        self.spec        = spec
        self.damage      = damage
        self.crit_rate   = crit_rate
        self.health      = health
        self.mana        = mana
        self.shield      = shield
        self.h_regen     = h_regen
        self.m_regen     = m_regen
        self.s_regen     = s_regen

    def attack(self):
        print("Attacking")

    def defend(self):
        print("Defending")

    def regen(self):
        print("Regenerating")

    def print_stats(self):
        print(f"Name: {self.name}\nClass: {self.spec}\nHealth: {self.health}\nMana: {self.mana}\nShield: {self.shield}\n"
              f"Damage: {self.damage}\nCritical Rate: {self.crit_rate}\nHealth Regeneration: {self.h_regen}per sec.\nMana Regeneration: {self.m_regen}per sec.\n"
              f"Shield Regeneration: {self.s_regen}per sec.")

# ===================================================================
#                                                                MAIN
# ===================================================================
specs_arr = ["Melee", "Ranged", "Tank", "Support", "Assassin", "Mage", "Debuffer"]
try:
    name   = str(input("Enter character name: "))
    spec   = str(input(f"Select a class:\n{specs_arr}\n: "))
    match spec:
        case "Melee":
            damage    = 15
            crit_rate = 30
            health    = 100
            mana      = 50
            shield    = 50
            h_regen   = 1
            m_regen   = 0.5
            s_regen   = 1
        case "Ranged":
            damage    = 20
            crit_rate = 35
            health    = 50
            mana      = 75
            shield    = 50
            h_regen   = 0.7
            m_regen   = 1
            s_regen   = 0.7
        case "Tank":
            damage    = 7.5
            crit_rate = 15
            health    = 150
            mana      = 25
            shield    = 150
            h_regen   = 2
            m_regen   = 1.5
            s_regen   = 2
        case "Support":
            damage    = 12
            crit_rate = 25
            health    = 75
            mana      = 75
            shield    = 100
            h_regen   = 1.5
            m_regen   = 1.5
            s_regen   = 1
        case "Assassin":
            damage    = 35
            crit_rate = 45
            health    = 25
            mana      = 75
            shield    = 25
            h_regen   = 1
            m_regen   = 1
            s_regen   = 1
        case "Mage":
            damage    = 25
            crit_rate = 40
            health    = 25
            mana      = 100
            shield    = 150
            h_regen   = 1
            m_regen   = 2
            s_regen   = 2
        case "Debuffer":
            damage    = 17.5
            crit_rate = 30
            health    = 75
            mana      = 75
            shield    = 100
            h_regen   = 0.5
            m_regen   = 1
            s_regen   = 0.5
        case _:
            print("The class you selected is invalid.")
except:
    print("Invalid input.")


player = Character(name, spec, damage, crit_rate, health, mana, shield, h_regen, m_regen, s_regen)
enemy  = Character("Orange Cat", "Boss", 30, 20, 150, 100, 150, 2, 2, 2)

print(f"Ladies & Gentleman, Today we are here to witness the battle between: {player.name} VS {enemy.name}\n")
player.print_stats()
print("\nVS\n")
enemy.print_stats()
