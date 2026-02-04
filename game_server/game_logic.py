# Card game rules, deck, turn management
import random
from models import Card, Suit, Player, GameState

def create_deck() -> list[Card]:
    """ Create a standard 52-card deck """
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = [Card(rank, suit) for suit in Suit for rank in ranks]
    random.shuffle(deck)
    return deck

for c in create_deck():
    print(c)