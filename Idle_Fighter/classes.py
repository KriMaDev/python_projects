# ===================================================================
#                                                             CLASSES
# ===================================================================

class Character:
    """A fighter with combat stats. Regen values are per second."""

    def __init__(self, name: str, spec: str, damage: float, crit_rate: float, crit_chan: float, health: float,
                 mana: float, shield: float, h_regen: float, m_regen: float, s_regen: float) -> None:
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

    def attack(self) -> None:
        print("Attacking")

    def defend(self) -> None:
        print("Defending")

    def regen(self) -> None:
        print("Regenerating")

    def print_stats(self) -> None:
        """Print all stats of the character."""
        print(f"Name: {self.name}\nClass: {self.spec}\nHealth: {self.health}\nMana: {self.mana}\nShield: {self.shield}\n"
              f"Damage: {self.damage}\nCritical Rate: {self.crit_rate}\nCritical Chance: {self.crit_chan}\nHealth Regeneration: {self.h_regen}per sec.\nMana Regeneration: {self.m_regen}per sec.\n"
              f"Shield Regeneration: {self.s_regen}per sec.")
