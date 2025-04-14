import random

# ---- Item Classes ----
class Item:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def use(self, player):
        print(f"You used {self.name}, but nothing happened.")

class HealthPotion(Item):
    def __init__(self):
        super().__init__("Health Potion", 5)

    def use(self, player):
        if player.health < player.max_health:
            heal_amount = 2
            player.health = min(player.max_health, player.health + heal_amount)
            print(f"You used a Health Potion and healed {heal_amount} HP!")
        else:
            print("Your health is already full.")

class FireOrb(Item):
    def __init__(self):
        super().__init__("Fire Orb", 2)

    def use(self, player):
        player.fire_orb_bonus = 1
        print("You used a Fire Orb! +1 damage on your next attack.")

# ---- Player Class ----
class Player:
    def __init__(self):
        self.inventory = []
        self.gold = 10
        self.health = 3
        self.max_health = 3
        self.level = 0
        self.fire_orb_bonus = 0

    def use_item(self):
        if not self.inventory:
            print("Your inventory is empty.")
            return

        print("\nInventory Items:")
        for i, item in enumerate(self.inventory, 1):
            print(f"{i}. {item.name}")

        choice = input("Enter the number of the item you want to use (or press enter to cancel): ").strip()
        if not choice:
            print("Cancelled item use.")
            return

        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(self.inventory):
                item = self.inventory.pop(index)
                item.use(self)
            else:
                print("Invalid item number.")
        else:
            print("Invalid input.")

    def buy_item(self, item_name, item_cost):
        item_lookup = {
            "Health Potion": HealthPotion,
            "Fire Orb": FireOrb,
        }

        if self.gold >= item_cost:
            item_class = item_lookup.get(item_name)
            if item_class:
                self.inventory.append(item_class())
            else:
                print(f"{item_name} is not implemented as a class. Adding as placeholder.")
                self.inventory.append(Item(item_name, item_cost))
            self.gold -= item_cost
            print(f"\nYou bought {item_name} for {item_cost} gold.")
        else:
            print(f"Not enough gold to buy {item_name}.")

    def show_inventory(self):
        print("Your Inventory:")
        if not self.inventory:
            print(" - (empty)")
        else:
            for item in self.inventory:
                print(f" - {item.name}")
        print(f"Gold: {self.gold}")

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
    Roll2 = random.randint(0, 2)
    category = ["Common", "Rare", "Boss"][Roll2]
    monsters = Monster0[category]
    monster = random.choice(monsters)
    print(f"\nA wild {monster['name']} has appeared! (Category: {category})")
    combat(monster)

def combat(monster):
    print(f"Engaging in combat with {monster['name']}...\n")
    monster_health = monster["health"]
    print(f"{monster['name']} has {monster_health} HP.")

    while monster_health > 0 and player.health > 0:
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

# ---- Game Loop ----
while True:
    print("\n1. View Inventory\n2. Fight a Monster\n3. Visit a Shop\n4. Visit Mistwood Basic Shop (StoreB)\n5. Quit Game")
    choice = input("What would you like to do? ").strip()
    if choice == "1":
        player.show_inventory()
    elif choice == "2":
        encounter_monster()
    elif choice == "3":
        Store0()  # Example: Visit Shop Level 0
    elif choice == "4":
        StoreB()  # Visit the Basic Orb Shop! (StoreB)
    elif choice == "5":
        print("Exiting the game...")
        break
    else:
        print("Invalid choice, please try again.")