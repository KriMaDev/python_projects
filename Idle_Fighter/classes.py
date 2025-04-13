# ===================================================================
#                                                             CLASSES
# ===================================================================

class Character:
    def __init__(self, name, spec, damage, crit_rate, crit_chan, health, mana, shield, h_regen, m_regen, s_regen):
        self.name        = name
        self.spec        = spec
        self.damage      = damage
        self.crit_rate   = crit_rate
        self.crit_chan   = crit_chan
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
              f"Damage: {self.damage}\nCritical Rate: {self.crit_rate}\nCritical Chance: {self.crit_chan}\nHealth Regeneration: {self.h_regen}per sec.\nMana Regeneration: {self.m_regen}per sec.\n"
              f"Shield Regeneration: {self.s_regen}per sec.")
