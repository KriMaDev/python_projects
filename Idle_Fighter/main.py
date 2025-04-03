from classes import *
from functions import *

# ===================================================================
#                                                                MAIN
# ===================================================================

player = chooseCharacter()
enemy  = Character("Orange Cat", "Boss", 30, 20, 150, 100, 150, 2, 2, 2)

cc = 0
while player.health > 0 and enemy.health > 0:
    print("We living")
    player.health -= 1
    cc += 1
print(cc)