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
    """ Current player takes the top card from the deck """
    if game_state.deck:
        card = game_state.deck.pop()
        game_state.players[game_state.current_turn].hand.append(card)
        return card
    return None


def discard_card(game_state: GameState, card:Card) -> bool:
    """ Current player discards a card from their hand (Auto progresses turns)"""
    player = game_state.players[game_state.current_turn]
    if card in player.hand:
        player.hand.remove(card)
        next_turn(game_state)
        return True
    return False


def fold(game_state: GameState) -> None:
    """ Current player folds their hand """
    folder = game_state.players[game_state.current_turn]
    foldee = game_state.players[(game_state.current_turn + 1) % len(game_state.players)]
    
    folder_deadwood = calculate_deadwood(folder.hand)
    if folder_deadwood == 0: # Gin condition
        folder.score += 20 + calculate_deadwood(foldee.hand)    # 20 point bonus for gin
    else:   # Knock condition
        foldee_deadwood = calculate_deadwood(foldee.hand)
        if folder_deadwood < foldee_deadwood:   # Folder has less deadwood
            folder.score += foldee_deadwood - folder_deadwood
        else:                                   # Foldee has less or equal deadwood
            foldee.score += 10 + (folder_deadwood - foldee_deadwood) # 10 point undercut bonus


def start_game(players: list[Player]) -> GameState:
    """ Initialize game state and deal cards """
    deck = create_deck()
    deal_cards(deck, players, cards_per_player=10)
    return GameState(players=players, deck=deck, current_turn=0, top_card=deck.pop() if deck else None)


#== Example usage ==##
gs = start_game([Player(name="Katy"), Player(name="Karen")])
# %%