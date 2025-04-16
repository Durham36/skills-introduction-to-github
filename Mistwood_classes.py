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
            
            
class LeatherArmor(Item):
    def __init__(self):
        super().__init__("Leather Armor", 10)
        
    def use(self, player):
        player.armor_equipped = "Leather Armor"
        print("you equipped Leather Armor!")
            
            
class Dagger(Item):
    def __init__(self):
        super().__init__("Dagger", 7)
        
    def use(self, player):
        player.dagger_active = True
        print("You used Dagger! Damage increased.")
            
        
class FireOrb(Item):
    def __init__(self):
        super().__init__("Fire Orb", 2)
        
    def use(self, player):
        player.fire_orb_bonus += 1
        print("You used a Fire Orb! +1 damage on your next attack.")


class WaterOrb(Item):
    def __init__(self):
        super().__init__("Water Orb", 3)
        
    def use(self, player):
        if player.health < player.max_health:
            player.health = min(player.health + 1, player.max_health)
            print("You used Water Orb and healed for 1 HP.")
        else:
            print("You're already at full health. Water Orb does nothing.")


class EarthOrb(Item):
    def __init__(self):
        super().__init__("Earth Orb", 3)
            
    def use(self, player):
        player.earth_orb_charges += 1
        print(f"You used an Earth Orb! Enemy attack will be reduced by 1. ({player.earth_orb_charges} charge(s) active)")
            


class Player:
    def __init__(self):
        self.health = 3
        self.max_health = 3
        self.inventory = []
        self.gold = 10
        self.level = 0
        self.fire_orb_bonus = 0
        self.earth_orb_charges = 0
        self.dagger_active = False
        self.armor_equipped = None

    def use_item(self):
        if not self.inventory:
            print("You have no items.")
            return

        print("\nInventory Items:")
        for i, item in enumerate(self.inventory, 1):
            print(f"{i}. {item.name}")
    
        choice = input("Enter the number of the item you want to use (or press enter to cancel): ").strip()
        if not choice:
            print("Cancelled item use.")
            return

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(self.inventory):
            print("Invalid choice.")
            return

        item_index = int(choice) - 1
        item = self.inventory[item_index]

        item.use(self)  # Heal the player
        del self.inventory[item_index]  # Remove the used item

    def buy_item(self, item_name, item_cost):
        item_lookup = {
            "Health Potion": HealthPotion,
            "Fire Orb": FireOrb,
            "Earth Orb": EarthOrb,
            "Dagger": Dagger,
            "Water Orb": WaterOrb,
            "Leather Armor": LeatherArmor
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

    def show_inventory(self):  # Added 'self' to make this an instance method
        print("Your Inventory:")
        if not self.inventory:
            print(" - (empty)")
        else:
            for item in self.inventory:
                print(f" - {item.name}")
        print(f"Equipped Armor: {self.armor_equipped if self.armor_equipped else 'None'}")
        print(f"Gold: {self.gold}")