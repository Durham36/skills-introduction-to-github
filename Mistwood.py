import random
from Mistwood_classes import Player # Item, HealthPotion, FireOrb, EarthOrb, Player

player = Player()

biome = ["Mistwood Forest", "Haunted Woods", "Desert Temple"]
levels = ["Easy (lvl 0)", "Medium (lvl 1)", "Hard (lvl 2)"]

Roll1 = random.randint(0, 2)
print(biome[Roll1], levels[Roll1])

Monster0 = {
    "Common": [
        {"name": "Mistwood Spider", "health": 2, "min_attack": 0, "max_attack": 1, "gold_drop": 1},
    ],
    "Rare": [
        {"name": "Mistwood Ooze", "health": 3, "min_attack": 0, "max_attack": 2, "gold_drop": 2},
        {"name": "Mistwood Serpent", "health": 4, "min_attack": 0, "max_attack": 1, "gold_drop": 2},
    ],
    "Boss": [
        {"name": "Spider Queen", "health": 5, "min_attack": 0, "max_attack": 3, "gold_drop": 5},
        {"name": "Giant Ooze", "health": 4, "min_attack": 1, "max_attack": 2, "gold_drop": 4},
        {"name": "Corrupted Serpent", "health": 7, "min_attack": 0, "max_attack": 1, "gold_drop": 4},
    ],
    "Legendary": [
        {"name": "The Ancient Wyrm", "health": 12, "min_attack": 1, "max_attack": 3, "gold_drop": 10}
    ]
}

ShopB = {
    "Orbs": [
        ("Fire Orb", 2),
        ("Water Orb", 3),
        ("Earth Orb", 3),
        ("Mana Orb", 3)
    ]
}

Shop0 = {
    "Potions": [("Health Potion", 5)],
    "Weapons": [("Dagger", 7)],
    "Spells": [("FireBall", 7)],
    "Armor": [("Leather Armor", 10)]
}

Shop1 = {
    "Orbs": [("Orb of Acid", 3), ("Orb of Return", 8)],
    "Weapons": [("Rune Dagger", 10)],
    "Spells": [("FireBall II", 10), ("Lesser Heal", 8), ("FireBolt", 10)],
    "Armor": [("Rune Hide Armor", 15)]
}

def open_store(shop_dict, shop_name):
    print(f"\n{shop_name}\n")
    items_for_sale = []
    i = 1

    for category, items in shop_dict.items():
        print(f"{category}:")
        for item_name, price in items:
            print(f" {i}. {item_name} - {price} Gold")
            items_for_sale.append((item_name, price))
            i += 1
        print()

    choice = input("Enter the number of the item you want to buy (or press enter to leave): ")
    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(items_for_sale):
            item_name, price = items_for_sale[choice - 1]
            player.buy_item(item_name, price)
        else:
            print("Invalid choice.")
    else:
        print("Leaving shop.")

def StoreB():
    open_store(ShopB, "Mistwood Basic Shop")

def Store0():
    open_store(Shop0, "Mistwood Shop Level 0")

def Store1():
    open_store(Shop1, "Mistwood Shop Level 1")

def encounter_monster():
    category = random.choice(["Common", "Rare"])
    monsters = Monster0[category]
    monster = random.choice(monsters)
    print(f"\nA wild {monster['name']} has appeared! (Category: {category})")
    combat(monster)

def combat(monster, allow_heal=True):
    print(f"Engaging in combat with {monster['name']}...\n")
    monster_health = monster["health"]
    print(f"{monster['name']} has {monster_health} HP.")

    while monster_health > 0 and player.health > 0:
        monster_dice_roll = random.randint(1, 4)
        if monster_dice_roll == 1:
            predicted_damage = monster["min_attack"]
        elif monster_dice_roll in [2, 3]:
            predicted_damage = (monster['min_attack'] + monster['max_attack']) // 2
        else:
            predicted_damage = monster['max_attack']

        if player.earth_orb_charges > 0 and predicted_damage > 0:
            preview_damage = max(0, predicted_damage - player.earth_orb_charges)
            print(f"\n[Pre-Attack] The {monster['name']} prepares to strike for {preview_damage} damage (Earth Orb active)!")
        else:
            print(f"\n[Pre-Attack] The {monster['name']} prepares to strike for {predicted_damage} damage!")

        valid_turn = False
        while not valid_turn:
            action = input("\nYour turn! (Attack / Run / Inventory / Use Item): ").strip().lower()
            
            if action == "inventory":
                player.show_inventory()

            elif action == "use item":
                player.use_item()

            elif action == "attack":
                if player.dagger_active:
                    player_damage = random.randint(1, 4)
                    print("Dagger active!")
                    player.dagger_active = False
                else:
                    player_dice_roll = random.randint(1, 4)
                    if player_dice_roll == 1:
                        player_damage = 0
                    elif player_dice_roll in (2, 3):
                        player_damage = 1
                    else:
                        player_damage = 2

                bonus = player.fire_orb_bonus + player.fireball_bonus
                player.fire_orb_bonus = player.firevall_bonus = 0
                
                player_damage += bonus
                if bonus:
                    print("fSpell/Orb Bonus! +{bonus} damage!")


                monster_health -= player_damage
                print(f"\nYou attack {monster['name']} and deal {player_damage} damage!")
                print(f"{monster['name']} now has {max(monster_health, 0)} HP left.")
                valid_turn = True

            elif action == "run":
                print("\nYou ran away from the battle!")
                return

            else:
                print("Invalid action.")


        if monster_health <= 0:
            print(f"\nYou defeated {monster['name']}! Monster defeated.")
            gold_reward = monster.get("gold_drop", 1)
            player.gold += gold_reward
            print(f"\nYou defeated {monster['name']}! It dropped {gold_reward} gold.")
            
            if allow_heal:
                player.health = player.max_health
            player.show_inventory()
            break

        print(f"\n{monster['name']}'s turn!")
        monster_damage = predicted_damage
        monster_damage_before = predicted_damage
        monster_damage = monster_damage_before
        
        if player.earth_orb_charges > 0:
            reduction = min(monster_damage, player.earth_orb_charges)
            monster_damage -= reduction
            print(f"Earth Orb effect: Enemy attack reduced by {reduction}!")
            player.earth_orb_charges -= reduction

        armor_blocked = 0
        if player.armor_equipped == "Leather Armor" and monster_damage > 0:
            armor_blocked = 1
            monster_damage -= armor_blocked
            print("Your Armor reduces the damage by 1!")

        if monster_damage > 0:
            player.health -= monster_damage
            print(f"{monster['name']} attacks you for {monster_damage} damage!")
            print(f"You now have {max(player.health,0)} HP left.")
        else:
            print(f"{monster['name']} attacks but deals no damage!")
                
        if player.armor_equipped == "Leather Armor" and armor_blocked and monster_damage > 0:
            player.armor_equipped = None
            
            for i, itm in enumerate(player.inventory):
                if itm.name == "Leather Armor":
                    del player.inventory[i]
                    break
            print("Your Leather Armor absorbed damage and broke!")

        if player.health <= 0:
            print("\nYou have been defeated!")
            print("Game Over - You Died")
            player.inventory = []
            player.gold = 0
            player.health = player.max_health
            player.level = 0
            
            return

def Mob0():
    encounter_monster()
    
    
def legendary_boss_fight():
    print("\nA Starting Legendary Boss Fight!")
    monster = random.choice(Monster0["Legendary"])
    combat(monster, allow_heal=False)
    
    if player.health > 0:
        player.show_inventory()
    
    
def boss_gauntlet():
    print("\nStarting the Gauntlet")

    all_monster_categories = ["Common", "Rare", "Boss"]

    for category in all_monster_categories:
        if player.health <= 0:
            print("You Died!")
            return

        print(f"\nNext up: {category} Monster")
        monster = random.choice(Monster0[category])
        combat(monster, allow_heal=False)

        if player.health <= 0:
            print("You were defeated during the Gauntlet.")
            return

    player.health = player.max_health
        
        
def main_menu():
    while True:
        print("\n=== Main Menu ===")
        print("1. Fight a Monster")
        print("2. Boss Gauntlet")
        print("3. Show Inventory")
        print("4. Open Store Level (Basic)")
        print("5. Open Store Level (0)")
        print("6. Exit")
        print("7. Fight the Legendary Boss")
        
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            Mob0()
        elif choice == "2":
            boss_gauntlet()
        elif choice == "3":
            player.show_inventory()
        elif choice == "4":
            StoreB()
        elif choice == "5":
            Store0()
        elif choice == "6":
            print("Exit")
            break
        elif choice == "7":
            legendary_boss_fight()
        else:
            print("Invalid option")
        
if __name__ == "__main__":
    main_menu()