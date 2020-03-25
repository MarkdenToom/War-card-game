# !Python
# Simulates a game of War. See game instructions here: https://en.wikipedia.org/wiki/War_(card_game)
"""Rules in a nutshell:
The deck is divided evenly, with each player receiving 26 cards, dealt one at a time, face down. Anyone may deal first.
Each player places his stack of cards face down, in front of him.

Each player turns up a card at the same time and the player with the higher card
takes both cards and puts them, face down, on the bottom of his stack.

If the cards are the same rank, it is War. Each player turns up three cards face
down and one card face up. The player with the higher cards takes both piles
(six cards). If the turned-up cards are again the same rank, each player places
another card face down and turns another card face up. The player with the
higher card takes all 10 cards, and so on.

I'm ignoring double wars and wars won against players with less than 3 cards. I also removed jokers."""

from random import shuffle

# Deck variations.
card_types = 'H D S C'.split()
card_ranks = '2 3 4 5 6 7 8 9 10 J Q K A'.split()


# Class for main deck
class Deck:
    def __init__(self):
        self.card_stack = [(s, r) for s in card_types for r in card_ranks]
        print('Initializing card_stack...')

    def shuffle(self):
        print('Shuffling deck...')
        shuffle(self.card_stack)

    def split(self):
        return self.card_stack[:26], self.card_stack[26:]


# Class for cards in the hands of players.
class Hand:
    def __init__(self, cards):
        self.cards = cards

    def __str__(self):
        return f"Contains {len(self.cards)} cards."

    def add(self, added_card):
        self.cards.extend(added_card)
        print(f'{added_card} added.')

    def remove(self):
        return self.cards.pop()


# Class for the players
class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

    def play(self):
        drawn_card = self.hand.remove()
        print(f"{self.name} has played {drawn_card}")
        return drawn_card

    # When I match with my opponent, we do the following:
    def remove_war_cards(self):
        war_cards = []
        if len(self.hand.cards) < 3:
            return war_cards
        else:
            for _ in range(3):
                war_cards.append(self.hand.cards.pop(0))  # Could use self.hand.remove() here too
            return war_cards

    # Check if player has cards left
    def still_has_cards(self):
        return len(self.hand.cards) != 0


# Simulate a game
print("Welcome to War, let's begin...")

# Create deck and split it
d = Deck()
d.shuffle()
hand1, hand2 = d.split()

# Create players
computer = Player("computer", Hand(hand1))
user = Player("user", Hand(hand2))

total_rounds = 0
war_count = 0

# Main play-the-game loop
while user.still_has_cards() and computer.still_has_cards():
    total_rounds += 1
    print(f"""\nNew round!
Current score:
{user.name} card count: {str(len(user.hand.cards))}.
{computer.name} card count: {str(len(computer.hand.cards))}.
Playing cards...""")
    table_cards = []

    # Play cards TODO: create a function for this
    computer_card = computer.play()
    user_card = user.play()

    table_cards.append(computer_card)
    table_cards.append(user_card)

    # Check for War / matching card ranks
    if computer_card[1] == user_card[1]:
        war_count += 1
        print("\nWe have a match, time for war!")
        print("Each player removes 3 cards 'face down' and then one card face up")
        table_cards.extend(user.remove_war_cards())
        table_cards.extend(computer.remove_war_cards())

        # Play cards
        computer_card = computer.play()
        user_card = user.play()

        table_cards.append(computer_card)
        table_cards.append(user_card)

        # Check to see who had higher rank TODO: create a function for this
        if card_ranks.index(computer_card[1]) < card_ranks.index(user_card[1]):
            print(user.name + " has the higher card, adding to hand...")
            user.hand.add(table_cards)
        else:
            print(computer.name + " has the higher card, adding to hand...")
            computer.hand.add(table_cards)

    else:
        # Check to see who had higher rank
        if card_ranks.index(computer_card[1]) < card_ranks.index(user_card[1]):
            print(user.name + " has the higher card, adding to hand.")
            user.hand.add(table_cards)
        else:
            print(computer.name + " has the higher card, adding to hand.")
            computer.hand.add(table_cards)

print("\nGreat Game, it lasted:", total_rounds, "rounds.")
print("A war occured", war_count, "times.")
