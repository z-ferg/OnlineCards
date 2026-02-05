from ast import List
from typing import Set
from models import Card, Player, GameState


def get_rank_value(rank: str) -> int:
    """ Convert rank to a numeric value for sorting and run detection """
    if rank == 'A':
        return 1
    elif rank == 'J':
        return 11
    elif rank == 'Q':
        return 12
    elif rank == 'K':
        return 13
    else:
        return int(rank)


def get_card_points(rank: str) -> int:
    """ Convert card rank to its point value for deadwood calculation """
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 1
    else:
        return int(rank)


def find_all_valid_melds(hand: list[Card]) -> list[list[Card]]:
    """ Find all valid melds in a player's hand (runs and sets) """
    melds = []
    
    # Find all sets (3-4 cards of same rank)
    rank_groups = {}
    for card in hand:
        rank = card.rank
        if rank not in rank_groups:
            rank_groups[rank] = []
        rank_groups[rank].append(card)
    
    for rank, cards in rank_groups.items():
        if len(cards) >= 3:
            melds.append(cards[:3])
        if len(cards) == 4:
            melds.append(cards)
    
    # Find all runs (3+ cards of same suit in sequence)
    suit_groups = {}
    for card in hand:
        suit = card.suit
        if suit not in suit_groups:
            suit_groups[suit] = []
        suit_groups[suit].append(card)
    
    for suit, cards in suit_groups.items():
        cards.sort(key=lambda c: c.rank)
        for start in range(len(cards)):
            for end in range(start + 2, len(cards)):
                is_run = True
                for i in range(start, end):
                    if cards[i+1].rank != cards[i].rank + 1:
                        is_run = False
                        break
                if is_run:
                    melds.append(cards[start:end+1])
    
    return melds


def minimize_deadwood(hand: list[Card]) -> tuple[list[list[Card]], int]:
    """  
    Find optimal meld combination to minimize deadwood points 
    
    Returns:
        Tuple of (best_melds, deadwood_points)
        - best_melds: List of melds
        - deadwood_points: Total points of cards not in melds
    """
    all_melds = find_all_valid_melds(hand)
    
    best_deadwood = sum(get_card_points(card.rank) for card in hand)
    best_melds = []
    
    def backtrack(meld_index: int, used_cards: Set[Card], current_melds: List[List[Card]]):
        nonlocal best_deadwood, best_melds
        
        deadwood_cards = [card for card in hand if card not in used_cards]
        deadwood = sum(get_card_points(card.rank) for card in deadwood_cards)
        
        if deadwood < best_deadwood:
            best_deadwood = deadwood
            best_melds = current_melds.copy()
        
        for i in range(meld_index, len(all_melds)):
            meld = all_melds[i]

            if not any(card in used_cards for card in meld):
                new_used = used_cards | set(meld)
                backtrack(i + 1, new_used, current_melds + [meld])
    
    backtrack(0, set(), [])
    return best_melds, best_deadwood


def calculate_deadwood(hand: List[Card], melds: List[List[Card]]) -> int:
    """ Calculate total deadwood points given hand and melds """
    melded_cards = set()
    for meld in melds:
        melded_cards.update(meld)
    
    deadwood_cards = [card for card in hand if card not in melded_cards]
    return sum(get_card_points(card.rank) for card in deadwood_cards)