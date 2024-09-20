import random
from collections import defaultdict

# Define the Card class
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

# Define the Deck class
class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None  # If the deck is empty

# Define the Player class
class Player:
    rank_order = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, '10': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
    
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.books = 0  # Track the number of sets of 4 a player has

    def draw_card(self, deck):
        card = deck.draw()
        if card:
            self.hand.append(card)
            self.hand = self.insertion_sort(self.hand)  # Sort the hand after drawing a card

    def remove_cards_by_rank(self, rank):
        matching_cards = [card for card in self.hand if card.rank == rank]
        self.hand = [card for card in self.hand if card.rank != rank]
        return matching_cards

    def has_rank(self, rank):
        return any(card.rank == rank for card in self.hand)

    def check_for_books(self):
        rank_count = defaultdict(int)
        for card in self.hand:
            rank_count[card.rank] += 1

        for rank, count in rank_count.items():
            if count == 4:  # If there are 4 cards of the same rank
                self.books += 1
                # Remove the cards from the hand
                self.hand = [card for card in self.hand if card.rank != rank]
                print(f"{self.name} has completed a book of {rank}s!")

    def show_hand(self):
        return ', '.join(str(card) for card in self.hand)

    # Insertion Sort Algorithm
    def insertion_sort(self, cards):
        for i in range(1, len(cards)):
            key_card = cards[i]
            j = i - 1
            while j >= 0 and self.rank_order[cards[j].rank] > self.rank_order[key_card.rank]:
                cards[j + 1] = cards[j]
                j -= 1
            cards[j + 1] = key_card
        return cards

# Define the Game class
class GoFishGame:
    def __init__(self, players):
        self.players = [Player(name) for name in players]
        self.deck = Deck()
        self.current_player_index = 0

    def deal(self):
        cards_per_player = 7 if len(self.players) <= 3 else 5
        for _ in range(cards_per_player):
            for player in self.players:
                player.draw_card(self.deck)

    def go_fish(self, player):
        print(f"{player.name} is going fishing...")
        player.draw_card(self.deck)
        player.check_for_books()

    def play_turn(self, player):
        print(f"\n{player.name}'s turn.")
        print(f"Current hand: {player.show_hand()}")

        # Ask for a rank from the next player
        opponent = self.players[(self.current_player_index + 1) % len(self.players)]
        print(f"Choose a rank to ask {opponent.name} for: ")
        rank = input(f"{player.name}, enter a rank (2-A): ").upper()

        if opponent.has_rank(rank):
            print(f"{opponent.name} has {rank}!")
            cards = opponent.remove_cards_by_rank(rank)
            player.hand.extend(cards)
            player.hand = player.insertion_sort(player.hand)  # Sort hand after receiving cards
        else:
            print(f"{opponent.name} does not have {rank}. Go Fish!")
            self.go_fish(player)

        player.check_for_books()

    def check_game_end(self):
        return len(self.deck.cards) == 0 or all(player.hand == [] for player in self.players)

    def display_books(self):
        for player in self.players:
            print(f"{player.name} has {player.books} books.")

    def play_game(self):
        self.deal()

        while not self.check_game_end():
            current_player = self.players[self.current_player_index]
            self.play_turn(current_player)

            # Move to the next player
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

        print("\nGame over!")
        self.display_books()
        winner = max(self.players, key=lambda player: player.books)
        print(f"The winner is {winner.name} with {winner.books} books!")

# Setup the game
if __name__ == "__main__":
    num_players = int(input("Enter the number of players: "))
    player_names = [input(f"Enter name for Player {i + 1}: ") for i in range(num_players)]

    game = GoFishGame(player_names)
    game.play_game()
