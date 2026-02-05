# Card game rules, deck, turn management
import random
from typing import Optional
from models import Card, Suit, Player, GameState
from scoring import calculate_deadwood

def create_deck() -> list[Card]:
    """ Create a standard 52-card deck """
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = [Card(rank, suit) for suit in Suit for rank in ranks]
    random.shuffle(deck)
    return deck


def deal_cards(deck: list[Card], players: list[Player], cards_per_player: int) -> None:
    """ Deal cards to players from the deck """
    for player in players:
        for _ in range(cards_per_player):
            if deck:
                player.hand.append(deck.pop())


def next_turn(game_state: GameState) -> None:
    """ Move to the next player's turn """
    game_state.current_turn = (game_state.current_turn + 1) % len(game_state.players)


def take_top_card(game_state: GameState) -> Optional[Card]:
    """ Player takes the top card from the deck """
    if game_state.deck:
        card = game_state.deck.pop()
        game_state.players[game_state.current_turn].hand.append(card)
        return card
    return None


def discard_card(game_state: GameState, card:Card) -> bool:
    """ Player discards a card from their hand """
    player = game_state.players[game_state.current_turn]
    if card in player.hand:
        player.hand.remove(card)
        next_turn(game_state)
        return True
    return False


def fold(game_state: GameState) -> None:
    """ Player folds their hand """
    folder = game_state.players[game_state.current_turn]
    foldee = game_state.players[(game_state.current_turn + 1) % len(game_state.players)]


def start_game(players: list[Player]) -> GameState:
    """ Initialize game state and deal cards """
    deck = create_deck()
    deal_cards(deck, players, cards_per_player=10)
    return GameState(players=players, deck=deck, current_turn=0, top_card=deck.pop() if deck else None)


#== Example usage ==##
gs = start_game([Player(name="Katy"), Player(name="Karen")])
# %%