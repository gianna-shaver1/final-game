import random
import time

# Define player and enemy stats
class Player:
    def __init__(self):
        self.health = 10
        self.attack = 5
        self.defense = 3
        self.inventory = []
        self.position = (0, 0)  # Starting position of the player

    def display_stats(self):
        print(f"Health: {self.health}/10   Attack: {self.attack}   Defense: {self.defense}")
        print(f"Inventory: {', '.join(self.inventory) if self.inventory else 'None'}")

class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def is_alive(self):
        return self.health > 0

# Create a simple random dungeon
def create_dungeon():
    # Let's create a 5x5 grid of rooms
    dungeon = [['Empty' for _ in range(5)] for _ in range(5)]
    # Place enemies randomly
    num_enemies = random.randint(2, 5)
    for _ in range(num_enemies):
        x, y = random.randint(0, 4), random.randint(0, 4)
        while dungeon[x][y] != 'Empty':
            x, y = random.randint(0, 4), random.randint(0, 4)
        dungeon[x][y] = 'Enemy'
    # Place some items randomly
    num_items = random.randint(2, 4)
    for _ in range(num_items):
        x, y = random.randint(0, 4), random.randint(0, 4)
        while dungeon[x][y] != 'Empty':
            x, y = random.randint(0, 4), random.randint(0, 4)
        dungeon[x][y] = 'Item'
    # Set exit
    dungeon[4][4] = 'Exit'
    return dungeon

# Display the dungeon
def display_dungeon(dungeon, player_pos):
    for i in range(5):
        row = ''
        for j in range(5):
            if (i, j) == player_pos:
                row += 'P '  # Player's position
            elif dungeon[i][j] == 'Empty':
                row += '. '  # Empty room
            elif dungeon[i][j] == 'Enemy':
                row += 'E '  # Enemy
            elif dungeon[i][j] == 'Item':
                row += 'I '  # Item
            elif dungeon[i][j] == 'Exit':
                row += 'X '  # Exit
        print(row)
    print()

# Combat system
def combat(player, enemy):
    print(f"\nYou have encountered a {enemy.name}!")
    while player.health > 0 and enemy.is_alive():
        print(f"\n{enemy.name}'s Health: {enemy.health}")
        print("What do you want to do?")
        print("1. Attack")
        print("2. Defend")
        print("3. Use item")
        action = input("Choose action (1/2/3): ")

        if action == '1':  # Attack
            damage = max(0, player.attack - enemy.attack)
            enemy.health -= damage
            print(f"You attack the {enemy.name} for {damage} damage!")
        elif action == '2':  # Defend
            print("You brace yourself for the enemy's attack.")
            player.defense += 2  # Temporary defense boost
            time.sleep(1)
            player.defense -= 2  # Reset after the turn
        elif action == '3' and 'Potion' in player.inventory:  # Use item
            player.health = min(10, player.health + 5)
            player.inventory.remove('Potion')
            print("You use a health potion and recover 5 health!")
        else:
            print("Invalid action. You do nothing.")

        if enemy.is_alive():
            enemy_damage = max(0, enemy.attack - player.defense)
            player.health -= enemy_damage
            print(f"The {enemy.name} attacks you for {enemy_damage} damage.")

    if player.health <= 0:
        print("\nYou have been defeated!")
        return False
    else:
        print(f"\nYou defeated the {enemy.name}!")
        return True

# Main game loop
def main():
    print("Welcome to Dungeon Escape!\n")
    player = Player()
    dungeon = create_dungeon()
    player_position = (0, 0)
    
    while True:
        print("\n------------------------------------")
        display_dungeon(dungeon, player_position)
        player.display_stats()
        print("------------------------------------")
        print("What do you want to do?")
        print("1. Go North")
        print("2. Go South")
        print("3. Go East")
        print("4. Go West")
        print("5. Quit")
        action = input("Choose action (1/2/3/4/5): ")

        if action == '5':
            print("Thank you for playing Dungeon Escape!")
            break

        # Move the player
        x, y = player_position
        if action == '1' and x > 0:
            player_position = (x - 1, y)
        elif action == '2' and x < 4:
            player_position = (x + 1, y)
        elif action == '3' and y < 4:
            player_position = (x, y + 1)
        elif action == '4' and y > 0:
            player_position = (x, y - 1)
        else:
            print("You can't move in that direction!")

        room = dungeon[player_position[0]][player_position[1]]
        if room == 'Enemy':
            enemy = Enemy("Goblin", random.randint(5, 10), random.randint(1, 3))
            if not combat(player, enemy):
                break
        elif room == 'Item':
            item = random.choice(['Potion', 'Sword', 'Key'])
            player.inventory.append(item)
            print(f"You found a {item}!")
        elif room == 'Exit':
            print("You have found the exit! Congratulations, you escaped the dungeon!")
            break

if __name__ == "__main__":
    main()
