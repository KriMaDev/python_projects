from classes import *
from functions import *

# ===================================================================
#                                                                MAIN
# ===================================================================

player = chooseCharacter()
enemy  = Character("Orange Cat", "Boss", 3, 2, 0.2, 150, 100, 150, 0.2, 0.2, 0.2)

turn = 2
while player.health > 0 and enemy.health > 0 and turn <= 50:
    if (turn % 2 == 0):
        caused_dmg = player.damage
        enemy.health -= caused_dmg
        print(f"Inflicted {caused_dmg} Damage to the enemy!")
        print(f"Enemy health is now {enemy.health}HP!")
        turn += 1
    else:
        caused_dmg = enemy.damage
        player.health -= caused_dmg
        print(f"Enemy has inflicted {caused_dmg} Damage to you!")
        print(f"Your health is now {player.health}HP!")
        turn += 1
    

if (player.health <= 0 and enemy.health > 0):
    print(f"You have been defeated! Enemy still has {enemy.health}HP left!")
elif (enemy.health <= 0 and player.health > 0):
    print(f"Enemy has been defeated! You survived with {player.health}HP left!")
else: 
    print(f"Draw! Nobody won within the turn limit. Enemy has {enemy.health}HP and you have {player.health}HP left.")