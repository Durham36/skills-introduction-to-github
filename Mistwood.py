import random
from Mistwood_classes import Item, HealthPotion, FireOrb, EarthOrb, Player

# ---- Combat System and Game ----
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
    "Spells": [("Fireball", 7)],
    "Armor": [("Leather Armor", 10)]
}

Shop1 = {
    "Orbs": [("Orb of Acid", 3), ("Orb of Return", 8)],
    "Weapons": [("Rune Dagger", 10)],
    "Spells": [("Fireball II", 10), ("Lesser Heal", 8), ("FireBolt", 10)],
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
            predicted_damage = monster["mins_attack"]
        elif monster_dice_roll in [2, 3]:
            predicted_damage = (monster['min_attack'] + monster['max_attack']) // 2
        else:
            predicted_damage = monster['max_attack']
            
            if player.earth_orb_active and predicted_damage > 0:
                preview_damage = max(0, predicted_damage - 1)
                print(f"\n[Danger Sense] the {monster['name']} prepares to strike for {preview_damage} damage (Earth Orb active)!")
            else:
                print(f"\n[Danger Sense] The {monster['name']} prepares to strike for {predicted_damage} damage!")
                
        while True:
            action = input("\nYour turn! (Attack / Run / Inventory / Use Item): ").strip().lower()
            if action == "inventory":
                player.show_inventory()  # Display inventory when 'inventory' is typed
            elif action == "use item":
                player.use_item()
            elif action == "attack":
                player_dice_roll = random.randint(1, 4)
                if player_dice_roll == 1:
                    player_damage = 0
                elif player_dice_roll in [2, 3]:
                    player_damage = 1
                else:
                    player_damage = 2

                bonus = player.fire_orb_bonus
                player.fire_orb_bonus = 0
                player_damage += bonus
                if bonus:
                    print("Fire Orb Bonus! +1 damage")

                monster_health -= player_damage
                print(f"\nYou attack {monster['name']} and deal {player_damage} damage!")
                print(f"{monster['name']} now has {max(monster_health, 0)} HP left.")
                break
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
            player.show_inventory()  # Show inventory after defeating the monster
            break

        print(f"\n{monster['name']}'s turn!")
        monster_dice_roll = random.randint(1, 4)
        if monster_dice_roll == 1:
            monster_damage = monster['min_attack']
        elif monster_dice_roll in [2, 3]:
            monster_damage = (monster['min_attack'] + monster['max_attack']) // 2
        else:
            monster_damage = monster['max_attack']

        if player.earth_orb_active:
            monster_damage = max(0, monster_damage - 1)
            player.earth_orb_active = False
            print("Earth Orb effect: Enemy attack reduced by 1!")

        player.health -= monster_damage
        print(f"{monster['name']} attacks you for {monster_damage} damage!")
        print(f"You now have {max(player.health, 0)} HP left.")

        if player.health <= 0:
            print("\nYou have been defeated!")
            player.inventory = []
            player.gold = 0
            player.health = player.max_health
            player.level = 0
            print("Game Over - You Died")
            return

def Mob0():
    encounter_monster()
    
def boss_gauntlet():
    print("\nStarting the Gauntlet")
    
    # List of categories: Common, Rare, Boss
    all_monster_categories = ["Common", "Rare", "Boss"]
    
    # Loop through the categories and encounter monsters
    for category in all_monster_categories:
        if player.health <= 0:
            print("You Died!")
            return
        
        print(f"\nNext up: {category} Monster")
        monster = random.choice(Monster0[category])
        
        # Check if it's the last monster
        is_last_monster = category == all_monster_categories[-1]
        
        combat(monster, allow_heal=False)  # Don't heal after each monster
        
        # Only heal after the last monster is defeated
        if is_last_monster and player.health > 0:
            print("\nYou defeated the last monster of the gauntlet!")
            player.health = player.max_health
            print("You heal to full health.")

    # If the player is still alive after all monsters
    if player.health > 0:
        print("\nYou won the Gauntlet!")
    else:
        print("Game Over - You Died")
        
        
def main_menu():
    while True:
        print("\n=== Main Menu ===")
        print("1. Fight a Monster")
        print("2. Boss Gauntlet")
        print("3. Show Inventory")
        print("4. Open Store Level (Basic)")
        print("5. Open Store Level (0)")
        print("6. Exit")
        
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
        else:
            print("Invalid option")
        
if __name__ == "__main__":
    main_menu()