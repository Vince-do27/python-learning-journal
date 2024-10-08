import random

# card's info setup
class Card:
    def __init__(self, name, description, effect, damage=0, heal=0):
        self.name = name  # Name of the card
        self.description = description
        self.effect = effect  # heal or damage
        self.damage = damage  # Damage caused by the card
        self.heal = heal  # Health restored by the card

    #Plays the card, applying its effect to the player or opponent.
    def play(self, player, opponent):
        if self.effect == "heal":
            player.health += self.heal
            print(f"{player.name} used {self.name} and gained {self.heal} health.")
        elif self.effect == "damage":
            opponent.health -= self.damage
            print(f"{player.name} used {self.name} and dealt {self.damage} damage to {opponent.name}.")

# Unit Card class
class UnitCard(Card):
    def __init__(self, name, description, attack, hp):
        super().__init__(name, description, effect = None)
        self.attack = attack
        self.hp = hp

    def play(self, player, opponent):
        player.board.append(self)

# Spell Card class
class SpellCard(Card):
    def __init__(self, name, description, effect):
        super().__init__(name, description, effect = effect)
        self.effect = effect

    def play(self, player, opponent):
        self.effect(player, opponent)

#Linked list node for Deck
class Node:
    def __init__(self, card):
        self.card = card
        self.next = None

#Linked list Deck
class LinkedListDeck:
    def __init__(self):
        self.head = None

    def add(self, card): #New node is created for each card added into the deck
        newNode = Node(card)
        newNode.next = self.head
        self.head = newNode

    def draw(self): #Draw card from top of deck into hand, next card on top of the deck is now the head of the node.
        if self.head is None:
            return None
        drawnCard = self.head.card
        self.head = self.head.next
        return drawnCard

# Represent players 
class Player:
    def __init__(self, name):
        self.name = name  # what player
        self.health = 20  # Initial health 
        self.deck = []  # List to hold the player's deck of cards
        self.hand = []  # List to hold the player's current hand of cards
        self.board = []  # Holds units placed on the board

    # draw card
    def drawCard(self):
        if self.deck:
            card = self.deck.pop(0)
            self.hand.append(card)
            print(f"{self.name} drew {card.name}.")
        else:
            print("Deck is empty!")

    # play card 
    def playCard(self, card, opponent):
        if card in self.hand:
            card.play(self, opponent)
            self.hand.remove(card)
        else:
            print(f"{card.name} is not in hand!")

    # attack opponent method
    def attack(self, opponent):
        if self.board:
            total_attack = sum(unit.attack for unit in self.board)
            opponent.health -= total_attack
            print(f"{self.name}'s units attacked {opponent.name}, dealing {total_attack} damage.")
        else:
            print(f"{self.name} has no units to attack.")

    # Displays player's health
    def display_health(self):
        print(f"{self.name}'s current health: {self.health}")

#Game loop
class Game:
    log = [] #Log to keep track of all actions taken in the game

    def __init__(self, player1, player2): 
        self.players = [player1, player2]
        self.currentPlayerIndex = 0 #Keeps track of players' turn, 0 represents player1 and 1 represents player2
    
    #Initial draw
    def start(self):
        for player in self.players:
            for x in range(5):
                player.drawCard() 

        while all(player.health > 0 for player in self.players):
            self.turn()

            if any(player.health <= 0 for player in self.players):
                winner = self.players[self.currentPlayerIndex]
                print(f"The winner is {winner.name}!")
                break

            self.currentPlayerIndex = 1 - self.currentPlayerIndex # Switches players turn

        #Print log of all actions that took place in game
        print("\nGame Log: ")
        for entry in Game.log:
            print(entry)

    #Determine the current player and opponent
    def turn(self):
        player = self.players[self.currentPlayerIndex]
        opponent = self.players[1 - self.currentPlayerIndex]

        # Player's turn
        print(f"\n{player.name}'s turn:")
        player.drawCard()

        # Displays Player's health
        print(f"{player.name}'s health: {player.health}")
        print(f"{opponent.name}'s health: {opponent.health}")

        # Flags to track if the player has already played a Unit or Spell card
        unitPlayed = False
        spellPlayed = False

        # Allow the player to play one Unit and one Spell card
        while True:
            self.display_hand(player)
            choice = input("Enter the index of the card to play, 'a' to attack, or 'e' to end your turn: ").strip().lower()

            if choice == 'a':
                # Proceed to attack phase
                player.attack(opponent)
                break
            elif choice == 'e':
                # End the card playing phase
                break
            elif choice.isdigit():
                try:
                    card_index = int(choice)
                    card = player.hand[card_index]  # This line could raise an IndexError if the index is invalid

                    # Determine if the card is a UnitCard or SpellCard
                    if isinstance(card, UnitCard):
                        if unitPlayed:
                            print("You can only play one Unit Card per turn.")
                        else:
                            player.playCard(card, opponent)
                            unitPlayed = True  # Mark that a Unit Card has been played
                    elif isinstance(card, SpellCard):
                        if spellPlayed:
                            print("You can only play one Spell Card per turn.")
                        else:
                            player.playCard(card, opponent)
                            spellPlayed = True  # Mark that a Spell Card has been played
                except IndexError:
                    print("Invalid card index. Please choose a valid card from your hand.")
            else:
                print("Invalid choice. Please enter a valid option.")


    def display_hand(self, player):
        print(f"\n{player.name}'s hand:")
        for i, card in enumerate(player.hand):
            if isinstance(card, UnitCard):
                print(f"{i}: {card.name} (Unit, Attack: {card.attack}, HP: {card.hp}) - {card.description}")
            elif isinstance(card, SpellCard):
                print(f"{i}: {card.name} (Spell) - {card.description}")

# Create the players
player1 = Player("Player 1")
player2 = Player("Player 2")

def create_deck():
    deck = []
    for i in range(3):
        # Add unit cards
        deck.append(UnitCard("Pikachu", "Electric-type pokemon", attack=4, hp=4))
        deck.append(UnitCard("Charmander", "Fire-type pokemon", attack=5, hp=3))
        deck.append(UnitCard("Squirtle", "Water-type pokemon", attack=3, hp=5))
        deck.append(UnitCard("Bulbasaur", "Grass-type pokemone", attack=2, hp=6))
        
        # Add spell cards with proper effect functions
        deck.append(SpellCard("Healing Spell", "Heals 5 health", effect=heal_5_health))
        deck.append(SpellCard("Fireball", "Deals 4 damage to opponent", effect=deal_4_damage))

    random.shuffle(deck)  # Shuffle the deck
    return deck

# Functions for SpellCard effects
def heal_5_health(player, opponent):
    player.health += 5
    print(f"{player.name} healed 5 health!")

def deal_4_damage(player, opponent):
    opponent.health -= 4
    print(f"{player.name} dealt 4 damage to {opponent.name}!")

# Assign the decks to the players
player1.deck = create_deck()
player2.deck = create_deck()

# Start the game
game = Game(player1, player2)
game.start()
